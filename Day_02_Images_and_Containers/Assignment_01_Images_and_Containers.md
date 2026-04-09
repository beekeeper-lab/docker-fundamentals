# Day 2 Assignment: Images and Containers

## Overview

- **Topic:** Pulling Images, Understanding Tags, and Running Containers
- **Type:** Technical / Hands-On
- **Estimated Time:** 30 minutes

## Background

### Docker Images

An image is a layered, read-only template. Images are identified by:

```
registry/repository:tag
```

Examples:
- `nginx:latest` — Latest Nginx from Docker Hub
- `python:3.12-slim` — Python 3.12 slim variant
- `ubuntu:22.04` — Specific Ubuntu version
- `node:20-alpine` — Node.js on lightweight Alpine Linux

### Tags

Tags identify specific versions of an image:

| Tag | Meaning |
|-----|---------|
| `latest` | Default tag (not always the newest!) |
| `3.12` | Specific version |
| `3.12-slim` | Minimal variant (smaller) |
| `3.12-alpine` | Alpine Linux base (smallest) |
| `bookworm` | Debian Bookworm base |

### Image Layers

Images are built in **layers**. Each instruction in a Dockerfile creates a layer. Layers are cached and shared between images, saving disk space and download time.

---

## Part 1: Pulling Images

### Task A: Pull Different Image Variants

```bash
docker pull python:3.12
docker pull python:3.12-slim
docker pull python:3.12-alpine
```

Compare their sizes:

```bash
docker images | grep python
```

You'll see a dramatic size difference:
- `python:3.12` — ~1 GB (full Debian with build tools)
- `python:3.12-slim` — ~150 MB (Debian without extras)
- `python:3.12-alpine` — ~50 MB (Alpine Linux, minimal)

### Task B: Inspect an Image

```bash
docker inspect python:3.12-slim
```

This shows detailed metadata: layers, environment variables, entry point, and more.

Try a focused query:

```bash
docker inspect --format='{{.Config.Env}}' python:3.12-slim
docker inspect --format='{{.Size}}' python:3.12-slim
```

---

## Part 2: Running Containers from Different Images

### Task C: Run Python in a Container

```bash
docker run -it python:3.12-slim python3
```

You're in a Python REPL inside a container:

```python
>>> import sys
>>> print(sys.version)
>>> print("Hello from Docker!")
>>> exit()
```

Run a one-liner without entering interactive mode:

```bash
docker run python:3.12-slim python3 -c "print('Hello from Docker!')"
```

### Task D: Run Node.js

```bash
docker pull node:20-alpine
docker run node:20-alpine node -e "console.log('Hello from Node.js in Docker!')"
```

### Task E: Run Multiple Versions Side by Side

This is one of Docker's superpowers — run different versions simultaneously:

```bash
docker run python:3.12-slim python3 -c "import sys; print(f'Python {sys.version}')"
docker pull python:3.11-slim
docker run python:3.11-slim python3 -c "import sys; print(f'Python {sys.version}')"
```

Two different Python versions, no conflicts, no installing anything on your system.

---

## Part 3: Container Naming and Listing

### Task F: Named Containers

```bash
docker run -d --name web-server nginx
docker run -d --name api-server python:3.12-slim python3 -m http.server 8000
```

List running containers:

```bash
docker ps
```

Names make containers easy to reference:

```bash
docker logs web-server
docker logs api-server
```

### Task G: Container Details

```bash
docker inspect web-server --format='{{.NetworkSettings.IPAddress}}'
docker stats --no-stream
```

`docker stats` shows real-time CPU, memory, and network usage for all running containers.

### Task H: Clean Up

```bash
docker stop web-server api-server
docker rm web-server api-server
```

---

## Part 4: Running Containers with Options

### Task I: Environment Variables

Pass environment variables into a container:

```bash
docker run -e MY_NAME="Campbell" -e MY_ROLE="Intern" python:3.12-slim \
    python3 -c "import os; print(f'{os.environ[\"MY_NAME\"]} is a {os.environ[\"MY_ROLE\"]}')"
```

### Task J: Automatic Cleanup with `--rm`

Normally stopped containers stick around. Use `--rm` to auto-delete on exit:

```bash
docker run --rm python:3.12-slim python3 -c "print('I will be cleaned up automatically')"
docker ps -a
```

The container won't appear in `docker ps -a` — it was removed on exit.

### Task K: Working Directory

```bash
docker run --rm -w /app python:3.12-slim pwd
```

The `-w` flag sets the working directory inside the container.

---

## Submission

Save a file named `Day_02_Output.md` in this folder containing the terminal output from each task.

## Grading Criteria

| Criteria | Points |
|----------|--------|
| Three Python variants pulled and sizes compared | 15 |
| Image inspected with `docker inspect` | 10 |
| Python REPL run inside container | 10 |
| Node.js run from a container | 10 |
| Multiple Python versions run side by side | 10 |
| Named containers created and logged | 15 |
| `docker stats` output captured | 5 |
| Environment variables passed to container | 10 |
| `--rm` auto-cleanup demonstrated | 10 |
| All containers cleaned up | 5 |
| **Total** | **100** |
