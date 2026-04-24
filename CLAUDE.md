# Docker Fundamentals

A 10-day Docker course covering containers, images, Dockerfiles, volumes, networking, Compose, and registries.

## Course Details

- **10 days** of content with source markdown, assignments, and quizzes
- Source files: `source/module-01-what-is-docker.md` through `source/module-10-docker-hub-and-registries.md`
- Day folders: `Day_01_What_Is_Docker/` through `Day_10_Docker_Hub_and_Registries/`

## Build Pipeline

See `COURSE-BUILDER-GUIDE.md` for the full build pipeline documentation.

```bash
uv run --with markdown --with pygments python scripts/build_course.py
uv run --with elevenlabs python scripts/generate_narration.py
uv run --with markdown --with pygments python scripts/deploy.py --version 1.0
```

## Quizzes

10 quizzes in `Quiz/Day_01_Quiz_File/` through `Quiz/Day_10_Quiz_File/`. Run from the parent directory:

```bash
python ../quiz_app.py Docker_Fundamentals <day>
```

Results tracked in `Gradebook.md`.

## Content Scope

Days 1-10 cover: what is Docker, images/containers, container management, Dockerfiles (parts 1-2), volumes/persistence, networking, Docker Compose (parts 1-2), and Docker Hub/registries.
