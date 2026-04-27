---
description: Build this course end-to-end (markdown -> HTML)
---

Run this course's `scripts/build_course.py` to regenerate every HTML page from the markdown sources. Embeds images and audio from `images/` and `audio/`.

```bash
uv run --with markdown --with pygments python scripts/build_course.py
```

After the build, briefly summarize what was generated (number of HTML pages, the index page) and note any sources skipped due to missing images, missing audio, or missing quiz JSON. Do not run `generate_images.py` or `generate_narration.py` — those have direct API costs and require explicit instructions from Gregg.

If the user passes a module short-name as the argument (e.g. `module-04-hooks`), pass it through:

```bash
uv run --with markdown --with pygments python scripts/build_course.py --module <arg>
```

When the build completes, optionally run `python scripts/status.py` to confirm the new HTML count.
