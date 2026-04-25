#!/usr/bin/env python3
"""
Build the Docker Fundamentals course from Markdown source files.
Transforms source/*.md into self-contained HTML files in html/.
"""

import json
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
            raw = img_path.read_bytes()
            mime = _sniff_image_mime(raw, img_path.suffix)
            b64 = base64.b64encode(raw).decode()
            return full_tag.replace(src, f"data:{mime};base64,{b64}")

        return full_tag

    return re.sub(r'<img[^>]+src="([^"]+)"', replace_img, html_text)


def _sniff_image_mime(data: bytes, ext: str) -> str:
    """Detect image MIME from magic bytes; fall back to extension.

    Gemini-generated files often carry a `.png` extension but hold JPEG bytes.
    Trusting the extension produces broken <img> tags that browsers silently
    refuse to render. Sniff instead.
    """
    if data.startswith(b"\x89PNG\r\n\x1a\n"):
        return "image/png"
    if data[:3] == b"\xff\xd8\xff":
        return "image/jpeg"
    if data[:6] in (b"GIF87a", b"GIF89a"):
        return "image/gif"
    if data[:4] == b"RIFF" and data[8:12] == b"WEBP":
        return "image/webp"
    if data.lstrip().startswith(b"<svg") or data.lstrip().startswith(b"<?xml"):
        return "image/svg+xml"
    return {
        "png": "image/png", "jpg": "image/jpeg", "jpeg": "image/jpeg",
        "gif": "image/gif", "svg": "image/svg+xml", "webp": "image/webp",
    }.get(ext.lstrip(".").lower(), "application/octet-stream")


def embed_audio(html_text, module_name):
    """Embed narration audio as base64 into narration blocks.

    Scoped replacement: finds each <div class="narration-block"> opening,
    walks forward with balanced <div>/</div> depth tracking to locate its
    matching close, and inserts the <audio> tag immediately before that
    close. Narration blocks are paired with manifest entries by 1-based
    index in document order.

    Contrast with the earlier implementation, which ran
    `re.sub(r'(</div>\\s*</div>)', ...)` against the ENTIRE document and
    targeted the Nth match by a counter: any stray nested </div></div> pair
    in markdown-rendered HTML (callout blocks, nested content, etc.) could
    pull the audio out of a narration-block context.
    """
    module_slug = module_name.replace(".md", "")
    audio_dir = AUDIO / module_slug

    if not audio_dir.exists():
        return html_text

    manifest_path = audio_dir / "manifest.json"
    if not manifest_path.exists():
        return html_text

    import json
    manifest = json.loads(manifest_path.read_text())

    # Support both shapes:
    #   - list of entries (Docker's current manifest format)
    #   - {"entries": [...]} (legacy/alternative shape)
    if isinstance(manifest, dict):
        entries = manifest.get("entries", [])
    else:
        entries = manifest

    # Index manifest entries by 1-based `index` for O(1) lookup per block.
    by_index = {}
    for entry in entries:
        idx = entry.get("index")
        if isinstance(idx, int):
            by_index[idx] = entry

    if not by_index:
        return html_text

    open_tag = '<div class="narration-block">'
    div_open_re = re.compile(r'<div\b[^>]*>')
    div_close_re = re.compile(r'</div\s*>')

    def find_matching_close(text, start):
        """Return the index of the </div> that closes the narration-block
        opening at `start`, or -1 if unbalanced. Tracks div depth across
        arbitrary nested content (callout blocks, paragraphs, etc.).
        """
        depth = 1
        pos = start + len(open_tag)
        while pos < len(text):
            next_open = div_open_re.search(text, pos)
            next_close = div_close_re.search(text, pos)
            if not next_close:
                return -1
            if next_open and next_open.start() < next_close.start():
                depth += 1
                pos = next_open.end()
            else:
                depth -= 1
                if depth == 0:
                    return next_close.start()
                pos = next_close.end()
        return -1

    out = []
    cursor = 0
    narration_counter = 0

    while True:
        open_at = html_text.find(open_tag, cursor)
        if open_at == -1:
            out.append(html_text[cursor:])
            break

        close_at = find_matching_close(html_text, open_at)
        if close_at == -1:
            # Malformed block; bail out gracefully.
            out.append(html_text[cursor:])
            break

        narration_counter += 1
        block = html_text[open_at:close_at]
        close_tag = "</div>"

        out.append(html_text[cursor:open_at])

        entry = by_index.get(narration_counter)
        # Skip embedding if no entry, no file on disk, or audio already
        # inlined by process_narration_blocks (don't double-embed).
        should_embed = False
        audio_tag = ""
        if entry and "<audio" not in block:
            audio_filename = entry.get("audio_file") or entry.get("file", "")
            if audio_filename:
                audio_file = audio_dir / audio_filename
                if audio_file.exists():
                    b64 = base64.b64encode(audio_file.read_bytes()).decode()
                    audio_tag = (
                        '<audio controls preload="none">'
                        f'<source src="data:audio/mpeg;base64,{b64}" '
                        'type="audio/mpeg"></audio>'
                    )
                    should_embed = True

        if should_embed:
            out.append(block)
            out.append(audio_tag)
            out.append(close_tag)
        else:
            out.append(block)
            out.append(close_tag)

        cursor = close_at + len(close_tag)

    return "".join(out)


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
    """Build previous/next module navigation links.

    Returns a (prev_link, next_link) tuple of HTML <a> snippets, since the
    canonical shared template uses separate {{PREV_LINK}} and {{NEXT_LINK}}
    placeholders rather than a single combined nav block.
    """
    all_modules = ALL_MODULES

    if module_idx > 0:
        prev_mod = all_modules[module_idx - 1]
        prev_file = prev_mod["file"].replace(".md", ".html")
        prev_link = f'<a href="{prev_file}">← {prev_mod["short"]}: {prev_mod["title"]}</a>'
    else:
        prev_link = '<a href="../index.html">← Course Home</a>'

    if module_idx < len(all_modules) - 1:
        next_mod = all_modules[module_idx + 1]
        next_file = next_mod["file"].replace(".md", ".html")
        next_link = f'<a href="{next_file}">{next_mod["short"]}: {next_mod["title"]} →</a>'
    else:
        next_link = '<a href="../index.html">Course Home →</a>'

    return prev_link, next_link


