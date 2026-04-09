# Module 9: Docker Compose Part 2

> 🏷️ When You're Ready

> 🎯 **Teach:** Advanced Docker Compose features: environment variable management, health checks, profiles, restart policies, and resource limits.
> **See:** Production-ready Compose configurations with proper dependency management and resilience.
> **Feel:** Ready to write Docker Compose files for real production deployments.

> 🔄 **Where this fits:** Module 8 covered the basics of Docker Compose. Now you'll learn the features that make Compose production-ready — environment management, health-aware dependencies, optional services, and automatic recovery.

## Environment Variables

> 🎯 **Teach:** The three ways to pass environment variables to services in Docker Compose.
> **See:** Inline variables, env_file references, and shell variable substitution in a Compose file.
> **Feel:** Aware of the options so you can choose the right approach for each situation.

> 🎙️ Managing configuration is one of the most important parts of any deployment. Docker Compose gives you three ways to set environment variables: inline in the YAML file, from an external env file, and through shell variable substitution. The .env file approach is the most common because it keeps secrets out of your docker-compose.yml, which you can safely commit to version control.

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

> 💡 **Remember this one thing:** Keep secrets in `.env` files that are gitignored, not in `docker-compose.yml`. Use `${VAR:-default}` syntax to provide fallback values for optional variables.

## Environment Variables and .env Files

> 🎯 **Teach:** How to manage configuration with .env files and environment variable substitution.
> **See:** Variables flowing from .env into containers, and switching between environments.
> **Feel:** In control of your application configuration across environments.

> 🎙️ Let's set up a project that demonstrates all three approaches to environment variables. You'll create a dot-env file with your configuration, a Flask app that reads those variables, and a Compose file that wires everything together. Pay attention to how the variable values flow from the dot-env file into the running containers.

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

> 🎙️ One of the best things about using dot-env files is that you can swap configurations without changing your docker-compose.yml at all. You'll create a separate production env file and launch the same stack with completely different settings. This is how teams manage different environments — development, staging, and production — with the same Compose file.

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

## Health Checks and Dependencies

> 🎯 **Teach:** How health checks verify service readiness and how depends_on conditions enforce startup order.
> **See:** A database transitioning from "starting" to "healthy" while the API waits to launch.
> **Feel:** Confident that your services start in the right order without fragile sleep workarounds.

> 🎙️ Health checks let Docker monitor whether a service is actually ready, not just running. A database container might be running but still initializing. With a health check, Docker can tell the difference. And with condition service_healthy in depends_on, your API won't start until the database is truly ready to accept connections. This eliminates the fragile "sleep 5 and hope" pattern.

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

> 🎙️ Now let's see health checks in action. Start the stack and watch the database service transition from "starting" to "healthy." The API service will wait patiently until the database reports healthy before it starts up. This is reliable, deterministic startup ordering.

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

> 💡 **Remember this one thing:** Use `healthcheck` with `condition: service_healthy` in `depends_on` to ensure services start in the right order. This replaces fragile sleep-based workarounds with reliable dependency management.

## Profiles

> 🎯 **Teach:** How Compose profiles let you define optional services that only start on demand.
> **See:** Debug and admin services that appear only when you activate their profile.
> **Feel:** Empowered to keep your default stack lean while having extra tools a flag away.

> 🎙️ Profiles let you define optional services that only start when you ask for them. This is perfect for development tools, debug utilities, or cache services that you don't always need. A service without a profile always starts. A service with a profile only starts when you pass the dash-dash-profile flag. This keeps your default stack lean while making extra tools available on demand.

```yaml
services:
  app:
    # Always starts (no profile)

  debug-tools:
    profiles: ["debug"]
    # Only starts with: docker compose --profile debug up
```

> 🎙️ Let's add two optional services — Adminer for database administration and Redis for caching. By putting them behind profiles, they won't start by default. Your core stack stays lean, and you only bring in extra tools when you need them.

### Task E: Add Debug and Admin Services

Update `docker-compose.yml` — add these services:

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

## Restart Policies and Resource Limits

> 🎯 **Teach:** How restart policies provide automatic recovery and resource limits prevent runaway containers.
> **See:** A killed container restarting itself, and memory/CPU caps applied to a service.
> **Feel:** Prepared to make your Compose services resilient and production-safe.

> 🎙️ In production, you want services that recover automatically from crashes. Restart policies tell Docker what to do when a container exits. The "unless-stopped" policy restarts containers on failure and on system reboot, but respects a manual stop. Resource limits prevent a single service from consuming all available memory or CPU on the host.

> 🎙️ Now you'll add a restart policy and resource limits to your API service. The restart policy tells Docker to automatically restart the container if it crashes. Resource limits prevent a runaway process from consuming all available CPU or memory on your host machine. Together, these two settings make your services much more resilient.

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

> 🎙️ You've now covered the advanced features that make Docker Compose production-ready — environment management, health checks, profiles, restart policies, and resource limits. These are the tools that separate a quick demo from a robust deployment. Make sure to clean up with "docker compose down dash v" before submitting your work.

## Submission

Save a file named `Day_09_Output.md` in this folder containing terminal output and your `docker-compose.yml` and `.env` files.

### Grading Criteria

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
