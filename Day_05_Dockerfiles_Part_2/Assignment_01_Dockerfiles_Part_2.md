# Day 5 Assignment: Dockerfiles Part 2

## Overview

- **Topic:** Layers, Caching, Multi-Stage Builds, and `.dockerignore`
- **Type:** Technical / Hands-On
- **Estimated Time:** 30 minutes

## Background

### Layer Optimization

Every `RUN`, `COPY`, and `ADD` instruction creates a new layer. Fewer layers = smaller images.

```dockerfile
# Bad — 3 layers
RUN apt-get update
RUN apt-get install -y curl
RUN apt-get clean

# Good — 1 layer
RUN apt-get update && \
    apt-get install -y curl && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*
```

### Multi-Stage Builds

Use one stage to build, another to run. Only the final stage goes into the image:

```dockerfile
# Stage 1: Build
FROM golang:1.21 AS builder
WORKDIR /app
COPY . .
RUN go build -o myapp

# Stage 2: Run (tiny image, only the binary)
FROM alpine:3.19
COPY --from=builder /app/myapp /usr/local/bin/
CMD ["myapp"]
```

The build tools, source code, and intermediate files are NOT in the final image.

### `.dockerignore`

Like `.gitignore`, this tells Docker which files to exclude from the build context:

```
.git
__pycache__
*.pyc
node_modules
.env
*.md
.venv
```

---

## Part 1: Layer Optimization

### Task A: Compare Layer Counts

Create a project directory:

```bash
mkdir ~/docker-layers
cd ~/docker-layers
```

Create `Dockerfile.bad` (many layers):

```dockerfile
FROM python:3.12-slim
WORKDIR /app
RUN pip install flask
RUN pip install requests
RUN pip install gunicorn
COPY app.py .
CMD ["python", "app.py"]
```

Create `Dockerfile.good` (optimized):

```dockerfile
FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY app.py .
CMD ["python", "app.py"]
```

Create supporting files:

```bash
echo "flask\nrequests\ngunicorn" > requirements.txt
echo 'print("hello")' > app.py
```

Build both and compare:

```bash
docker build -f Dockerfile.bad -t layers-bad .
docker build -f Dockerfile.good -t layers-good .
docker history layers-bad
docker history layers-good
```

`docker history` shows each layer's size. The optimized version has fewer, more logical layers.

---

## Part 2: Multi-Stage Builds

### Task B: Build a Java App with Multi-Stage

Create a project:

```bash
mkdir ~/docker-multistage
cd ~/docker-multistage
```

Create `Hello.java`:

```java
public class Hello {
    public static void main(String[] args) {
        System.out.println("Hello from a multi-stage Docker build!");
        System.out.println("Java version: " + System.getProperty("java.version"));
    }
}
```

Create a `Dockerfile`:

```dockerfile
# Stage 1: Compile with full JDK
FROM eclipse-temurin:21-jdk AS builder
WORKDIR /app
COPY Hello.java .
RUN javac Hello.java

# Stage 2: Run with lightweight JRE
FROM eclipse-temurin:21-jre-alpine
WORKDIR /app
COPY --from=builder /app/Hello.class .
CMD ["java", "Hello"]
```

Build and compare sizes:

```bash
docker build -t hello-java:multistage .
docker images | grep -E "(temurin|hello-java)"
```

The multi-stage image is much smaller because it doesn't include the JDK (compiler, dev tools).

### Task C: Multi-Stage Python Build

```bash
mkdir ~/docker-multistage-py
cd ~/docker-multistage-py
```

Create `app.py`:

```python
from flask import Flask
app = Flask(__name__)

@app.route("/")
def home():
    return "Hello from multi-stage Python!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
```

Create `requirements.txt`:

```
flask==3.1.0
```

Create `Dockerfile`:

```dockerfile
# Stage 1: Install dependencies
FROM python:3.12-slim AS builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

# Stage 2: Run with minimal image
FROM python:3.12-slim
WORKDIR /app
COPY --from=builder /install /usr/local
COPY app.py .
EXPOSE 5000
CMD ["python", "app.py"]
```

```bash
docker build -t flask-multistage .
docker run --rm -d -p 5000:5000 --name flask-ms flask-multistage
curl http://localhost:5000
docker stop flask-ms
```

---

## Part 3: `.dockerignore`

### Task D: Create a `.dockerignore`

In your project directory:

```bash
cat > .dockerignore << 'EOF'
.git
.gitignore
__pycache__
*.pyc
*.pyo
.env
.venv
venv
node_modules
*.md
Dockerfile*
docker-compose*.yml
.dockerignore
tests/
docs/
EOF
```

### Task E: See the Effect

Create some files that should be ignored:

```bash
mkdir __pycache__ tests docs .venv
echo "SECRET=abc" > .env
echo "# readme" > README.md
touch __pycache__/module.pyc
```

Build and check that ignored files aren't in the image:

```bash
docker build -t ignore-test .
docker run --rm ignore-test ls -la
docker run --rm ignore-test sh -c "ls .env 2>&1 || echo '.env not found (ignored!)'"
```

---

## Part 4: Best Practices Summary

### Task F: Build an Optimized Image

Combine everything into one well-structured Dockerfile:

```bash
mkdir ~/docker-best-practices
cd ~/docker-best-practices
```

Create a Python app with proper structure, a `.dockerignore`, and an optimized Dockerfile that follows these best practices:

1. Use a specific image tag (not `latest`)
2. Set a non-root user for security
3. Copy requirements first, install, then copy code (caching)
4. Use `--no-cache-dir` with pip
5. Set `PYTHONDONTWRITEBYTECODE=1` and `PYTHONUNBUFFERED=1`
6. Use `EXPOSE` to document the port

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

Build, run, and verify the user:

```bash
docker build -t best-practices .
docker run --rm best-practices whoami
```

It should print `appuser`, not `root`.

---

## Submission

Save a file named `Day_05_Output.md` in this folder containing the terminal output and all Dockerfiles.

## Grading Criteria

| Criteria | Points |
|----------|--------|
| Layer comparison with `docker history` | 15 |
| Java multi-stage build with size comparison | 20 |
| Python multi-stage build working | 15 |
| `.dockerignore` created and tested | 15 |
| Best practices Dockerfile with non-root user | 25 |
| All containers cleaned up | 10 |
| **Total** | **100** |
