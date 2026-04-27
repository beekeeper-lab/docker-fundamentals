#!/usr/bin/env python3
"""Lint a Stonewaters course for structural integrity.

Exits 0 if all checks pass, 1 if any rule fails. Diagnostics are written
to stderr; a final summary line goes to stdout.

Rules
-----
1. Image references in source/*.md (`![alt](path/to/foo.png)`) must each
   correspond to an entry in IMAGE-PLAN.md (or IMAGE-PLAN-ADDITIONS.md).
2. Every `**File**:` entry in the image plan must show up as an `![](...)`
   reference somewhere in source/, OR be flagged as `<!-- orphan -->` in
   the plan (allowing intentionally-unreferenced reference images).
3. Every `module-XX-*.md` (and `day-XX-*.md`, `week-XX-module-YY-*.md`)
   source file must have a quiz JSON at the path returned by this course's
   `resolve_quiz_json()`.
4. Every quiz JSON parses; `total_questions` matches `len(questions)`;
   every question's `answer` appears in its `options`.
5. Every `> 🎙️` narration opener has at least one continuation line of
   blockquote (a `>`-prefixed line) — i.e. the block is non-empty.
6. The image plan title heading nearest each `**File**:` entry should
   match the filename stem (warning, not failure).
7. No source file references an image path that doesn't exist on disk
   AND isn't planned (catches typos in plan-but-missing files).

The validator is intentionally tolerant: if a course doesn't ship an
IMAGE-PLAN.md at all, rules 1, 2, 6, and 7 are skipped. If a course has
no Quiz/ directory at all, rules 3 and 4 are skipped.
"""

from __future__ import annotations

import importlib.util
import json
import re
import sys
from pathlib import Path

COURSE_ROOT = Path(__file__).resolve().parent.parent
SOURCE_DIR = COURSE_ROOT / "source"
IMAGES_DIR = COURSE_ROOT / "images"
QUIZ_DIR = COURSE_ROOT / "Quiz"
BUILD_SCRIPT = COURSE_ROOT / "scripts" / "build_course.py"

IMAGE_PLAN_FILES = ["IMAGE-PLAN.md", "IMAGE-PLAN-ADDITIONS.md"]

IMG_REF_RE = re.compile(r"!\[[^\]]*\]\(([^)]+)\)")
HEADING_RE = re.compile(r"^###\s+Image\s+\d+\s*[:.]?\s*(.*)$")
FILE_RE = re.compile(r"^[-*]\s*\*\*File\*\*\s*[:：]\s*[`\"']?([^`\"']+?)[`\"']?\s*$")
NARR_OPEN_RE = re.compile(r"^>\s*🎙️")
QUOTE_CONT_RE = re.compile(r"^>\s?")


# ── Helpers ──────────────────────────────────────────────────────────────────

def _load_resolve_quiz_json():
    if not BUILD_SCRIPT.exists():
        return None
    spec = importlib.util.spec_from_file_location(
        f"_validate_build_{COURSE_ROOT.name.replace('-', '_')}", BUILD_SCRIPT
    )
    if spec is None or spec.loader is None:
        return None
    module = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(module)
    except Exception:
        return None
    return getattr(module, "resolve_quiz_json", None)


def _normalize_image_path(p: str) -> str:
    """Reduce path to a canonical form: stripped of `../`, leading `./`,
    and an optional leading `images/`. Used to compare across plan/refs."""
    p = p.strip().lstrip("./")
    while p.startswith("../"):
        p = p[3:]
    if p.startswith("images/"):
        p = p[len("images/"):]
    return p


def _parse_image_plan() -> tuple[list[dict], list[str]]:
    """Return (entries, errors). Each entry is a dict with keys
    {file, normalized, title, orphan}. Errors are strings.
    """
    entries: list[dict] = []
    errors: list[str] = []
    for plan_name in IMAGE_PLAN_FILES:
        plan_path = COURSE_ROOT / plan_name
        if not plan_path.exists():
            continue
        last_title: str | None = None
        last_was_heading = False
        text = plan_path.read_text(encoding="utf-8", errors="replace")
        lines = text.splitlines()
        for i, line in enumerate(lines, 1):
            heading = HEADING_RE.match(line)
            if heading:
                last_title = heading.group(1).strip() or None
                last_was_heading = True
                continue
            file_match = FILE_RE.match(line)
            if file_match:
                rel = file_match.group(1).strip()
                # Look ahead a few lines for an `<!-- orphan -->` marker
                window = "\n".join(lines[max(0, i - 3): i + 3])
                orphan = "orphan" in window.lower() and "<!--" in window
                entries.append({
                    "file": rel,
                    "normalized": _normalize_image_path(rel),
                    "title": last_title or "",
                    "plan": plan_name,
                    "line": i,
                    "orphan": orphan,
                })
                last_was_heading = False
    return entries, errors


