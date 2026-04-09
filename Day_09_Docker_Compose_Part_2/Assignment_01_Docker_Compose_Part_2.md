# Day 9 Assignment: Docker Compose Part 2

## Overview

- **Topic:** Environment Variables, `.env` Files, Health Checks, and Profiles
- **Type:** Technical / Hands-On
- **Estimated Time:** 30 minutes

## Background

### Environment Variables

Three ways to set environment variables in Compose:

```yaml
services:
  app:
    # 1. Inline
    environment:
      - DEBUG=true
      - API_KEY=abc123

    # 2. From a file
    env_file:
      - .env

    # 3. From shell (variable substitution)
    environment:
      - DB_HOST=${DB_HOST:-localhost}
```

### `.env` File

Docker Compose automatically reads a `.env` file in the same directory:

```bash
# .env
POSTGRES_PASSWORD=supersecret
APP_PORT=8080
DEBUG=false
```

```yaml
services:
  db:
    environment:
      - POSTGRES_PASSWORD=${POSTGRES_PASSWORD}
  app:
    ports:
      - "${APP_PORT}:5000"
```

### Health Checks

```yaml
services:
  db:
    image: postgres:16-alpine
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 10s
      timeout: 5s
      retries: 3
      start_period: 10s
```

### Profiles

Group services so you only start what you need:

```yaml
services:
  app:
    # Always starts (no profile)

  debug-tools:
    profiles: ["debug"]
    # Only starts with: docker compose --profile debug up
```

---

## Part 1: Environment Variables and `.env` Files

### Task A: Set Up the Project

```bash
mkdir ~/compose-env
cd ~/compose-env
```

Create `.env`:

```bash
cat > .env << 'EOF'
APP_PORT=8080
DB_PASSWORD=my-secure-password
DB_NAME=myapp
DB_USER=appuser
FLASK_DEBUG=true
EOF
```

Create `app.py`:

```python
from flask import Flask, jsonify
import os

app = Flask(__name__)

@app.route("/")
def home():
    return jsonify({
        "debug": os.environ.get("FLASK_DEBUG", "false"),
        "db_host": os.environ.get("DB_HOST", "unknown"),
        "db_name": os.environ.get("DB_NAME", "unknown"),
    })

if __name__ == "__main__":
    debug = os.environ.get("FLASK_DEBUG", "false").lower() == "true"
    app.run(host="0.0.0.0", port=5000, debug=debug)
```

Create `requirements.txt`:

```
flask==3.1.0
```

Create `Dockerfile`:

```dockerfile
FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY app.py .
CMD ["python", "app.py"]
```

Create `docker-compose.yml`:

```yaml
services:
  api:
    build: .
    ports:
      - "${APP_PORT}:5000"
    environment:
      - FLASK_DEBUG=${FLASK_DEBUG}
      - DB_HOST=db
      - DB_NAME=${DB_NAME}
    depends_on:
      db:
        condition: service_healthy

  db:
    image: postgres:16-alpine
    environment:
      - POSTGRES_PASSWORD=${DB_PASSWORD}
      - POSTGRES_USER=${DB_USER}
      - POSTGRES_DB=${DB_NAME}
    volumes:
      - db-data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U ${DB_USER}"]
      interval: 5s
      timeout: 3s
      retries: 5
      start_period: 5s

volumes:
  db-data:
```

### Task B: Start and Verify

```bash
docker compose up -d
docker compose ps
curl http://localhost:8080
```

The response should show the environment variables from `.env`.

### Task C: Override with a Different `.env`

Create `.env.production`:

```bash
cat > .env.production << 'EOF'
APP_PORT=80
DB_PASSWORD=production-password-42
DB_NAME=proddb
DB_USER=produser
FLASK_DEBUG=false
EOF
```

```bash
docker compose down
docker compose --env-file .env.production up -d
curl http://localhost:80
docker compose down
```

---

## Part 2: Health Checks and Dependencies

### Task D: Observe Health Checks

```bash
docker compose --env-file .env up -d
docker compose ps
```

Watch the `db` service go from "starting" to "healthy":

```bash
watch -n 1 docker compose ps
```

(Press `Ctrl+C` to stop watching)

The `api` service won't start until `db` is healthy because of `condition: service_healthy`.

---

## Part 3: Profiles

### Task E: Add Debug and Admin Services

Update `docker-compose.yml` — add these services at the end:

```yaml
  adminer:
    image: adminer
    ports:
      - "9090:8080"
    profiles:
      - debug
    depends_on:
      - db

  redis:
    image: redis:alpine
    profiles:
      - cache
```

### Task F: Start with Profiles

```bash
docker compose down

# Start only the core services (api + db)
docker compose up -d
docker compose ps

# Start with the debug profile (adds adminer)
docker compose --profile debug up -d
docker compose ps
```

Visit `http://localhost:9090` to see Adminer (a database admin UI). Log in with the credentials from your `.env`.

```bash
# Start everything
docker compose --profile debug --profile cache up -d
docker compose ps
docker compose down
```

---

## Part 4: Restart Policies and Resource Limits

### Task G: Add Restart Policies

Update your `api` service in `docker-compose.yml`:

```yaml
  api:
    build: .
    ports:
      - "${APP_PORT}:5000"
    environment:
      - FLASK_DEBUG=${FLASK_DEBUG}
      - DB_HOST=db
      - DB_NAME=${DB_NAME}
    depends_on:
      db:
        condition: service_healthy
    restart: unless-stopped
    deploy:
      resources:
        limits:
          memory: 256M
          cpus: "0.5"
```

Restart policies:
- `no` — Never restart (default)
- `always` — Always restart
- `unless-stopped` — Restart unless manually stopped
- `on-failure` — Restart only on non-zero exit

### Task H: Test the Restart Policy

```bash
docker compose up -d
docker compose ps

# Kill the API process
docker compose kill api
docker compose ps
```

Wait a few seconds and check again — the container should restart automatically.

```bash
docker compose ps
docker compose down -v
```

---

## Submission

Save a file named `Day_09_Output.md` in this folder containing terminal output and your `docker-compose.yml` and `.env` files.

## Grading Criteria

| Criteria | Points |
|----------|--------|
| `.env` file created and values used in compose | 15 |
| Environment variables visible in running app | 10 |
| Alternate `.env.production` file used | 10 |
| Health check configured and working | 15 |
| `depends_on` with `condition: service_healthy` | 10 |
| Profiles used to optionally start services | 15 |
| Restart policy configured and tested | 15 |
| Everything cleaned up with `docker compose down -v` | 10 |
| **Total** | **100** |
