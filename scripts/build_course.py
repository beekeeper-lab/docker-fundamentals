#!/usr/bin/env python3
"""
Build the Docker Fundamentals course from Markdown source files.
Transforms source/*.md into self-contained HTML files in html/.
"""

import os
import re
import sys
import base64
import html as html_mod
from pathlib import Path

import markdown
from markdown.extensions.fenced_code import FencedCodeExtension
from markdown.extensions.codehilite import CodeHiliteExtension
from markdown.extensions.tables import TableExtension
from markdown.extensions.toc import TocExtension
from markdown.extensions.md_in_html import MarkdownInHtmlExtension

# ── Project paths ──────────────────────────────────────────────────────
ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT / "source"
IMAGES = ROOT / "images"
AUDIO = ROOT / "audio"
HTML_OUT = ROOT / "html"
QUIZ_DIR = ROOT / "Quiz"
TEMPLATE_PATH = Path(__file__).resolve().parent / "module_template.html"

# ── Module registry ────────────────────────────────────────────────────
MODULES = [
    {
        "file": "module-00-what-is-docker.md",
        "short": "Module 1",
        "title": "What Is Docker",
        "tier": "Start Here",
        "tier_css": "tier-start-here",
    },
    {
        "file": "module-01-images-and-containers.md",
        "short": "Module 2",
        "title": "Images and Containers",
        "tier": "Start Here",
        "tier_css": "tier-start-here",
    },
    {
        "file": "module-02-container-management.md",
        "short": "Module 3",
        "title": "Container Management",
        "tier": "Start Here",
        "tier_css": "tier-start-here",
    },
    {
        "file": "module-03-dockerfiles-part-1.md",
        "short": "Module 4",
        "title": "Dockerfiles Part 1",
        "tier": "Useful Soon",
        "tier_css": "tier-useful-soon",
    },
    {
        "file": "module-04-dockerfiles-part-2.md",
        "short": "Module 5",
        "title": "Dockerfiles Part 2",
        "tier": "Useful Soon",
        "tier_css": "tier-useful-soon",
    },
    {
        "file": "module-05-volumes-and-persistence.md",
        "short": "Module 6",
        "title": "Volumes and Persistence",
        "tier": "Useful Soon",
        "tier_css": "tier-useful-soon",
    },
    {
        "file": "module-06-networking.md",
        "short": "Module 7",
        "title": "Networking",
        "tier": "When You're Ready",
        "tier_css": "tier-when-youre-ready",
    },
    {
        "file": "module-07-docker-compose-part-1.md",
        "short": "Module 8",
        "title": "Docker Compose Part 1",
        "tier": "When You're Ready",
        "tier_css": "tier-when-youre-ready",
    },
    {
        "file": "module-08-docker-compose-part-2.md",
        "short": "Module 9",
        "title": "Docker Compose Part 2",
        "tier": "When You're Ready",
        "tier_css": "tier-when-youre-ready",
    },
    {
        "file": "module-09-docker-hub-and-registries.md",
        "short": "Module 10",
        "title": "Docker Hub and Registries",
        "tier": "Advanced",
        "tier_css": "tier-advanced",
    },
]

EXTRAS = []
REFERENCES = []

ALL_MODULES = MODULES + EXTRAS + REFERENCES


def read_template():
    return TEMPLATE_PATH.read_text()


def md_to_html(md_text):
    """Convert markdown text to HTML."""
    extensions = [
        FencedCodeExtension(),
        CodeHiliteExtension(css_class="highlight", guess_lang=False, use_pygments=True),
        TableExtension(),
        TocExtension(toc_depth="2-3"),
        MarkdownInHtmlExtension(),
    ]
    md = markdown.Markdown(extensions=extensions)
    body = md.convert(md_text)
    toc = md.toc
    return body, toc


