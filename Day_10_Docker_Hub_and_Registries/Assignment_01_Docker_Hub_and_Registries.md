# Day 10 Assignment: Docker Hub and Registries

## Overview

- **Topic:** Pushing Images, Docker Hub, Image Tagging, and Best Practices
- **Type:** Technical / Hands-On
- **Estimated Time:** 30 minutes

## Background

### Docker Hub

[Docker Hub](https://hub.docker.com) is the default public registry for Docker images. It's where `nginx`, `python`, `postgres`, and thousands of other images come from.

### Image Naming Convention

```
registry/username/repository:tag
```

Examples:
- `nginx:alpine` — Official image (no username)
- `yourusername/my-app:1.0` — Your image
- `ghcr.io/owner/repo:latest` — GitHub Container Registry

### Tagging Strategy

| Tag | Purpose |
|-----|---------|
| `1.0.0` | Specific version (immutable) |
| `1.0` | Latest patch in 1.0.x |
| `1` | Latest minor in 1.x.x |
| `latest` | Most recent build (default, mutable) |

---

## Part 1: Docker Hub Account

### Task A: Create a Docker Hub Account

1. Go to [hub.docker.com](https://hub.docker.com) and create a free account
2. Log in from the CLI:

```bash
docker login
```

Enter your username and password (or access token).

### Task B: Verify Login

```bash
docker info | grep Username
```

---

## Part 2: Build, Tag, and Push

### Task C: Create an Image to Push

```bash
mkdir ~/docker-publish
cd ~/docker-publish
```

Create `app.py`:

```python
from flask import Flask, jsonify
from datetime import datetime

app = Flask(__name__)

@app.route("/")
def home():
    return jsonify({
        "app": "Docker Demo",
        "version": "1.0.0",
        "timestamp": datetime.now().isoformat(),
        "author": "Campbell Reed",
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
```

Create `requirements.txt`:

```
flask==3.1.0
```

Create `Dockerfile`:

```dockerfile
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

RUN adduser --disabled-password --gecos '' appuser

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

USER appuser
EXPOSE 5000

CMD ["python", "app.py"]
```

### Task D: Build and Tag

```bash
docker build -t my-demo-app .
```

Tag it for Docker Hub (replace `YOUR-USERNAME` with your Docker Hub username):

```bash
docker tag my-demo-app YOUR-USERNAME/demo-app:1.0.0
docker tag my-demo-app YOUR-USERNAME/demo-app:1.0
docker tag my-demo-app YOUR-USERNAME/demo-app:latest
```

See all your tags:

```bash
docker images | grep demo-app
```

Notice they all have the same Image ID — tags are just labels pointing to the same image.

### Task E: Push to Docker Hub

```bash
docker push YOUR-USERNAME/demo-app:1.0.0
docker push YOUR-USERNAME/demo-app:1.0
docker push YOUR-USERNAME/demo-app:latest
```

Go to `hub.docker.com/r/YOUR-USERNAME/demo-app` in a browser and see your image listed.

---

## Part 3: Pull and Run from Docker Hub

### Task F: Simulate a Fresh Machine

Remove the local image and pull it from Docker Hub:

```bash
docker rmi YOUR-USERNAME/demo-app:1.0.0
docker rmi YOUR-USERNAME/demo-app:1.0
docker rmi YOUR-USERNAME/demo-app:latest
docker rmi my-demo-app

docker images | grep demo-app
```

All gone locally. Now pull and run:

```bash
docker run --rm -p 5000:5000 YOUR-USERNAME/demo-app:1.0.0
```

Docker pulls it from Docker Hub and runs it. Press `Ctrl+C` to stop.

---

## Part 4: Versioning and Updates

### Task G: Release a New Version

Update `app.py` — change the version to `"1.1.0"` and add a new endpoint:

```python
@app.route("/api/info")
def info():
    import platform
    return jsonify({
        "python": platform.python_version(),
        "platform": platform.platform(),
    })
```

Build and push the new version:

```bash
docker build -t YOUR-USERNAME/demo-app:1.1.0 .
docker tag YOUR-USERNAME/demo-app:1.1.0 YOUR-USERNAME/demo-app:1.1
docker tag YOUR-USERNAME/demo-app:1.1.0 YOUR-USERNAME/demo-app:latest
docker push YOUR-USERNAME/demo-app:1.1.0
docker push YOUR-USERNAME/demo-app:1.1
docker push YOUR-USERNAME/demo-app:latest
```

Now someone pulling `latest` gets 1.1.0, but `1.0.0` is still available.

### Task H: Run Different Versions

```bash
docker run --rm -d -p 5000:5000 --name v1 YOUR-USERNAME/demo-app:1.0.0
docker run --rm -d -p 5001:5000 --name v2 YOUR-USERNAME/demo-app:1.1.0

curl http://localhost:5000
curl http://localhost:5001
curl http://localhost:5001/api/info

docker stop v1 v2
```

Both versions running side by side.

---

## Part 5: Image Security and Best Practices

### Task I: Scan an Image for Vulnerabilities

```bash
docker scout quickview YOUR-USERNAME/demo-app:1.1.0
```

Or if Docker Scout isn't available:

```bash
docker inspect YOUR-USERNAME/demo-app:1.1.0 --format='{{.Config.User}}'
```

Verify the image runs as a non-root user.

### Task J: Best Practices Checklist

Review your image against these best practices:

- [ ] Uses a specific base image tag (not `latest`)
- [ ] Runs as non-root user
- [ ] Uses `--no-cache-dir` with pip
- [ ] Has a `.dockerignore` file
- [ ] Sets `PYTHONDONTWRITEBYTECODE` and `PYTHONUNBUFFERED`
- [ ] Dependencies installed before copying app code (layer caching)
- [ ] `EXPOSE` documents the port
- [ ] Uses semantic version tags (1.0.0, 1.1.0)

### Task K: Clean Up

```bash
docker system prune -a
```

This removes all unused images, containers, and networks. Use with caution in production!

---

## Submission

Save a file named `Day_10_Output.md` in this folder containing terminal output and a link to your Docker Hub repository.

## Grading Criteria

| Criteria | Points |
|----------|--------|
| Docker Hub account created and logged in | 10 |
| Image built with proper Dockerfile | 10 |
| Image tagged with multiple version tags | 15 |
| Image pushed to Docker Hub | 15 |
| Image pulled and run from Docker Hub | 10 |
| Updated version pushed with new tag | 15 |
| Two versions run side by side | 10 |
| Best practices checklist completed | 10 |
| System cleaned up | 5 |
| **Total** | **100** |
