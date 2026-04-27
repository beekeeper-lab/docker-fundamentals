---
description: Report build state for this course (sources, html, images, audio, quizzes, todos)
---

Run this course's `scripts/status.py` and render a human-readable summary of the resulting JSON.

```bash
python scripts/status.py
```

The script emits a JSON object on stdout with this shape:

- `course_name`, `stage` ("post-pipeline", "pre-pipeline", or "empty")
- `sources` — `{count, files[]}`
- `html` — `{count, missing[]}` (sources whose `.html` doesn't yet exist)
- `images` — `{on_disk, planned, missing[{file, title}]}`
- `audio` — `{files, narration_blocks, missing_chars, per_module{...}}`
- `quizzes` — `{count, total_questions, modules_without[]}`
- `todos` — `len(images.missing) + max(0, narration_blocks - audio.files) + len(modules_without)`

Render the JSON as the following Markdown summary:

```
## <course-name> — <todos> to-dos
- **Stage:** <stage>
- **Sources / HTML:** <html.count> / <sources.count>  (<missing list if any>)
- **Images:** <on_disk> on disk / <planned> planned  (<missing count> missing)
- **Audio:** <audio.files> / <narration_blocks> blocks  (~<missing_chars> chars / ElevenLabs credits remaining)
- **Quizzes:** <count> files / <total_questions> questions  (<modules_without count> modules without quiz)
```

Then list (under appropriate `###` subheadings, only if non-empty):

- the first 10 entries of `images.missing` as `- file — title`
- entries in `audio.per_module` with `missing_chars > 0`, sorted by `missing_chars` descending: `- <source> — <missing> of <total> blocks (~<chars>k credits)`
- `quizzes.modules_without` as `- <source>`

Skip empty sections. Don't add commentary or "next steps" — just the summary. If the user passes a substring argument, additionally show the full per-module narration breakdown (every entry in `audio.per_module`).

The JSON contract this command depends on is documented at `docs/STATUS-CONTRACT.md`.