def process_tier_badges(html_text):
    """Convert tier markers into styled badge elements."""
    tier_classes = {
        "Start Here": "tier-start-here",
        "Useful Soon": "tier-useful-soon",
        "When You're Ready": "tier-when-youre-ready",
        "Advanced": "tier-advanced",
    }

    def replace_tier(m):
        content = m.group(1)
        text = re.sub(r'🏷️\s*', '', content).strip()
        tier_name = text.split('.')[0].split(':')[0].strip()
        css_class = tier_classes.get(tier_name, "tier-start-here")
        return f'<div class="tier-badge {css_class}">{tier_name}</div>'

    html_text = re.sub(
        r'<blockquote>\s*(?:<p>)*(🏷️.*?)(?:</p>)*\s*</blockquote>',
        replace_tier, html_text, flags=re.DOTALL,
    )
    html_text = re.sub(
        r'<p>(🏷️.*?)</p>',
        replace_tier, html_text, flags=re.DOTALL,
    )
    return html_text


def process_cycle_blocks(html_text):
    """Convert cycle anchor blockquotes (🔄) into styled blocks."""
    def replace_anchor(m):
        content = m.group(1)
        display_text = re.sub(r'🔄\s*', '', content)
        if not display_text.strip().startswith('<'):
            display_text = f'<p>{display_text.strip()}</p>'
        return f'<div class="cycle-block"><div class="cycle-icon">🔄</div><div>{display_text}</div></div>'

    html_text = re.sub(
        r'<blockquote>\s*((?:<p>)*🔄.*?)\s*</blockquote>',
        replace_anchor, html_text, flags=re.DOTALL,
    )
    html_text = re.sub(
        r'<p>(🔄.*?)</p>',
        replace_anchor, html_text, flags=re.DOTALL,
    )
    return html_text


def process_callout_blocks(html_text):
    """Convert key takeaway callouts (💡) into styled blocks."""
    def replace_callout(m):
        content = m.group(1)
        display_text = re.sub(r'💡\s*', '', content)
        if not display_text.strip().startswith('<'):
            display_text = f'<p>{display_text.strip()}</p>'
        return f'<div class="callout-block"><div class="callout-icon">💡</div><div>{display_text}</div></div>'

    html_text = re.sub(
        r'<blockquote>\s*((?:<p>)*💡.*?)\s*</blockquote>',
        replace_callout, html_text, flags=re.DOTALL,
    )
    html_text = re.sub(
        r'<p>(💡.*?)</p>',
        replace_callout, html_text, flags=re.DOTALL,
    )
    return html_text


def process_teach_blocks(html_text):
    """Convert teaching intent blockquotes (🎯) into styled blocks."""
    def replace_teach(m):
        content = m.group(1)
        display_text = re.sub(r'🎯\s*', '', content)
        if not display_text.strip().startswith('<'):
            display_text = f'<p>{display_text.strip()}</p>'
        return f'<div class="teach-block"><div class="teach-icon">🎯</div><div>{display_text}</div></div>'

    html_text = re.sub(
        r'<blockquote>\s*((?:<p>)*🎯.*?)\s*</blockquote>',
        replace_teach, html_text, flags=re.DOTALL,
    )
    html_text = re.sub(
        r'<p>(🎯.*?)</p>',
        replace_teach, html_text, flags=re.DOTALL,
    )
    return html_text


def process_narration_blocks(html_text, module_stem):
    """Convert narration blockquotes (🎙️) into audio player widgets."""
    audio_module_dir = AUDIO / module_stem

    # Load manifest if it exists
    manifest_path = audio_module_dir / "manifest.json"
    audio_files = {}
    if manifest_path.exists():
        import json
        manifest = json.loads(manifest_path.read_text())
        for entry in manifest:
            audio_files[entry["index"]] = entry

    narration_counter = 0

    def replace_narration(m):
        nonlocal narration_counter
        narration_counter += 1
        content = m.group(1)

        # Remove the 🎙️ emoji and clean up for display
        display_text = re.sub(r'🎙️\s*', '', content)
        if not display_text.strip().startswith('<p>'):
            display_text = f'<p>{display_text.strip()}</p>'

        # Check for audio file
        audio_entry = audio_files.get(narration_counter)
        audio_html = ""
        if audio_entry:
            audio_path = audio_module_dir / audio_entry["audio_file"]
            if audio_path.exists():
                audio_b64 = base64.b64encode(audio_path.read_bytes()).decode()
                audio_html = f'''
                <button class="narration-play" onclick="playNarration(this)" aria-label="Play narration">
                    <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
                        <path d="M8 5v14l11-7z"/>
                    </svg>
                </button>
                <audio preload="none">
                    <source src="data:audio/mpeg;base64,{audio_b64}" type="audio/mpeg">
                </audio>'''

        return f'''<div class="narration-block">
            <div class="narration-icon">🎙️</div>
            <div class="narration-content">{display_text}</div>
            {audio_html}
        </div>'''

    # Match blockquotes containing 🎙️ (handles multi-paragraph blockquotes)
    html_text = re.sub(
        r'<blockquote>\s*((?:<p>)*🎙️.*?)\s*</blockquote>',
        replace_narration,
        html_text,
        flags=re.DOTALL,
    )

    # Also match plain <p>🎙️ paragraphs (narrations not in blockquotes)
    html_text = re.sub(
        r'<p>(🎙️.*?)</p>',
        replace_narration,
        html_text,
        flags=re.DOTALL,
    )

    return html_text


