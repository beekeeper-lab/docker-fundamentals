#!/usr/bin/env python3
"""Emit a JSON status report describing this course's build state.

Output schema (stdout, single JSON object):

    {
      "course_name": "<basename of course root>",
      "stage": "post-pipeline" | "pre-pipeline" | "empty",
      "sources":     {"count": N, "files": [...]},
      "html":        {"count": N, "missing": [<source>, ...]},
      "images":      {"on_disk": N, "planned": N,
                      "missing": [{"file": "...", "title": "..."}]},
      "audio":       {"files": N,
                      "narration_blocks": N,
                      "missing_chars": N,
                      "per_module": {
                          "<source-stem>": {
                              "blocks": N, "generated": N, "missing_chars": N
                          }, ...}},
      "quizzes":     {"count": N, "total_questions": N,
                      "modules_without": [<source>, ...]},
      "todos":       <int>
    }

`todos` = images.missing + (max 0 narration_blocks - audio.files) + len(quizzes.modules_without).

This script is the canonical per-course status emitter; the parent-level
`/ReportStatus` skill aggregates these JSON outputs into a portfolio table.
The script is portable across courses: it dynamically loads each course's
`scripts/build_course.py` to honor that course's `resolve_quiz_json()`
naming convention (Day_XX, Module_XX, Week_XX_Module_YY, etc.).
"""

from __future__ import annotations

import importlib.util
import json
import re
import sys
from pathlib import Path

COURSE_ROOT = Path(__file__).resolve().parent.parent
SOURCE_DIR = COURSE_ROOT / "source"
HTML_DIR = COURSE_ROOT / "html"
IMAGES_DIR = COURSE_ROOT / "images"
AUDIO_DIR = COURSE_ROOT / "audio"
QUIZ_DIR = COURSE_ROOT / "Quiz"
BUILD_SCRIPT = COURSE_ROOT / "scripts" / "build_course.py"

IMAGE_PLAN_FILES = ["IMAGE-PLAN.md", "IMAGE-PLAN-ADDITIONS.md"]


# ── Quiz resolver ────────────────────────────────────────────────────────────

def _load_resolve_quiz_json():
    """Load this course's resolve_quiz_json from build_course.py. Returns the
    callable, or None if build_course.py is absent or doesn't expose one.
    """
    if not BUILD_SCRIPT.exists():
        return None
    spec = importlib.util.spec_from_file_location(
        f"_status_build_{COURSE_ROOT.name.replace('-', '_')}", BUILD_SCRIPT
    )
    if spec is None or spec.loader is None:
        return None
    module = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(module)
    except Exception:
        return None
    return getattr(module, "resolve_quiz_json", None)


# ── Source / HTML ────────────────────────────────────────────────────────────

def _list_sources() -> list[Path]:
    if not SOURCE_DIR.exists():
        return []
    return sorted(p for p in SOURCE_DIR.glob("*.md") if p.is_file())


def _list_html() -> set[str]:
    if not HTML_DIR.exists():
        return set()
    return {p.stem for p in HTML_DIR.glob("*.html") if p.is_file()}


# ── Image plan ───────────────────────────────────────────────────────────────

_IMAGE_HEADING_RE = re.compile(r"^###\s+Image\s+\d+\s*[:.]?\s*(.*)$")
_IMAGE_FILE_RE = re.compile(r"^[-*]\s*\*\*File\*\*\s*[:：]\s*[`\"']?([^`\"']+?)[`\"']?\s*$")


def _parse_image_plan() -> tuple[int, list[dict]]:
    """Return (planned_count, missing_entries) where each missing entry has
    {"file": <relative path string>, "title": <descriptive title>}.

    The plan format is:

        ### Image N: <title>
        - **File**: `images/module-XX/foo.png`
        - **Description**: ...

    `planned_count` is the number of `### Image N` headings across all plan files.
    `missing` checks each `**File**` path on disk relative to the course root,
    falling back to `<course-root>/images/<path>` if the path doesn't include
    the leading "images/".
    """
    planned = 0
    missing: list[dict] = []
    last_title: str | None = None

    for plan_name in IMAGE_PLAN_FILES:
        plan_path = COURSE_ROOT / plan_name
        if not plan_path.exists():
            continue
        for line in plan_path.read_text(encoding="utf-8", errors="replace").splitlines():
            heading = _IMAGE_HEADING_RE.match(line)
            if heading:
                planned += 1
                last_title = heading.group(1).strip() or None
                continue
            file_match = _IMAGE_FILE_RE.match(line)
            if file_match:
                rel = file_match.group(1).strip()
                # Try a few resolutions: as-is from course root, or under images/
                candidates = [
                    COURSE_ROOT / rel,
                    COURSE_ROOT / "images" / rel.lstrip("/"),
                ]
                if not any(c.exists() for c in candidates):
                    missing.append({"file": rel, "title": last_title or ""})
    return planned, missing


# ── Narration / audio ────────────────────────────────────────────────────────

_NARRATION_LINE_RE = re.compile(r"^>\s*🎙️\s*(.*)$")
_QUOTE_CONT_RE = re.compile(r"^>\s?(.*)$")


