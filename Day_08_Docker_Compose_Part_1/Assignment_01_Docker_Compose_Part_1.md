# Day 8 Assignment: Docker Compose Part 1

## Overview

- **Topic:** Defining Multi-Container Applications with `docker-compose.yml`
- **Type:** Technical / Hands-On
- **Estimated Time:** 30 minutes

## Background

### What Is Docker Compose?

Docker Compose lets you define and run **multi-container applications** with a single YAML file. Instead of running multiple `docker run` commands with networks and volumes, you describe everything in `docker-compose.yml` and start it with one command.

### Basic Structure

```yaml
services:
  web:
    image: nginx
    ports:
      - "8080:80"

  api:
    build: ./api
    ports:
      - "5000:5000"
    environment:
      - DATABASE_URL=postgres://db:5432/mydb

  db:
    image: postgres:16-alpine
    environment:
      - POSTGRES_PASSWORD=secret
    volumes:
      - db-data:/var/lib/postgresql/data

volumes:
  db-data:
```

### Key Commands

| Command | Purpose |
|---------|---------|
| `docker compose up` | Start all services |
| `docker compose up -d` | Start in background |
| `docker compose down` | Stop and remove everything |
| `docker compose ps` | List running services |
| `docker compose logs` | View logs from all services |
| `docker compose build` | Build/rebuild images |
| `docker compose exec <svc> <cmd>` | Run command in a service |

> **Note:** Modern Docker uses `docker compose` (with a space). Older versions used `docker-compose` (with a hyphen).

---

## Part 1: Your First Compose File

### Task A: Create a Simple Compose Project

```bash
mkdir ~/compose-demo
cd ~/compose-demo
```

Create `docker-compose.yml`:

```yaml
services:
  web:
    image: nginx:alpine
    ports:
      - "8080:80"
    volumes:
      - ./html:/usr/share/nginx/html
```

Create the content:

```bash
mkdir html
echo "<h1>Hello from Docker Compose!</h1>" > html/index.html
```

### Task B: Start the Services

```bash
docker compose up -d
docker compose ps
curl http://localhost:8080
```

### Task C: View Logs

```bash
docker compose logs
docker compose logs web
docker compose logs -f web     # Follow — Ctrl+C to stop
```

### Task D: Stop Everything

```bash
docker compose down
docker compose ps
```

`down` stops containers, removes them, and removes the network. Clean and simple.

---

## Part 2: Multi-Service Application

### Task E: Build a Web App with an API

Create project structure:

```bash
mkdir ~/compose-app
cd ~/compose-app
mkdir api frontend
```

Create `api/app.py`:

```python
from flask import Flask, jsonify
import os

app = Flask(__name__)

@app.route("/api/message")
def message():
    return jsonify({
        "message": "Hello from the API!",
        "hostname": os.uname().nodename,
    })

@app.route("/api/health")
def health():
    return jsonify({"status": "healthy"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
```

Create `api/requirements.txt`:

```
flask==3.1.0
```

Create `api/Dockerfile`:

```dockerfile
FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY app.py .
EXPOSE 5000
CMD ["python", "app.py"]
```

Create `frontend/index.html`:

```html
<!DOCTYPE html>
<html>
<head><title>Compose Demo</title></head>
<body>
    <h1>Docker Compose Demo</h1>
    <p>Frontend served by Nginx, API served by Flask.</p>
    <p>Try: <a href="/api/message">/api/message</a></p>
    <p>Try: <a href="/api/health">/api/health</a></p>
</body>
</html>
```

Create `frontend/nginx.conf`:

```nginx
server {
    listen 80;

    location / {
        root /usr/share/nginx/html;
        index index.html;
    }

    location /api/ {
        proxy_pass http://api:5000;
        proxy_set_header Host $host;
    }
}
```

Create `docker-compose.yml`:

```yaml
services:
  frontend:
    image: nginx:alpine
    ports:
      - "8080:80"
    volumes:
      - ./frontend/index.html:/usr/share/nginx/html/index.html
      - ./frontend/nginx.conf:/etc/nginx/conf.d/default.conf
    depends_on:
      - api

  api:
    build: ./api
    expose:
      - "5000"
```

### Task F: Start and Test

```bash
docker compose up -d
docker compose ps
curl http://localhost:8080
curl http://localhost:8080/api/message
curl http://localhost:8080/api/health
```

Notice:
- The frontend is accessible on port 8080
- Nginx proxies `/api/*` requests to the Flask container
- The containers find each other by service name (`api`)
- `depends_on` ensures the API starts before the frontend

### Task G: Check Logs from Both Services

```bash
docker compose logs
docker compose logs api
docker compose logs frontend
```

---

## Part 3: Adding a Database

### Task H: Add PostgreSQL to the Stack

Update `docker-compose.yml`:

```yaml
services:
  frontend:
    image: nginx:alpine
    ports:
      - "8080:80"
    volumes:
      - ./frontend/index.html:/usr/share/nginx/html/index.html
      - ./frontend/nginx.conf:/etc/nginx/conf.d/default.conf
    depends_on:
      - api

  api:
    build: ./api
    expose:
      - "5000"
    environment:
      - DATABASE_HOST=db
      - DATABASE_PORT=5432
      - DATABASE_USER=postgres
      - DATABASE_PASSWORD=secret
    depends_on:
      - db

  db:
    image: postgres:16-alpine
    environment:
      - POSTGRES_PASSWORD=secret
    volumes:
      - db-data:/var/lib/postgresql/data

volumes:
  db-data:
```

### Task I: Restart the Stack

```bash
docker compose down
docker compose up -d
docker compose ps
```

All three services should be running.

### Task J: Interact with the Database

```bash
docker compose exec db psql -U postgres -c "SELECT version();"
docker compose exec db psql -U postgres -c "CREATE TABLE visits(id serial, visited_at timestamp default now());"
docker compose exec db psql -U postgres -c "INSERT INTO visits DEFAULT VALUES;"
docker compose exec db psql -U postgres -c "SELECT * FROM visits;"
```

### Task K: Stop and Clean Up

```bash
docker compose down
docker compose down -v   # Also removes volumes
```

The `-v` flag removes named volumes too. Without it, `db-data` persists for next time.

---

## Submission

Save a file named `Day_08_Output.md` in this folder containing terminal output and your `docker-compose.yml` files.

## Grading Criteria

| Criteria | Points |
|----------|--------|
| Simple single-service Compose file working | 10 |
| `docker compose up/down/ps/logs` all demonstrated | 10 |
| Multi-service app with frontend + API | 20 |
| Nginx reverse proxy to API working | 15 |
| PostgreSQL added to the stack | 15 |
| Database queries run via `docker compose exec` | 10 |
| `depends_on` used correctly | 5 |
| Named volume used for database persistence | 10 |
| Everything cleaned up with `docker compose down` | 5 |
| **Total** | **100** |