MARKER_EMOJI_RE = re.compile(r'[\U0001F3F7]\uFE0F|[\U0001F3AF]|[\U0001F399]\uFE0F|[\U0001F504]|[\U0001F4A1]')


def split_merged_blockquotes(html_text):
    """Split merged blockquotes that contain multiple emoji-marked paragraphs.

    Python-Markdown merges adjacent > blockquotes into a single <blockquote>
    with multiple <p> children. This breaks the per-block emoji processors,
    so we split them back out into individual <blockquote> elements.
    """

    def splitter(m):
        inner = m.group(1)
        # Split on paragraph boundaries
        paragraphs = re.split(r'</p>\s*<p>', inner)
        if len(paragraphs) <= 1:
            return m.group(0)

        # Check if any paragraph contains a marker emoji
        has_marker = any(MARKER_EMOJI_RE.search(p) for p in paragraphs)
        if not has_marker:
            return m.group(0)

        # Rewrap each paragraph in its own blockquote
        result = []
        for p in paragraphs:
            p = p.strip()
            # Ensure proper <p> wrapping
            if not p.startswith('<p>'):
                p = '<p>' + p
            if not p.endswith('</p>'):
                p = p + '</p>'
            result.append(f'<blockquote>\n{p}\n</blockquote>')
        return '\n'.join(result)

    return re.sub(
        r'<blockquote>\s*(.*?)\s*</blockquote>',
        splitter,
        html_text,
        flags=re.DOTALL,
    )


def process_special_blocks(html_text, module_stem=""):
    """Transform emoji-prefixed blockquotes into styled components."""
    html_text = split_merged_blockquotes(html_text)
    html_text = process_tier_badges(html_text)
    html_text = process_cycle_blocks(html_text)
    html_text = process_callout_blocks(html_text)
    html_text = process_teach_blocks(html_text)
    html_text = process_narration_blocks(html_text, module_stem)
    return html_text


def embed_images(html_text, module_name):
    """Replace image src paths with base64 data URIs."""

    def replace_img(m):
        full_tag = m.group(0)
        src = m.group(1)

        # Resolve path relative to images/
        if src.startswith("../images/"):
            img_path = IMAGES / src[len("../images/"):]
        elif src.startswith("images/"):
            img_path = IMAGES / src[len("images/"):]
        else:
            img_path = ROOT / src

        if img_path.exists():
            ext = img_path.suffix.lower()
            mime = {
                ".png": "image/png",
                ".jpg": "image/jpeg",
                ".jpeg": "image/jpeg",
                ".gif": "image/gif",
                ".svg": "image/svg+xml",
                ".webp": "image/webp",
            }.get(ext, "image/png")

            b64 = base64.b64encode(img_path.read_bytes()).decode()
            return full_tag.replace(src, f"data:{mime};base64,{b64}")

        return full_tag

    return re.sub(r'<img[^>]+src="([^"]+)"', replace_img, html_text)