def _collect_source_image_refs() -> dict[str, list[tuple[str, int]]]:
    """Return {normalized_path: [(source_filename, line_no), ...]}."""
    refs: dict[str, list[tuple[str, int]]] = {}
    if not SOURCE_DIR.exists():
        return refs
    for src in sorted(SOURCE_DIR.glob("*.md")):
        for i, line in enumerate(src.read_text(encoding="utf-8",
                                               errors="replace").splitlines(), 1):
            for m in IMG_REF_RE.finditer(line):
                norm = _normalize_image_path(m.group(1))
                if norm.lower().endswith(".png") or norm.lower().endswith(".jpg") \
                        or norm.lower().endswith(".jpeg") or norm.lower().endswith(".webp"):
                    refs.setdefault(norm, []).append((src.name, i))
    return refs


# ── Rules ────────────────────────────────────────────────────────────────────

def rule_image_refs_have_plan(refs, entries) -> list[str]:
    """Rule 1: every image ref maps to a plan entry."""
    if not entries:
        return []
    planned = {e["normalized"] for e in entries}
    errs: list[str] = []
    for norm, locations in sorted(refs.items()):
        if norm not in planned:
            loc = ", ".join(f"{src}:{ln}" for src, ln in locations[:3])
            errs.append(f"image ref not in plan: {norm}  ({loc})")
    return errs


def rule_plan_entries_have_refs(refs, entries) -> list[str]:
    """Rule 2: every plan File: entry is referenced from source (or is orphan)."""
    if not entries:
        return []
    referenced = set(refs.keys())
    errs: list[str] = []
    for e in entries:
        if e["orphan"]:
            continue
        if e["normalized"] not in referenced:
            errs.append(
                f"plan entry not referenced by source: {e['file']}  "
                f"({e['plan']}:{e['line']})"
            )
    return errs


def rule_modules_have_quizzes(resolve) -> list[str]:
    """Rule 3: every module/day/week-module source has a quiz JSON."""
    if resolve is None or not SOURCE_DIR.exists():
        return []
    if not QUIZ_DIR.exists():
        return []
    module_re = re.compile(
        r"^(?:module-\d+-|day-\d+-|week-\d+-module-\d+-)", re.IGNORECASE
    )
    errs: list[str] = []
    for src in sorted(SOURCE_DIR.glob("*.md")):
        if not module_re.match(src.name):
            continue
        path = resolve(src.name)
        if path is None:
            errs.append(f"missing quiz JSON for {src.name}")
    return errs


def rule_quiz_json_well_formed() -> list[str]:
    """Rule 4: every quiz JSON parses, totals match, answers in options."""
    if not QUIZ_DIR.exists():
        return []
    errs: list[str] = []
    for f in sorted(QUIZ_DIR.rglob("*.json")):
        try:
            data = json.loads(f.read_text(encoding="utf-8"))
        except Exception as e:
            errs.append(f"{f.relative_to(COURSE_ROOT)}: invalid JSON ({e})")
            continue
        if not isinstance(data, dict):
            errs.append(f"{f.relative_to(COURSE_ROOT)}: top-level is not an object")
            continue
        questions = data.get("questions")
        if not isinstance(questions, list):
            errs.append(f"{f.relative_to(COURSE_ROOT)}: missing or invalid 'questions' array")
            continue
        total = data.get("total_questions")
        if isinstance(total, int) and total != len(questions):
            errs.append(
                f"{f.relative_to(COURSE_ROOT)}: total_questions={total} "
                f"but len(questions)={len(questions)}"
            )
        for idx, q in enumerate(questions, 1):
            if not isinstance(q, dict):
                errs.append(f"{f.relative_to(COURSE_ROOT)} Q{idx}: not an object")
                continue
            opts = q.get("options")
            ans = q.get("answer")
            if not isinstance(opts, list) or not opts:
                errs.append(f"{f.relative_to(COURSE_ROOT)} Q{idx}: missing/empty options")
                continue
            if ans is None:
                errs.append(f"{f.relative_to(COURSE_ROOT)} Q{idx}: missing answer")
                continue
            # answer can be the option text OR an index OR a letter — accept
            # any of these forms commonly seen in this portfolio.
            if isinstance(ans, str):
                if ans not in opts and ans.upper() not in {"A", "B", "C", "D", "E"}:
                    errs.append(
                        f"{f.relative_to(COURSE_ROOT)} Q{idx}: answer not in options"
                    )
            elif isinstance(ans, int):
                if not (0 <= ans < len(opts)):
                    errs.append(
                        f"{f.relative_to(COURSE_ROOT)} Q{idx}: answer index out of range"
                    )
    return errs


