# Module 4: Dockerfiles Part 1

> 🏷️ Useful Soon

> 🎯 **Teach:** How to write Dockerfiles to build custom images with your own applications.
> **See:** Building Python apps, Flask web apps, and static Nginx sites from scratch.
> **Feel:** Empowered to containerize any application you write.

> 🔄 **Where this fits:** So far you've been using pre-built images from Docker Hub. Now you learn to build your own. This is the transition from Docker consumer to Docker creator — and it's where Docker becomes truly powerful for your development workflow.

## Dockerfile Basics

> 🎯 **Teach:** The core Dockerfile instructions and how each one creates a layer in your image.
> **See:** A reference table of FROM, WORKDIR, COPY, RUN, CMD, EXPOSE, and ENV.
> **Feel:** Ready to read and write Dockerfiles with confidence.

> 🎙️ A Dockerfile is a text file with instructions for building a Docker image. Think of it as a recipe: each instruction adds a layer to the image. FROM sets the base image, WORKDIR sets your working directory, COPY brings files in from your host, RUN executes commands during the build, and CMD sets what runs when the container starts. These five instructions cover ninety percent of what you'll need.

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

> 🎙️ Take a look at the table above. These seven instructions are your Dockerfile vocabulary. You won't need all of them in every Dockerfile, but FROM, WORKDIR, COPY, RUN, and CMD will appear in almost every one you write.

### Building an Image

```bash
docker build -t my-app:1.0 .
```

- `-t my-app:1.0` — Tag the image with a name and version
- `.` — Build context (the directory containing the Dockerfile)

> 💡 **Remember this one thing:** Every Dockerfile instruction creates a layer. Order matters — put things that change least frequently (like installing dependencies) before things that change often (like copying your app code). This maximizes Docker's layer caching.

## Your First Dockerfile

> 🎯 **Teach:** The complete workflow of writing a Dockerfile, building an image, and running a container from it.
> **See:** A Python app running inside a custom-built container.
> **Feel:** The satisfaction of building your first image from scratch.

> 🎙️ Let's build your first custom Docker image. You'll create a simple Python script, write a Dockerfile for it, build the image, and run it. This is the core Docker workflow you'll use hundreds of times.

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

> 🎙️ Now it's time to build and run your image. The docker build command reads your Dockerfile and creates an image. The dash t flag gives it a name and version tag. Then docker run creates a container from that image and runs it.

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

## A Web Application

> 🎯 **Teach:** How to containerize a Flask web app with dependency caching optimization.
> **See:** A Dockerfile that separates requirements installation from code copying for faster rebuilds.
> **Feel:** Capable of containerizing real web applications you build.

> 🎙️ Now let's build something more real — a Flask web application. This is where you'll see an important optimization pattern: copy and install your requirements file first, then copy your application code. Docker caches each layer, so if you only change your app code, it skips the dependency installation step entirely. This saves huge amounts of time during development.

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

> 🎙️ Time to build and run your Flask app. Notice the dash d flag, which runs the container in detached mode so it stays running in the background. The dash p flag maps port 5000 on your host to port 5000 inside the container, so you can access the web app from your browser or curl.

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

## A Static Website

> 🎯 **Teach:** How to serve static HTML with a minimal Nginx container.
> **See:** A two-line Dockerfile that produces a tiny, production-ready web server.
> **Feel:** Impressed by how simple containerizing a static site can be.

> 🎙️ Not every containerized app needs a programming language runtime. Here you'll build a simple static website served by Nginx. The Dockerfile is just two lines: start from the Nginx Alpine image, and copy your HTML file into the right directory. Alpine-based images are tiny — your entire web server will be under 50 megabytes.

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
</body>
</html>
```

Create the `Dockerfile`:

```dockerfile
FROM nginx:alpine

COPY index.html /usr/share/nginx/html/index.html

EXPOSE 80
```

> 🎙️ Build this image and run it on port 8080. Since Nginx listens on port 80 inside the container, you'll map 8080 on your host to 80 in the container. After verifying it works with curl, clean up the container.

### Task G: Build and Run

```bash
docker build -t my-site:1.0 .
docker run -d -p 8080:80 --name my-site my-site:1.0
curl http://localhost:8080
docker stop my-site && docker rm my-site
```

## Understanding the Build Process

> 🎯 **Teach:** How Docker's layer caching works and why instruction order matters.
> **See:** A rebuild where cached layers are skipped and only changed layers are rebuilt.
> **Feel:** Motivated to structure Dockerfiles for maximum cache efficiency.

> 🎙️ One of Docker's most important features is layer caching. When you rebuild an image, Docker checks each instruction against its cache. If nothing changed, it reuses the cached layer. But the moment one layer changes, every layer after it must be rebuilt. That's why instruction order matters so much in your Dockerfiles.

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

> 🎙️ Let's take a moment to see all the custom images you've built in this module. The docker images command lists everything, and you can filter it with grep to see just your work.

### Task I: List Your Custom Images

```bash
docker images | grep -E "(hello-docker|flask-app|my-site)"
```

> 💡 **Remember this one thing:** Copy and install dependencies before copying application code. This maximizes cache hits and makes rebuilds dramatically faster during development.

> 🎙️ Great work. You've gone from writing your first Dockerfile to building three different types of applications: a simple Python script, a Flask web server, and a static Nginx site. You also saw how layer caching can speed up your builds dramatically. Save your output and Dockerfiles for submission.

## Submission

Save a file named `Day_04_Output.md` in this folder containing the terminal output from each task. Include the Dockerfiles you wrote.

### Grading Criteria

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