def embed_audio(html_text, module_name):
    """Embed narration audio as base64 into narration blocks."""
    # Look for audio files for this module
    module_slug = module_name.replace(".md", "")
    audio_dir = AUDIO / module_slug

    if not audio_dir.exists():
        return html_text

    # Check for manifest
    manifest_path = audio_dir / "manifest.json"
    if not manifest_path.exists():
        return html_text

    import json
    manifest = json.loads(manifest_path.read_text())

    # For each narration block, try to find matching audio
    narration_blocks = re.findall(r'<div class="narration-block">', html_text)

    for i, entry in enumerate(manifest.get("entries", [])):
        audio_file = audio_dir / entry.get("file", "")
        if audio_file.exists():
            b64 = base64.b64encode(audio_file.read_bytes()).decode()
            audio_tag = f'<audio controls preload="none"><source src="data:audio/mpeg;base64,{b64}" type="audio/mpeg"></audio>'

            # Insert audio tag into the i-th narration block
            count = 0
            def insert_audio(m):
                nonlocal count
                if count == i:
                    count += 1
                    return m.group(0) + audio_tag
                count += 1
                return m.group(0)

            html_text = re.sub(
                r'(</div>\s*</div>)',
                insert_audio,
                html_text,
            )

    return html_text


def paginate(html_text):
    """Split HTML at H2 boundaries into page sections."""
    # Split on <h2> tags
    parts = re.split(r'(?=<h2[^>]*>)', html_text)
    pages = []

    for part in parts:
        part = part.strip()
        if part:
            pages.append(part)

    if not pages:
        pages = [html_text]

    sections = []
    for i, page in enumerate(pages):
        sections.append(f'<div class="page-section" data-page="{i}">{page}</div>')

    return "\n".join(sections), len(sections)


def build_toc(html_text, num_pages):
    """Build sidebar TOC from H2 and H3 headings, grouped by page."""
    groups = []  # list of (page_idx, h2_title, [h3_titles])
    page_idx = -1

    for line in html_text.split("\n"):
        h2_match = re.search(r'<h2[^>]*>(.*?)</h2>', line)
        h3_match = re.search(r'<h3[^>]*>(.*?)</h3>', line)

        if h2_match:
            page_idx += 1
            title = re.sub(r'<[^>]+>', '', h2_match.group(1))
            groups.append((page_idx, title, []))
        elif h3_match and page_idx >= 0 and groups:
            title = re.sub(r'<[^>]+>', '', h3_match.group(1))
            groups[-1][2].append(title)

    toc_html = []
    for page_num, h2_title, h3_titles in groups:
        toc_html.append(f'<li class="toc-page-group" data-toc-page="{page_num}">')
        toc_html.append(f'  <a href="#" data-page="{page_num}" class="toc-h2-link">{h2_title}</a>')
        if h3_titles:
            toc_html.append('  <ul class="toc-subsections">')
            for h3 in h3_titles:
                toc_html.append(f'    <li><a href="#" data-page="{page_num}" class="toc-h3-link">{h3}</a></li>')
            toc_html.append('  </ul>')
        toc_html.append('</li>')

    return "\n".join(toc_html)


def build_module_nav(module_idx):
    """Build previous/next module navigation links."""
    all_modules = ALL_MODULES
    parts = []

    if module_idx > 0:
        prev_mod = all_modules[module_idx - 1]
        prev_file = prev_mod["file"].replace(".md", ".html")
        parts.append(f'<a href="{prev_file}">← {prev_mod["short"]}: {prev_mod["title"]}</a>')
    else:
        parts.append('<a href="../index.html">← Course Home</a>')

    if module_idx < len(all_modules) - 1:
        next_mod = all_modules[module_idx + 1]
        next_file = next_mod["file"].replace(".md", ".html")
        parts.append(f'<a href="{next_file}">{next_mod["short"]}: {next_mod["title"]} →</a>')
    else:
        parts.append('<a href="../index.html">Course Home →</a>')

    return "\n".join(parts)


