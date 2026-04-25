# Docker Fundamentals

A free, self-paced course for developers new to containers — ten focused days that take you from "what is a container?" to "I can ship a multi-service app with Docker Compose and publish images to a registry."

**Live URL:** **<https://beekeeper-lab.github.io/docker-fundamentals/>**

![Docker delivers applications in containers](images/module-00/hero-docker-world.png)

---

This repository serves two audiences. Pick whichever describes you, or skim both — they're written to work together.

- **If you want to take the course**, start at the live URL above. Everything below is optional.
- **If you want to build a course like this**, most of this README is for you. The pipeline that produced the course — illustrations, narration, HTML, quizzes — is entirely here in the repo, documented and reproducible.

---

## Table of contents

- [Take the course](#take-the-course)
- [What's in this repo](#whats-in-this-repo)
- [How this course was built (the pipeline)](#how-this-course-was-built-the-pipeline)
  - [1. Content authored in markdown](#1-content-authored-in-markdown)
  - [2. Illustration generation via Gemini](#2-illustration-generation-via-gemini)
  - [3. Narration generation via ElevenLabs](#3-narration-generation-via-elevenlabs)
  - [4. HTML build and deploy](#4-html-build-and-deploy)
  - [5. Quizzes](#5-quizzes)
- [Running the pipeline locally](#running-the-pipeline-locally)
- [Repository map](#repository-map)
- [Design philosophy worth stealing](#design-philosophy-worth-stealing)
- [Status and maintenance](#status-and-maintenance)
- [Credits](#credits)

---

## Take the course

**Live URL:** **<https://beekeeper-lab.github.io/docker-fundamentals/>**

Ten days (modules 0 through 9), each a single illustrated, narrated HTML page with an end-of-day 25-question quiz (80% to pass). No login, no sign-up, no tracking — your progress checkmarks and quiz scores live privately in your browser's `localStorage`.

**Who this is for.** Developers new to containers. If you've installed software, written a small web app, or used the command line, you have everything you need. The course assumes no prior Docker, no Linux internals, and no DevOps background.

**What you'll learn.** Day 1 — what containers are and why they're not VMs. Day 2 — images vs containers, the Docker Hub pull cycle. Day 3 — managing the container lifecycle (run, exec, logs, stop, rm). Days 4-5 — writing Dockerfiles, layers, multi-stage builds, image-size discipline. Day 6 — volumes and bind mounts for persistence. Day 7 — networking and port mapping across containers. Days 8-9 — Docker Compose for multi-service stacks. Day 10 — Docker Hub, tagging, and pushing your own images to a registry.

**How long it takes.** Roughly 10 days at one module per day, or about 8-12 hours of self-paced reading + listening if you marathon it. Each module is sized for a single working session.

**Prefer offline?** Each release also ships as a self-contained zip in [`dist/`](dist/). Unzip and open `index.html` in any browser — narration and illustrations are bundled.

---

## What's in this repo

Source of truth for the course plus every tool that produces it:

```
Docker_Fundamentals/
├── source/                # Markdown source for all 10 modules
├── images/                # All 38 illustrations, organized by module
├── audio/                 # Narration MP3s (106 total) + per-module manifest.json
├── Quiz/                  # 10 quiz JSON banks (25 questions each, 80% passing)
├── Day_XX_*/              # Per-day launchers for the desktop quiz runner + assignment markdown
├── scripts/               # Build and generation scripts (see pipeline below)
├── .github/workflows/     # GitHub Pages deploy workflow
├── IMAGE-PLAN.md          # Gemini prompts for every illustration, read by generate_images.py
├── COURSE-BUILDER-GUIDE.md # Authoritative documentation for the build pipeline
├── CLAUDE.md              # Project instructions for Claude Code sessions in this repo
└── Gradebook.md           # Desktop quiz runner writes scores here
```

A small naming wrinkle to know up front: source files and image/audio folders are **zero-indexed** (`module-00` through `module-09`), while Day folders and quiz folders are **one-indexed** (`Day_01` through `Day_10`). The build script handles the offset; this is the same convention used elsewhere in the Stonewaters course portfolio.

---

## How this course was built (the pipeline)

This is the section for builders. It walks through the actual sequence that produced every page you see live.

### 1. Content authored in markdown

Everything starts in `source/*.md`. Each day is one file. Pages are separated by `## ` headings; the HTML builder paginates automatically.

A typical module file contains:

- **Inline illustrations** — `![alt](../images/module-XX/name.png)` + a caption on the next line.
- **Narration blocks** — `> 🎙️ Docker is a platform for running applications...` blockquotes are picked up by the narration pipeline and spoken aloud on the page.
- **Teaching-intent and key-takeaway callouts** — emoji-prefixed blockquotes that the build script renders as styled cards. See [`COURSE-BUILDER-GUIDE.md`](COURSE-BUILDER-GUIDE.md) for the full marker reference.
- **Code blocks** — fenced with language hints (` ```bash `, ` ```dockerfile `) for Pygments syntax highlighting.

### 2. Illustration generation via Gemini

All 38 illustrations are generated by **Google Gemini** (`gemini-3-pro-image-preview`, nicknamed "Nano Banana") from prompts catalogued in [`IMAGE-PLAN.md`](IMAGE-PLAN.md).

**Process:**

1. Write the image into the content file as `![alt](../images/module-XX/name.png)` — the file doesn't exist yet.
2. Add a corresponding entry in `IMAGE-PLAN.md` with the Gemini prompt (4-6 sentences describing the scene, style, palette).
3. Run `uv run --with google-genai python scripts/generate_images.py` — the script parses the plan, finds entries whose PNG doesn't yet exist, generates each via Gemini, and writes it to disk. The script also sniffs returned image MIME types so it doesn't accidentally save a JPEG with a `.png` extension.
4. Rebuild the course; `build_course.py` inlines every PNG as a base64 data URI so the distribution zip is fully offline-capable.

The IMAGE-PLAN doubles as documentation: every image has a canonical prompt that can be re-generated, tweaked, or restyled.

### 3. Narration generation via ElevenLabs

Every `> 🎙️ ...` block in source markdown becomes an MP3 file, spoken by the **ElevenLabs** Rachel voice. There are 106 MP3s across the 10 modules.

**Process:**

1. Author narration inline in the markdown, one `> 🎙️` block per teaching beat (typically 2-4 sentences).
2. Run `uv run --with elevenlabs python scripts/generate_narration.py` — the script parses every source file's narration blocks, numbers them by position, and generates MP3s into `audio/<module-slug>/NN_<module-slug>.mp3`.
3. Each module has an `audio/<module-slug>/manifest.json` recording which text each MP3 corresponds to. The script supports `--regenerate-changed` to detect drift between text and audio.

**Important behavior:** because narrations are numbered by position, **inserting a narration mid-file shifts every subsequent narration's index**, which triggers cascade re-records. Plan edits accordingly.

**Browser audio playback works.** The build's audio embed regex is scoped so the narration player markup survives the markdown→HTML pass intact. If you fork this template and audio stops working in the browser, that regex is the first place to look.

### 4. HTML build and deploy

`scripts/build_course.py` renders every source markdown file into an HTML page using `scripts/module_template.html`. Outputs go to `html/` plus `index.html` at the repo root.

What the build does:

- Markdown → HTML via Python-Markdown + Pygments for code highlighting.
- Paginates each module at every `## ` heading.
- Embeds every image as a base64 data URI.
- Processes custom blocks: narration players (with hush toggle + autoplay + "click to start" fallback), teaching-intent cards, key-takeaway banners.
- Renders a sidebar header on every page with **Course Home**, a **hush** (mute-narration) toggle, and a **theme** (light/dark) toggle — the same chrome used by Agentic Engineering 101.
- Injects a Day Quiz page per module (second-to-last, before Up Next) with the matching quiz JSON embedded inline as `docker_quiz_<NN>` data.

**Deployment** is via [`.github/workflows/pages.yml`](.github/workflows/pages.yml). Every push to `main` triggers a GitHub Actions run that rebuilds the course and publishes to GitHub Pages. Cost: $0 on public repos.

For offline distribution, `scripts/deploy.py` produces a self-contained zip that includes `index.html`, all `html/`, and referenced media.

### 5. Quizzes

Two runners, one set of questions. Both read the same JSON banks at `Quiz/Day_XX_Quiz_File/day_XX_quiz.json` (10 files, 25 questions each, 80% passing — 20 of 25).

- **In-browser quiz.** Each module's built HTML has an embedded `<script type="application/json" id="quiz-data">` block with the full quiz, plus a JS runner that paints into the Day Quiz page. Timer, shuffle, submit/timeout, review-answers summary, retake. Scores persisted in `localStorage` per day.
- **Desktop tkinter quiz.** The shared `quiz_app.py` at the portfolio root (sibling to this repo) provides a full-screen quiz window. Results write to `Gradebook.md`. Launcher scripts at `Day_XX_*/run_quiz.{py,sh,bat}` invoke it with the right arguments.

The source/quiz numbering offset (source `module-00` → quiz `Day_01`) is handled by the build script when it injects the right `day_XX_quiz.json` into each module's HTML.

---

## Running the pipeline locally

All scripts use [`uv`](https://github.com/astral-sh/uv) for dependency management — no virtualenv setup required. Commands run from the repo root.

```bash
# 1. Build the course HTML (rebuild any time source changes)
uv run --with markdown --with pygments python scripts/build_course.py

# 2. Generate any missing illustrations (skips images that already exist)
uv run --with google-genai python scripts/generate_images.py

# 3. Generate narration audio (only generates missing or changed files)
uv run --with elevenlabs python scripts/generate_narration.py

# 4. Regenerate audio for narrations whose text changed since last run
uv run --with elevenlabs python scripts/generate_narration.py --regenerate-changed

# 5. Build the distribution zip (self-contained, browser-offline)
uv run --with markdown --with pygments python scripts/deploy.py --version 1.0

# 6. Run any day's quiz in the desktop tkinter app
python Day_01_What_Is_Docker/run_quiz.py
# ...or...
python ../quiz_app.py Docker_Fundamentals 1
```

**API keys needed** (only for generation scripts, not for building or reading):

- `GEMINI_API_KEY` for image generation (read from the repo's `.env` or the parent directory's `.env` — never committed)
- `ELEVENLABS_API_KEY` for narration

Reading the course and rebuilding the HTML requires **no API keys**. All generated assets are committed, so anyone who clones the repo can build and browse immediately.

---

## Repository map

A one-screen view of what lives where:

```
.github/workflows/pages.yml    # CI: build + deploy to GitHub Pages on push
CLAUDE.md                      # Instructions for Claude Code in this repo
COURSE-BUILDER-GUIDE.md        # Full build pipeline documentation
Gradebook.md                   # Desktop quiz runner writes scores here
IMAGE-PLAN.md                  # All Gemini prompts for 38 illustrations
README.md                      # You are here
favicon.png                    # Course favicon

source/                        # Course content (markdown → HTML)
└── module-00..module-09       # 10 modules, zero-indexed

images/                        # 38 PNGs + sibling JSON metadata
│                              # subdirs: module-00..module-09
│
audio/                         # 106 MP3s + manifest.json per module
│                              # subdirs match source file slugs
│
Quiz/                          # 10 quiz JSON banks
└── Day_XX_Quiz_File/day_XX_quiz.json

Day_XX_*/                      # Per-day desktop quiz launchers + assignments
├── Assignment_XX_*.md
└── run_quiz.{py,sh,bat}

scripts/                       # Build + generation pipeline
├── build_course.py            # Markdown → HTML + index
├── deploy.py                  # Build + bundle into dist/ zip
├── generate_images.py         # IMAGE-PLAN.md + Gemini → PNGs
├── generate_narration.py      # 🎙️ blocks + ElevenLabs → MP3s
└── module_template.html       # HTML shell with runtime JS/CSS
```

---

## Design philosophy worth stealing

Short version of choices that paid off here and across the portfolio:

1. **Everything is markdown, including the thing that generates the HTML.** One source of truth. Narrators, illustrators, and the HTML builder all read the same files.
2. **Every asset has a plan.** Illustrations are catalogued in `IMAGE-PLAN.md` with the exact Gemini prompt; narrations live in `🎙️` blocks inside the prose. Re-generating, tweaking, or re-voicing any asset is deterministic.
3. **One runner, many courses.** The quiz runner at the portfolio root is shared — Docker Fundamentals uses the day-based default; Agentic Engineering 101 passes `--unit module`. One bug fix, eight courses benefit.
4. **Graceful degradation for every runtime feature.** Narration auto-plays by default but shows a click-to-start banner when browsers block autoplay. Images are base64-embedded so the zip works offline. Quizzes persist to `localStorage` because there's no backend and that's fine.

For the long version, see Agentic Engineering 101's README — the same design principles guide both courses.

---

## Status and maintenance

**Shipped.** Ten modules, 38 illustrations, 106 narrations, 10 quizzes, all built and deployed. Hosting is free (GitHub Pages on a public repo).

The course covers Docker fundamentals as of 2026 and is expected to stay stable — Docker's CLI surface and Compose v2 file format have been steady for several years. Updates will mostly track Docker Engine releases and Docker Hub policy changes.

---

## Credits

Illustrations generated via **Google Gemini** (`gemini-3-pro-image-preview`). Narrations generated via **ElevenLabs** (Rachel voice). Built and maintained as part of the **Stonewaters Consulting** internship curriculum portfolio.

**Questions, issues, pull requests** → use the GitHub Issues and Pull Requests tabs of this repo. The repo is public; contributions are welcome.