def resolve_quiz_json(source_filename: str) -> Path | None:
    """Given 'module-00-what-is-docker.md', return the matching quiz JSON path
    at Quiz/Day_{N+1:02d}_Quiz_File/day_{N+1:02d}_quiz.json if it exists.

    Docker_Fundamentals uses `module-XX` source naming but `Day_YY` quiz
    folders, where YY = XX + 1 (module-00 -> Day_01, module-09 -> Day_10).
    """
    m = re.match(r"module-(\d+)-", source_filename)
    if not m:
        return None
    num = int(m.group(1)) + 1
    path = QUIZ_DIR / f"Day_{num:02d}_Quiz_File" / f"day_{num:02d}_quiz.json"
    return path if path.exists() else None


def build_quiz_page_html() -> str:
    """HTML scaffold for the injected Day Quiz page. Populated at runtime
    by initQuiz() in module_template.html.
    """
    return (
        '<div class="page-section" data-quiz-page="1">'
        '<h2 id="day-quiz">📝 Day Quiz</h2>'
        '<p class="quiz-intro">Test what you learned. 45 seconds per question. '
        'Your best attempt is saved in your browser so you can track progress '
        '-- nothing is sent to a server.</p>'
        '<div id="quiz-mount"></div>'
        '</div>'
    )


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

    # Paginate at H2 boundaries
    paginated_html, num_pages = paginate(body_html)

    # Build TOC
    toc = build_toc(body_html, num_pages)

    # Inject the Day Quiz as the final page (if a quiz JSON exists).
    # The quiz runner at window load reads <script id="quiz-data"> and mounts
    # into <div id="quiz-mount">. No further changes to TOC -- the quiz is
    # reached via the Next-Page control rather than the sidebar TOC.
    quiz_data_script = ""
    quiz_json_path = resolve_quiz_json(module_info["file"])
    if quiz_json_path:
        quiz_page = build_quiz_page_html()
        # Renumber the injected page as one past the last existing page.
        quiz_page = quiz_page.replace(
            'data-quiz-page="1"',
            f'data-page="{num_pages}"'
        )
        paginated_html += "\n" + quiz_page
        num_pages += 1
        quiz_json_text = quiz_json_path.read_text(encoding="utf-8")
        quiz_data_script = (
            '\n<script type="application/json" id="quiz-data">\n'
            f'{quiz_json_text}\n'
            '</script>\n'
        )

    # Append the quiz data script after the paginated content; the runtime
    # reads it at window load. Stored as a template-level append so it ends
    # up inside <main> but outside of any .page-section wrapper.
    paginated_html += quiz_data_script

    # Build module navigation (split into prev/next for canonical template)
    prev_link, next_link = build_module_nav(module_idx)

    # Extract title from H1 (used as fallback if module_info short/title aren't combined)
    h1_match = re.search(r'<h1[^>]*>(.*?)</h1>', body_html)
    h1_title = re.sub(r'<[^>]+>', '', h1_match.group(1)) if h1_match else module_info["title"]

    # Canonical shared template uses {{TITLE}} for the document <title>.
    # Combine the module short label and title to preserve the previous
    # "Module 3: Container Management" display, falling back to the H1.
    page_title = f'{module_info["short"]}: {module_info["title"]}' if module_info.get("short") else h1_title

    # Fill template -- canonical scheme: {{TITLE}}, {{TOC}}, {{BODY}},
    # {{PREV_LINK}}, {{NEXT_LINK}}.
    output = template
    output = output.replace("{{TITLE}}", page_title)
    output = output.replace("{{TOC}}", toc)
    output = output.replace("{{BODY}}", paginated_html)
    output = output.replace("{{PREV_LINK}}", prev_link)
    output = output.replace("{{NEXT_LINK}}", next_link)

    # Write output
    out_file = HTML_OUT / module_info["file"].replace(".md", ".html")
    out_file.write_text(output)
    print(f"    ✓ {out_file.name} ({num_pages} pages)")