def generate_quiz_html(module_num, module_slug):
    """Generate interactive quiz HTML from quiz JSON file."""
    import json as json_mod
    quiz_dir = QUIZ_DIR / f"Day_{module_num + 1:02d}_Quiz_File"
    quiz_file = quiz_dir / f"day_{module_num + 1:02d}_quiz.json"

    if not quiz_file.exists():
        return ""

    quiz_data = json_mod.loads(quiz_file.read_text())
    title = quiz_data.get("quiz_title", f"Module {module_num + 1} Quiz")
    passing = quiz_data.get("passing_score", 20)
    total = quiz_data.get("total_questions", 25)
    questions = quiz_data.get("questions", [])

    if not questions:
        return ""

    quiz_json = json_mod.dumps({
        "moduleSlug": module_slug,
        "passingScore": passing,
        "totalQuestions": total,
    })

    questions_html = []
    for q in questions:
        qid = q["id"]
        opts = ""
        for opt in q["options"]:
            opts += f'''<label>
              <input type="radio" name="q{qid}" value="{html_mod.escape(opt)}">
              <span>{html_mod.escape(opt)}</span>
            </label>\n'''

        questions_html.append(f'''<div class="quiz-question" data-answer="{html_mod.escape(q['answer'])}">
          <div class="quiz-question-number">Question {qid}</div>
          <div class="quiz-question-text">{html_mod.escape(q['question'])}</div>
          <div class="quiz-options">{opts}</div>
          <div class="quiz-feedback"></div>
        </div>''')

    return f'''<h2 id="quiz">Knowledge Check: {html_mod.escape(title)}</h2>
<div class="quiz-container">
  <script type="application/json" id="quizData">{quiz_json}</script>
  <form id="quizForm" onsubmit="return false;">
    {''.join(questions_html)}
    <button type="button" id="quizSubmitBtn" class="quiz-submit-btn">Submit Answers</button>
  </form>
  <div id="quizResults" class="quiz-results">
    <div id="quizScore" class="quiz-score"></div>
    <div id="quizLabel" class="quiz-label"></div>
    <div id="quizDetail" class="quiz-detail"></div>
    <button type="button" id="quizRetryBtn" class="quiz-retry-btn">Try Again</button>
  </div>
</div>'''


def build_module(module_info, module_idx, template, embed=True):
    """Build a single module HTML file."""
    source_file = SOURCE / module_info["file"]

    if not source_file.exists():
        print(f"  ⚠ Source file not found: {source_file}")
        return

    print(f"  Building {module_info['short']}: {module_info['title']}...")

    md_text = source_file.read_text()

    # Convert markdown to HTML
    body_html, toc_html = md_to_html(md_text)

    # Process special blocks (including narration with audio embedding)
    module_stem = module_info["file"].replace(".md", "")
    body_html = process_special_blocks(body_html, module_stem)

    # Embed images
    if embed:
        module_name = module_info["file"]
        body_html = embed_images(body_html, module_name)

    # Append quiz if available
    module_num_match = re.search(r'module-(\d+)', module_stem)
    if module_num_match:
        module_num = int(module_num_match.group(1))
        quiz_html = generate_quiz_html(module_num, module_stem)
        if quiz_html:
            body_html += quiz_html

    # Paginate at H2 boundaries
    paginated_html, num_pages = paginate(body_html)

    # Build TOC
    toc = build_toc(body_html, num_pages)

    # Build module navigation
    module_nav = build_module_nav(module_idx)

    # Extract title from H1
    h1_match = re.search(r'<h1[^>]*>(.*?)</h1>', body_html)
    title = re.sub(r'<[^>]+>', '', h1_match.group(1)) if h1_match else module_info["title"]

    # Fill template
    output = template
    output = output.replace("{{MODULE_TITLE}}", title)
    output = output.replace("{{MODULE_SHORT}}", module_info["short"])
    output = output.replace("{{TOC}}", toc)
    output = output.replace("{{CONTENT}}", paginated_html)
    output = output.replace("{{MODULE_NAV}}", module_nav)
    output = output.replace("{{MODULE_FILE}}", module_info["file"].replace(".md", ""))

    # Write output
    out_file = HTML_OUT / module_info["file"].replace(".md", ".html")
    out_file.write_text(output)
    print(f"    ✓ {out_file.name} ({num_pages} pages)")