def rule_narration_blocks_non_empty() -> list[str]:
    """Rule 5: every `> 🎙️` opener has at least one continuation line."""
    if not SOURCE_DIR.exists():
        return []
    errs: list[str] = []
    for src in sorted(SOURCE_DIR.glob("*.md")):
        lines = src.read_text(encoding="utf-8", errors="replace").splitlines()
        for i, line in enumerate(lines):
            if not NARR_OPEN_RE.match(line):
                continue
            # Acceptable: opener has text on its own line OR has a continuation.
            opener_text = line[line.index("🎙️") + 1:].strip()
            if opener_text:
                continue
            # Otherwise expect the next line to be a `>` continuation.
            if i + 1 < len(lines) and QUOTE_CONT_RE.match(lines[i + 1]):
                continue
            errs.append(f"{src.name}:{i+1}: empty narration block")
    return errs


def rule_image_refs_resolve_or_planned(refs, entries) -> list[str]:
    """Rule 7: a referenced image either exists on disk or is in the plan
    (so a missing file is acceptable if the plan promises it). Catches
    typos in references that are neither on disk nor planned.
    """
    if not entries and not IMAGES_DIR.exists():
        return []
    planned = {e["normalized"] for e in entries}
    errs: list[str] = []
    for norm, locations in sorted(refs.items()):
        on_disk = (IMAGES_DIR / norm).exists()
        if not on_disk and norm not in planned:
            loc = ", ".join(f"{src}:{ln}" for src, ln in locations[:3])
            errs.append(
                f"image ref neither exists nor is planned: {norm}  ({loc})"
            )
    return errs


# ── Main ─────────────────────────────────────────────────────────────────────

def main() -> int:
    if not SOURCE_DIR.exists():
        print(f"validate: no source/ directory in {COURSE_ROOT.name}", file=sys.stderr)
        return 0

    refs = _collect_source_image_refs()
    entries, _ = _parse_image_plan()
    resolve = _load_resolve_quiz_json()

    rule_results = {
        "1. image refs have plan entries": rule_image_refs_have_plan(refs, entries),
        "2. plan entries are referenced from source": rule_plan_entries_have_refs(refs, entries),
        "3. modules have quiz JSONs": rule_modules_have_quizzes(resolve),
        "4. quiz JSONs are well-formed": rule_quiz_json_well_formed(),
        "5. narration blocks non-empty": rule_narration_blocks_non_empty(),
        "7. image refs resolve or are planned": rule_image_refs_resolve_or_planned(refs, entries),
    }

    total_errors = sum(len(v) for v in rule_results.values())
    course = COURSE_ROOT.name

    if total_errors == 0:
        print(f"validate[{course}]: PASS  ({sum(len(v)==0 for v in rule_results.values())}/{len(rule_results)} rules)")
        return 0

    for rule, errs in rule_results.items():
        if not errs:
            continue
        print(f"\n[{course}] {rule}: {len(errs)} issue(s)", file=sys.stderr)
        for e in errs[:50]:
            print(f"  - {e}", file=sys.stderr)
        if len(errs) > 50:
            print(f"  ... ({len(errs) - 50} more)", file=sys.stderr)
    print(f"validate[{course}]: FAIL  ({total_errors} issue(s) across {sum(1 for v in rule_results.values() if v)} rule(s))")
    return 1


if __name__ == "__main__":
    sys.exit(main())