def build_index(template_unused=None):
    """Generate the landing page."""
    print("  Building index.html...")

    # Build a {slug: passing_score} map by reading each module's quiz JSON.
    # Consumed by the landing-page JS to determine pass/fail per module.
    quiz_passing = {}
    for mod in MODULES:
        slug = mod['file'].replace('.md', '')
        qpath = resolve_quiz_json(mod['file'])
        if qpath:
            try:
                with open(qpath) as qf:
                    qdata = json.load(qf)
                if isinstance(qdata.get("passing_score"), (int, float)):
                    quiz_passing[slug] = qdata["passing_score"]
            except Exception:
                pass
    quiz_passing_json = json.dumps(quiz_passing)

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
<link rel="icon" type="image/png" href="favicon.png">
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

  // Update quiz badges from per-module localStorage keys written by
  // the new quiz runtime:
  //   docker_quiz_<slug>_best ("score/total")
  //   docker_quiz_<slug>_attempts (int)
  //   docker_quiz_<slug>_last (YYYY-MM-DD)
  var QUIZ_PASSING = {quiz_passing_json};
  try {{
    document.querySelectorAll('.module-card[data-module-slug]').forEach(function(card) {{
      var slug = card.dataset.moduleSlug;
      var badge = card.querySelector('[data-quiz-badge]');
      var scoreLine = card.querySelector('[data-quiz-score]');
      if (!badge) return;
      var bestRaw = localStorage.getItem('docker_quiz_' + slug + '_best');
      var attempts = parseInt(localStorage.getItem('docker_quiz_' + slug + '_attempts') || '0', 10);
      var last = localStorage.getItem('docker_quiz_' + slug + '_last') || '';
      if (!bestRaw) return;
      var parts = bestRaw.split('/');
      var score = parseInt(parts[0], 10);
      var total = parseInt(parts[1], 10);
      var passing = QUIZ_PASSING[slug];
      var passed = (typeof passing === 'number') ? (score >= passing) : null;
      if (passed === true) {{
        badge.className = 'quiz-badge passed';
        badge.textContent = 'Passed';
      }} else if (passed === false) {{
        badge.className = 'quiz-badge failed';
        badge.textContent = 'Retry';
      }} else {{
        badge.className = 'quiz-badge failed';
        badge.textContent = 'Attempted';
      }}
      if (scoreLine) {{
        var pct = total ? Math.round(score/total*100) : 0;
        var line = score + '/' + total + ' (' + pct + '%)';
        if (attempts) line += ' · ' + attempts + ' attempt' + (attempts === 1 ? '' : 's');
        if (last) line += ' · ' + last;
        scoreLine.textContent = line;
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