def build_index(template_unused=None):
    """Generate the landing page."""
    print("  Building index.html...")

    # Group modules by tier
    tiers = {}
    for mod in MODULES:
        tier = mod["tier"]
        if tier not in tiers:
            tiers[tier] = []
        tiers[tier].append(mod)

    tier_order = ["Start Here", "Useful Soon", "When You're Ready", "Advanced"]
    tier_colors = {
        "Start Here": ("#dcfce7", "#166534"),
        "Useful Soon": ("#dbeafe", "#1e40af"),
        "When You're Ready": ("#fef3c7", "#92400e"),
        "Advanced": ("#fce7f3", "#9d174d"),
    }

    cards_html = ""
    for tier_name in tier_order:
        if tier_name not in tiers:
            continue

        bg, fg = tier_colors.get(tier_name, ("#f3f4f6", "#374151"))
        cards_html += f'<h2 style="margin-top: 2rem;">{tier_name}</h2>\n'
        cards_html += '<div class="module-grid">\n'

        for mod in tiers[tier_name]:
            html_file = f"html/{mod['file'].replace('.md', '.html')}"
            slug = mod['file'].replace('.md', '')
            cards_html += f'''<a href="{html_file}" class="module-card" data-module-slug="{slug}">
  <div class="card-badge" style="background:{bg};color:{fg}">{tier_name}</div>
  <h3>{mod["short"]}</h3>
  <p>{mod["title"]}</p>
  <span class="quiz-badge not-taken" data-quiz-badge>Quiz</span>
  <div class="quiz-score-line" data-quiz-score></div>
</a>\n'''

        cards_html += "</div>\n"

    # Build extras and references
    for section_title, section_modules in [("Extras", EXTRAS), ("References", REFERENCES)]:
        if section_modules:
            cards_html += f'<h2 style="margin-top: 2rem;">{section_title}</h2>\n'
            cards_html += '<div class="module-grid">\n'
            for mod in section_modules:
                html_file = f"html/{mod['file'].replace('.md', '.html')}"
                cards_html += f'''<a href="{html_file}" class="module-card">
  <h3>{mod["short"]}</h3>
  <p>{mod["title"]}</p>
</a>\n'''
            cards_html += "</div>\n"

    index_html = f'''<!DOCTYPE html>
<html lang="en" data-theme="light">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Docker Fundamentals</title>
<style>
:root {{
  --bg: #ffffff;
  --text: #1a1a2e;
  --card-bg: #f9fafb;
  --card-border: #e5e7eb;
  --accent: #0077b6;
  --shadow: 0 2px 8px rgba(0,0,0,0.08);
}}
[data-theme="dark"] {{
  --bg: #1a1a2e;
  --text: #e0e0e6;
  --card-bg: #16213e;
  --card-border: #2a2a4a;
  --accent: #4fc3f7;
  --shadow: 0 2px 8px rgba(0,0,0,0.3);
}}
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
body {{
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  background: var(--bg);
  color: var(--text);
  line-height: 1.6;
}}
.header {{
  text-align: center;
  padding: 3rem 2rem 2rem;
  background: linear-gradient(135deg, #0077b6, #00b4d8);
  color: white;
}}
.header h1 {{ font-size: 2.5rem; margin-bottom: 0.5rem; }}
.header p {{ font-size: 1.1rem; opacity: 0.9; }}
.container {{
  max-width: 1000px;
  margin: 0 auto;
  padding: 2rem;
}}
.module-grid {{
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 1rem;
  margin-top: 1rem;
}}
.module-card {{
  background: var(--card-bg);
  border: 1px solid var(--card-border);
  border-radius: 12px;
  padding: 1.5rem;
  text-decoration: none;
  color: var(--text);
  transition: transform 0.2s, box-shadow 0.2s;
  display: block;
}}
.module-card:hover {{
  transform: translateY(-2px);
  box-shadow: var(--shadow);
}}
.module-card h3 {{
  color: var(--accent);
  margin-bottom: 0.25rem;
  font-size: 1.1rem;
}}
.module-card p {{
  font-size: 0.95rem;
  opacity: 0.8;
}}
.card-badge {{
  display: inline-block;
  padding: 0.15rem 0.6rem;
  border-radius: 12px;
  font-size: 0.75rem;
  font-weight: 600;
  margin-bottom: 0.5rem;
}}
h2 {{
  font-size: 1.3rem;
  color: var(--accent);
}}
.controls {{
  position: fixed;
  top: 0;
  right: 0;
  padding: 0.75rem 1.5rem;
  z-index: 200;
}}
.controls button {{
  background: rgba(255,255,255,0.2);
  border: 1px solid rgba(255,255,255,0.3);
  color: white;
  padding: 0.4rem 0.8rem;
  border-radius: 6px;
  font-size: 0.82rem;
  cursor: pointer;
}}
.controls button:hover {{ background: rgba(255,255,255,0.3); }}
.quiz-badge {{
  display: inline-block;
  padding: 0.15rem 0.5rem;
  border-radius: 10px;
  font-size: 0.7rem;
  font-weight: 600;
  margin-top: 0.5rem;
}}
.quiz-badge.not-taken {{ background: #e5e7eb; color: #6b7280; }}
.quiz-badge.passed {{ background: #dcfce7; color: #166534; }}
.quiz-badge.failed {{ background: #fce7f3; color: #9d174d; }}
[data-theme="dark"] .quiz-badge.not-taken {{ background: #374151; color: #9ca3af; }}
[data-theme="dark"] .quiz-badge.passed {{ background: #14532d; color: #86efac; }}
[data-theme="dark"] .quiz-badge.failed {{ background: #500724; color: #f9a8d4; }}
.quiz-score-line {{
  font-size: 0.75rem;
  opacity: 0.7;
  margin-top: 0.25rem;
}}
</style>
</head>
<body>

<div class="controls">
  <button onclick="toggleTheme()" id="theme-btn">🌙 Dark</button>
</div>

<div class="header">
  <h1>Docker Fundamentals</h1>
  <p>A 10-module hands-on course from containers to production</p>
</div>

<div class="container">
  {cards_html}
</div>

<script>
function toggleTheme() {{
  const html = document.documentElement;
  const isDark = html.dataset.theme === 'dark';
  html.dataset.theme = isDark ? 'light' : 'dark';
  document.getElementById('theme-btn').textContent = isDark ? '🌙 Dark' : '☀️ Light';
  try {{ localStorage.setItem('docker-fund-theme', html.dataset.theme); }} catch(e) {{}}
}}
(function() {{
  try {{
    if (localStorage.getItem('docker-fund-theme') === 'dark') {{
      document.documentElement.dataset.theme = 'dark';
      document.getElementById('theme-btn').textContent = '☀️ Light';
    }}
  }} catch(e) {{}}

  // Update quiz badges from localStorage
  try {{
    var results = JSON.parse(localStorage.getItem('docker-fund-quiz-results') || '{{}}');
    document.querySelectorAll('.module-card[data-module-slug]').forEach(function(card) {{
      var slug = card.dataset.moduleSlug;
      var badge = card.querySelector('[data-quiz-badge]');
      var scoreLine = card.querySelector('[data-quiz-score]');
      if (results[slug] && badge) {{
        var r = results[slug];
        if (r.passed) {{
          badge.className = 'quiz-badge passed';
          badge.textContent = 'Passed';
        }} else {{
          badge.className = 'quiz-badge failed';
          badge.textContent = 'Retry';
        }}
        if (scoreLine) {{
          scoreLine.textContent = r.score + '/' + r.total + ' (' + Math.round(r.score/r.total*100) + '%)';
        }}
      }}
    }});
  }} catch(e) {{}}
}})();
</script>
</body>
</html>'''

    (ROOT / "index.html").write_text(index_html)
    print(f"    ✓ index.html")


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Build Docker Fundamentals course")
    parser.add_argument("--module", help="Build only this module (e.g., module-00-what-is-docker)")
    parser.add_argument("--no-embed", action="store_true", help="Don't embed images as base64")
    args = parser.parse_args()

    HTML_OUT.mkdir(exist_ok=True)
    template = read_template()
    embed = not args.no_embed

    print("Docker Fundamentals — Course Builder")
    print("=" * 50)

    if args.module:
        # Build single module
        for i, mod in enumerate(ALL_MODULES):
            if args.module in mod["file"]:
                build_module(mod, i, template, embed)
                break
        else:
            print(f"Module '{args.module}' not found")
            sys.exit(1)
    else:
        # Build all modules
        for i, mod in enumerate(ALL_MODULES):
            build_module(mod, i, template, embed)

        # Build index
        build_index()

    print("=" * 50)
    print("Done!")


if __name__ == "__main__":
    main()
