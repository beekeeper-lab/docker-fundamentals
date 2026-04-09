# Day 4 Assignment: Dockerfiles Part 1

## Overview

- **Topic:** Writing Dockerfiles to Build Custom Images
- **Type:** Technical / Hands-On
- **Estimated Time:** 30 minutes

## Background

A **Dockerfile** is a text file with instructions for building a Docker image. Each instruction creates a layer in the image.

### Common Dockerfile Instructions

| Instruction | Purpose | Example |
|-------------|---------|---------|
| `FROM` | Base image | `FROM python:3.12-slim` |
| `WORKDIR` | Set working directory | `WORKDIR /app` |
| `COPY` | Copy files from host to image | `COPY . .` |
| `RUN` | Execute a command during build | `RUN pip install flask` |
| `CMD` | Default command when container starts | `CMD ["python", "app.py"]` |
| `EXPOSE` | Document which port the app uses | `EXPOSE 5000` |
| `ENV` | Set environment variables | `ENV DEBUG=false` |

### Building an Image

```bash
docker build -t my-app:1.0 .
```

- `-t my-app:1.0` — Tag the image with a name and version
- `.` — Build context (the directory containing the Dockerfile)

---

## Part 1: Your First Dockerfile

### Task A: Build a Simple Python App

Create a project directory:

```bash
mkdir ~/docker-app
cd ~/docker-app
```

Create `app.py`:

```python
print("=" * 40)
print("  Hello from a Docker container!")
print("  Built with a custom Dockerfile.")
print("=" * 40)

import sys
print(f"\n  Python version: {sys.version}")

import os
name = os.environ.get("APP_USER", "World")
print(f"  Hello, {name}!")
print()
```

Create a `Dockerfile`:

```dockerfile
FROM python:3.12-slim

WORKDIR /app

COPY app.py .

CMD ["python", "app.py"]
```

### Task B: Build and Run

```bash
docker build -t hello-docker:1.0 .
docker run --rm hello-docker:1.0
docker run --rm -e APP_USER="Campbell" hello-docker:1.0
```

### Task C: See the Image

```bash
docker images | grep hello-docker
```

---

## Part 2: A Web Application

### Task D: Build a Flask App

Create a new directory:

```bash
mkdir ~/docker-flask
cd ~/docker-flask
```

Create `app.py`:

```python
from flask import Flask, jsonify
from datetime import datetime

app = Flask(__name__)

@app.route("/")
def home():
    return "<h1>Hello from Flask in Docker!</h1>"

@app.route("/api/time")
def get_time():
    return jsonify({"time": datetime.now().isoformat()})

@app.route("/api/health")
def health():
    return jsonify({"status": "healthy"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
```

Create `requirements.txt`:

```
flask==3.1.0
```

Create the `Dockerfile`:

```dockerfile
FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

EXPOSE 5000

CMD ["python", "app.py"]
```

> **Key detail:** We copy and install `requirements.txt` BEFORE copying `app.py`. This means Docker can cache the dependency installation layer. If you only change `app.py`, Docker skips the `pip install` step on rebuild.

### Task E: Build and Run the Flask App

```bash
docker build -t flask-app:1.0 .
docker run -d -p 5000:5000 --name my-flask flask-app:1.0
```

Test it:

```bash
curl http://localhost:5000
curl http://localhost:5000/api/time
curl http://localhost:5000/api/health
```

Check logs:

```bash
docker logs my-flask
```

Clean up:

```bash
docker stop my-flask && docker rm my-flask
```

---

## Part 3: A Static Website

### Task F: Build a Custom Nginx Site

```bash
mkdir ~/docker-site
cd ~/docker-site
```

Create `index.html`:

```html
<!DOCTYPE html>
<html>
<head>
    <title>My Docker Site</title>
    <style>
        body { font-family: sans-serif; max-width: 600px; margin: 50px auto; }
        h1 { color: #2196F3; }
    </style>
</head>
<body>
    <h1>Hello from Docker!</h1>
    <p>This static site is served by Nginx inside a Docker container.</p>
    <p>Built by Campbell Reed.</p>
</body>
</html>
```

Create the `Dockerfile`:

```dockerfile
FROM nginx:alpine

COPY index.html /usr/share/nginx/html/index.html

EXPOSE 80
```

### Task G: Build and Run

```bash
docker build -t my-site:1.0 .
docker run -d -p 8080:80 --name my-site my-site:1.0
curl http://localhost:8080
docker stop my-site && docker rm my-site
```

---

## Part 4: Understanding the Build Process

### Task H: Watch the Build Layers

Rebuild the Flask app and watch the output:

```bash
cd ~/docker-flask
docker build -t flask-app:1.1 .
```

Notice each step says `CACHED` — Docker reuses layers that haven't changed. Now modify `app.py` (add a comment) and rebuild:

```bash
echo "# modified" >> app.py
docker build -t flask-app:1.2 .
```

Only the layers AFTER the change are rebuilt. The `pip install` layer is still cached.

### Task I: List Your Custom Images

```bash
docker images | grep -E "(hello-docker|flask-app|my-site)"
```

---

## Submission

Save a file named `Day_04_Output.md` in this folder containing the terminal output from each task. Include the Dockerfiles you wrote.

## Grading Criteria

| Criteria | Points |
|----------|--------|
| Simple Python Dockerfile created and built | 15 |
| Container run with and without environment variable | 10 |
| Flask Dockerfile with requirements.txt optimization | 20 |
| Flask app accessible via browser/curl | 10 |
| Static Nginx site Dockerfile created | 15 |
| Static site served correctly | 10 |
| Layer caching demonstrated on rebuild | 10 |
| All custom images visible in `docker images` | 5 |
| All containers cleaned up | 5 |
| **Total** | **100** |