def _extract_narration_blocks(md_text: str) -> list[str]:
    """Return list of narration block texts (concatenated continuation lines).

    A narration block starts with `> 🎙️ ...` and continues across any
    subsequent contiguous `>` lines (until a non-quote line or another
    narration start). Blank quote lines (`>`) within the block are kept as
    spaces.
    """
    blocks: list[str] = []
    current: list[str] | None = None
    for line in md_text.splitlines():
        start = _NARRATION_LINE_RE.match(line)
        if start:
            if current is not None:
                blocks.append(" ".join(s.strip() for s in current).strip())
            current = [start.group(1)]
            continue
        if current is not None:
            cont = _QUOTE_CONT_RE.match(line)
            if cont:
                # If the continuation is a *new* narration heading, stop.
                if cont.group(1).lstrip().startswith("🎙️"):
                    blocks.append(" ".join(s.strip() for s in current).strip())
                    current = [cont.group(1).lstrip().lstrip("🎙️").strip()]
                else:
                    current.append(cont.group(1))
                continue
            # Non-quote line ends the block
            blocks.append(" ".join(s.strip() for s in current).strip())
            current = None
    if current is not None:
        blocks.append(" ".join(s.strip() for s in current).strip())
    return [b for b in blocks if b]


def _audio_files(stem: str) -> int:
    d = AUDIO_DIR / stem
    if not d.exists():
        return 0
    return sum(1 for p in d.glob("*.mp3") if p.is_file())


# ── Quiz parsing ─────────────────────────────────────────────────────────────

def _quiz_stats(resolve):
    """Walk Quiz/ for files and totals; build modules_without list using
    the course's resolve_quiz_json (if available) against each source MD.
    A None return from resolve_quiz_json means either "not a module file"
    (skip) or "expected location missing" — distinguish by also probing
    a synthetic call against a dummy filename to see if the resolver only
    returns paths-that-exist or always returns the planned path.

    Implementation simplified: we re-implement the convention by attempting
    the resolver. Since most resolvers return None for non-module files
    AND for missing files alike, we additionally do a "would have matched
    the module pattern" check (regex `module-(\\d+)-` or `day-(\\d+)-` or
    `week-(\\d+)-module-(\\d+)-`) to flag missing-quiz modules.
    """
    files: list[Path] = []
    if QUIZ_DIR.exists():
        files = sorted(p for p in QUIZ_DIR.rglob("*.json") if p.is_file())

    total_questions = 0
    for f in files:
        try:
            data = json.loads(f.read_text(encoding="utf-8"))
        except Exception:
            continue
        if isinstance(data, dict):
            if "total_questions" in data and isinstance(data["total_questions"], int):
                total_questions += data["total_questions"]
            elif isinstance(data.get("questions"), list):
                total_questions += len(data["questions"])

    modules_without: list[str] = []
    module_re = re.compile(
        r"^(?:module-\d+-|day-\d+-|week-\d+-module-\d+-)", re.IGNORECASE
    )
    if resolve is not None:
        for src in _list_sources():
            if not module_re.match(src.name):
                continue
            result = resolve(src.name)
            if result is None:
                modules_without.append(src.name)

    return {
        "count": len(files),
        "total_questions": total_questions,
        "modules_without": modules_without,
    }


# ── Main ─────────────────────────────────────────────────────────────────────

def build_status() -> dict:
    sources = _list_sources()
    html_stems = _list_html()

    if not sources:
        return {
            "course_name": COURSE_ROOT.name,
            "stage": "empty",
            "sources": {"count": 0, "files": []},
            "html": {"count": len(html_stems), "missing": []},
            "images": {"on_disk": 0, "planned": 0, "missing": []},
            "audio": {"files": 0, "narration_blocks": 0,
                      "missing_chars": 0, "per_module": {}},
            "quizzes": {"count": 0, "total_questions": 0, "modules_without": []},
            "todos": 0,
        }

    stage = "post-pipeline" if BUILD_SCRIPT.exists() else "pre-pipeline"

    # HTML missing — sources whose stem isn't in html/
    html_missing = sorted(s.name for s in sources if s.stem not in html_stems)

    # Images
    on_disk = (
        sum(1 for _ in IMAGES_DIR.rglob("*.png")) if IMAGES_DIR.exists() else 0
    )
    planned, missing_imgs = _parse_image_plan()
    if stage == "pre-pipeline":
        # No reliable image plan to diff against
        missing_imgs = []

    # Audio + narration
    total_blocks = 0
    total_audio = 0
    total_missing_chars = 0
    per_module: dict[str, dict] = {}
    for src in sources:
        text = src.read_text(encoding="utf-8", errors="replace")
        blocks = _extract_narration_blocks(text)
        n_blocks = len(blocks)
        n_audio = _audio_files(src.stem)
        # The first n_audio blocks are considered generated; remaining missing.
        missing_blocks = blocks[n_audio:] if n_audio < n_blocks else []
        miss_chars = sum(len(b) for b in missing_blocks)
        if n_blocks or n_audio:
            per_module[src.name] = {
                "blocks": n_blocks,
                "generated": min(n_audio, n_blocks),
                "missing_chars": miss_chars,
            }
        total_blocks += n_blocks
        total_audio += min(n_audio, n_blocks)
        total_missing_chars += miss_chars

    # Quizzes
    resolve = _load_resolve_quiz_json()
    quiz_info = _quiz_stats(resolve)

    todos = (
        len(missing_imgs)
        + max(0, total_blocks - total_audio)
        + len(quiz_info["modules_without"])
    )

    return {
        "course_name": COURSE_ROOT.name,
        "stage": stage,
        "sources": {"count": len(sources), "files": [s.name for s in sources]},
        "html": {"count": len(html_stems), "missing": html_missing},
        "images": {
            "on_disk": on_disk,
            "planned": planned,
            "missing": missing_imgs,
        },
        "audio": {
            "files": total_audio,
            "narration_blocks": total_blocks,
            "missing_chars": total_missing_chars,
            "per_module": per_module,
        },
        "quizzes": quiz_info,
        "todos": todos,
    }


def main():
    status = build_status()
    json.dump(status, sys.stdout, indent=2)
    sys.stdout.write("\n")


if __name__ == "__main__":
    main()
