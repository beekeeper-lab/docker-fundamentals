# Image Plan — Additions (Density Pass 2026-04-25)

**Style:** Head First book illustration — clean lines, slightly whimsical, warm colors, educational; matches the friendly-whale / shipping-container aesthetic of the existing 38 images
**Generator:** Google Gemini (gemini-3-pro-image-preview / Nano Banana Pro)
**Aspect ratio:** 16:9
**Background:** White

This file queues additional teaching-page illustrations to bring Docker Fundamentals in line with Gregg's "one image per teaching page" target. The existing 38 generated images cover module heroes and primary concept diagrams; this audit identified the per-Hands-On task pages that lack an inline illustration plus the module-intro page text that lives before the first H2. **Status: Queued — awaiting Gregg's approval before generation.**

`Submission` H2 sections are intentionally skipped — they are short rubric/checklist blocks.

---

## Module 00: What Is Docker?

#### m00-intro-overview
- **File**: `images/module-00/m00-intro-overview.png`
- **Page**: (intro/header)
- **Alt text**: A friendly day-zero welcome showing what Docker solves — "it works on my machine" jokes versus reproducible containerized apps
- **Status**: Queued
- **Goal**: Set the day's frame before the first H2.
- **Prompt**:
  Goal: editorial illustration for a programming textbook
  Scene: Two panels. Left "Without Docker" — a developer says "It works on my machine!" and a frustrated ops person looks at a different machine that's broken. Right "With Docker" — both machines run the same container labeled `python:3.12`, both work identically. A friendly Docker whale waves between them.
  Style: Head First book illustration style, clean lines, slightly whimsical and humorous, warm colors, educational
  Aspect ratio: 16:9
  Background: white
  Text in image: panel labels, machine speech bubbles
  Avoid: photorealistic, dark, scary, complex UI screenshots

#### m00-install-docker
- **File**: `images/module-00/m00-install-docker.png`
- **Page**: Install Docker
- **Alt text**: A friendly installer flow showing Docker Desktop on macOS and Windows, plus the Engine install on Linux
- **Status**: Queued
- **Goal**: Show the install paths students will follow today.
- **Prompt**:
  Goal: editorial illustration for a programming textbook
  Scene: Three install lanes. macOS — DMG file dragging into Applications. Windows — installer .exe with WSL2 callout. Linux — terminal showing `curl -fsSL https://get.docker.com | sh`. All three lead to a single running Docker whale ready to accept commands. A `docker --version` terminal at the bottom.
  Style: Head First book illustration style, clean lines, slightly whimsical and humorous, warm colors, educational
  Aspect ratio: 16:9
  Background: white
  Text in image: platform labels, install commands
  Avoid: photorealistic, dark, scary, complex UI screenshots

#### m00-explore-docker-commands
- **File**: `images/module-00/m00-explore-docker-commands.png`
- **Page**: Explore Docker Commands
- **Alt text**: A reference card showing the four most-used docker commands students will type today — version, info, run hello-world, ps
- **Status**: Queued
- **Goal**: Provide a one-page reference for the day's commands.
- **Prompt**:
  Goal: editorial illustration for a programming textbook
  Scene: A friendly cheat-sheet card with four labeled rows: `docker version` (whale + version tag), `docker info` (whale with stethoscope), `docker run hello-world` (whale carrying a tiny "hello!" gift), `docker ps` (whale checking a clipboard of running containers).
  Style: Head First book illustration style, clean lines, slightly whimsical and humorous, warm colors, educational
  Aspect ratio: 16:9
  Background: white
  Text in image: command names, brief captions
  Avoid: photorealistic, dark, scary, complex UI screenshots

## Module 01: Images and Containers

#### m01-intro-overview
- **File**: `images/module-01/m01-intro-overview.png`
- **Page**: (intro/header)
- **Alt text**: A welcoming module banner illustrating the image-vs-container distinction as a blueprint vs a running building
- **Status**: Queued
- **Goal**: Set up the central image-vs-container distinction at module start.
- **Prompt**:
  Goal: editorial illustration for a programming textbook
  Scene: An architect's blueprint labeled `docker image` on a drafting table; beside it, a fully-constructed building labeled `docker container` with people inside (running processes). An arrow `docker run` connects them.
  Style: Head First book illustration style, clean lines, slightly whimsical and humorous, warm colors, educational
  Aspect ratio: 16:9
  Background: white
  Text in image: image, container labels
  Avoid: photorealistic, dark, scary, complex UI screenshots

#### m01-tags-and-variants
- **File**: `images/module-01/m01-tags-and-variants.png`
- **Page**: Tags and Variants
- **Alt text**: A package on a shelf with multiple version tags showing how same-name images carry different tags like 3.12, slim, alpine
- **Status**: Queued
- **Goal**: Clarify that an image name + tag is the addressing scheme.
- **Prompt**:
  Goal: editorial illustration for a programming textbook
  Scene: A shelf of `python` boxes with different colored tags hanging off: `3.12`, `3.12-slim`, `3.12-alpine`, `latest`. A note: "tag = version + variant." A magnifying glass shows that `latest` is "whatever they pushed last — pin specific tags in production."
  Style: Head First book illustration style, clean lines, slightly whimsical and humorous, warm colors, educational
  Aspect ratio: 16:9
  Background: white
  Text in image: tag names, warning note
  Avoid: photorealistic, dark, scary, complex UI screenshots

#### m01-container-naming-listing
- **File**: `images/module-01/m01-container-naming-listing.png`
- **Page**: Container Naming and Listing
- **Alt text**: Multiple running containers each with a unique generated name and a custom name, listed in docker ps output
- **Status**: Queued
- **Goal**: Show how Docker auto-names containers and how to override.
- **Prompt**:
  Goal: editorial illustration for a programming textbook
  Scene: Four running containers with auto-generated tags (`pensive_einstein`, `fluffy_lovelace`) and one with a custom tag from `--name web`. A `docker ps` output table to the side lists them all with status columns.
  Style: Head First book illustration style, clean lines, slightly whimsical and humorous, warm colors, educational
  Aspect ratio: 16:9
  Background: white
  Text in image: container names, ps table headers
  Avoid: photorealistic, dark, scary, complex UI screenshots

## Module 02: Container Management

#### m02-intro-overview
- **File**: `images/module-02/m02-intro-overview.png`
- **Page**: (intro/header)
- **Alt text**: A welcoming module banner showing a fleet of containers being managed by a captain at a control panel
- **Status**: Queued
- **Goal**: Set up the day's frame — managing the lifecycle of running containers.
- **Prompt**:
  Goal: editorial illustration for a programming textbook
  Scene: A friendly captain (the operator) at a control panel labeled `docker`. Buttons: `start`, `stop`, `restart`, `logs`, `exec`. Several containers in the background respond to each button.
  Style: Head First book illustration style, clean lines, slightly whimsical and humorous, warm colors, educational
  Aspect ratio: 16:9
  Background: white
  Text in image: control panel buttons
  Avoid: photorealistic, dark, scary, complex UI screenshots

#### m02-start-stop-restart
- **File**: `images/module-02/m02-start-stop-restart.png`
- **Page**: Start, Stop, and Restart
- **Alt text**: A container's lifecycle states — created, running, paused, stopped — connected by arrows labeled with the matching docker commands
- **Status**: Queued
- **Goal**: Show the full state machine of a container.
- **Prompt**:
  Goal: editorial illustration for a programming textbook
  Scene: A state diagram. Boxes: `created`, `running`, `paused`, `exited`. Arrows: `docker start`, `docker stop`, `docker pause`, `docker unpause`, `docker restart`. Each container box has a small color-coded indicator.
  Style: Head First book illustration style, clean lines, slightly whimsical and humorous, warm colors, educational
  Aspect ratio: 16:9
  Background: white
  Text in image: state names, command labels
  Avoid: photorealistic, dark, scary, complex UI screenshots

#### m02-logs
- **File**: `images/module-02/m02-logs.png`
- **Page**: Logs
- **Alt text**: A container streaming stdout and stderr to the host's logs, with docker logs and -f follow mode shown
- **Status**: Queued
- **Goal**: Show how container output flows into the docker logs subsystem.
- **Prompt**:
  Goal: editorial illustration for a programming textbook
  Scene: A running container with two output streams (stdout green, stderr red) flowing into a logs cabinet. A terminal shows `docker logs -f web` tailing the stream live. A side note: "everything your app prints lives here."
  Style: Head First book illustration style, clean lines, slightly whimsical and humorous, warm colors, educational
  Aspect ratio: 16:9
  Background: white
  Text in image: stream labels, command line
  Avoid: photorealistic, dark, scary, complex UI screenshots

## Module 03: Dockerfiles (Part 1)

#### m03-intro-overview
- **File**: `images/module-03/m03-intro-overview.png`
- **Page**: (intro/header)
- **Alt text**: A welcoming module banner showing a Dockerfile recipe being baked into an image
- **Status**: Queued
- **Goal**: Set up the day's frame — recipe → image.
- **Prompt**:
  Goal: editorial illustration for a programming textbook
  Scene: A recipe card labeled `Dockerfile` going into a friendly oven labeled `docker build`. Out the other side: a freshly baked image with a tag. Steam rises in the shape of layers.
  Style: Head First book illustration style, clean lines, slightly whimsical and humorous, warm colors, educational
  Aspect ratio: 16:9
  Background: white
  Text in image: Dockerfile, build, image labels
  Avoid: photorealistic, dark, scary, complex UI screenshots

#### m03-your-first-dockerfile
- **File**: `images/module-03/m03-your-first-dockerfile.png`
- **Page**: Your First Dockerfile
- **Alt text**: A minimal Dockerfile dissected — FROM, WORKDIR, COPY, RUN, CMD — with each line annotated
- **Status**: Queued
- **Goal**: Single-page anatomy of a basic Dockerfile.
- **Prompt**:
  Goal: editorial illustration for a programming textbook
  Scene: A Dockerfile open: `FROM python:3.12-slim`, `WORKDIR /app`, `COPY . .`, `RUN pip install -r requirements.txt`, `CMD ["python", "app.py"]`. Each line has a callout: "base image," "set working dir," "copy source," "install deps," "default command."
  Style: Head First book illustration style, clean lines, slightly whimsical and humorous, warm colors, educational
  Aspect ratio: 16:9
  Background: white
  Text in image: Dockerfile lines, callouts
  Avoid: photorealistic, dark, scary, complex UI screenshots

#### m03-static-website
- **File**: `images/module-03/m03-static-website.png`
- **Page**: A Static Website
- **Alt text**: A static-site Dockerfile using nginx, copying HTML files into the image, and exposing port 80
- **Status**: Queued
- **Goal**: Walk through a real practical Dockerfile.
- **Prompt**:
  Goal: editorial illustration for a programming textbook
  Scene: A Dockerfile `FROM nginx:alpine`, `COPY ./site /usr/share/nginx/html`, `EXPOSE 80`. To the side: a phone browser hits `localhost:8080` and gets the static page. A diagram shows the host port mapping to the container port.
  Style: Head First book illustration style, clean lines, slightly whimsical and humorous, warm colors, educational
  Aspect ratio: 16:9
  Background: white
  Text in image: Dockerfile lines, port mapping
  Avoid: photorealistic, dark, scary, complex UI screenshots

## Module 04: Dockerfiles (Part 2)

#### m04-intro-overview
- **File**: `images/module-04/m04-intro-overview.png`
- **Page**: (intro/header)
- **Alt text**: A welcoming module banner introducing multi-stage builds and best practices for slim production images
- **Status**: Queued
- **Goal**: Set up the day's frame — making images smaller and safer.
- **Prompt**:
  Goal: editorial illustration for a programming textbook
  Scene: Two images side by side. Left "naive" — a giant container stuffed with build tools, source files, a compiler. Right "multi-stage" — a sleek, slim container holding only the compiled binary. A small chart: "10x smaller, 100x safer."
  Style: Head First book illustration style, clean lines, slightly whimsical and humorous, warm colors, educational
  Aspect ratio: 16:9
  Background: white
  Text in image: size comparison
  Avoid: photorealistic, dark, scary, complex UI screenshots

#### m04-multi-stage-builds
- **File**: `images/module-04/m04-multi-stage-builds.png`
- **Page**: Multi-Stage Builds
- **Alt text**: A two-stage Dockerfile with a builder stage compiling code and a runtime stage copying only the output, leaving build tools behind
- **Status**: Queued
- **Goal**: Show how multi-stage works mechanically.
- **Prompt**:
  Goal: editorial illustration for a programming textbook
  Scene: Two stacked stages. Top "builder" — heavy stage with compiler, source files, build tools. Bottom "runtime" — slim stage with only the compiled binary, copied via `COPY --from=builder /app/bin /app/bin`. A small note: "build tools never reach production."
  Style: Head First book illustration style, clean lines, slightly whimsical and humorous, warm colors, educational
  Aspect ratio: 16:9
  Background: white
  Text in image: stage labels, COPY --from
  Avoid: photorealistic, dark, scary, complex UI screenshots

## Module 05: Volumes and Persistence

#### m05-intro-overview
- **File**: `images/module-05/m05-intro-overview.png`
- **Page**: (intro/header)
- **Alt text**: A welcoming module banner showing data being saved outside the container so it survives container removal
- **Status**: Queued
- **Goal**: Set up the day's frame — containers are ephemeral, volumes are not.
- **Prompt**:
  Goal: editorial illustration for a programming textbook
  Scene: A container being removed (poof of smoke). Beside it, a glowing data box labeled `volume` survives. A small caption: "data outlives the container."
  Style: Head First book illustration style, clean lines, slightly whimsical and humorous, warm colors, educational
  Aspect ratio: 16:9
  Background: white
  Text in image: volume label, ephemeral container
  Avoid: photorealistic, dark, scary, complex UI screenshots

#### m05-named-volumes
- **File**: `images/module-05/m05-named-volumes.png`
- **Page**: Named Volumes
- **Alt text**: A named volume created with docker volume create, mounted into multiple containers as the same persistent storage
- **Status**: Queued
- **Goal**: Show how named volumes are sharable storage.
- **Prompt**:
  Goal: editorial illustration for a programming textbook
  Scene: A friendly storage cabinet labeled `db_data` (named volume). Two containers (`postgres-1`, `postgres-2`) connect to it via mount lines `-v db_data:/var/lib/postgresql/data`. Both see the same data.
  Style: Head First book illustration style, clean lines, slightly whimsical and humorous, warm colors, educational
  Aspect ratio: 16:9
  Background: white
  Text in image: volume name, mount syntax
  Avoid: photorealistic, dark, scary, complex UI screenshots

#### m05-volume-management
- **File**: `images/module-05/m05-volume-management.png`
- **Page**: Volume Management
- **Alt text**: A docker volume command reference — ls, create, inspect, rm, prune — with each command's effect visualized
- **Status**: Queued
- **Goal**: Provide a one-page reference for volume management.
- **Prompt**:
  Goal: editorial illustration for a programming textbook
  Scene: A control panel with five buttons: `volume ls` (lists), `volume create` (adds), `volume inspect` (magnifying glass), `volume rm` (trashes), `volume prune` (broom sweeps unused). Each button shows its effect on a row of cabinets.
  Style: Head First book illustration style, clean lines, slightly whimsical and humorous, warm colors, educational
  Aspect ratio: 16:9
  Background: white
  Text in image: command names, captions
  Avoid: photorealistic, dark, scary, complex UI screenshots

## Module 06: Networking

#### m06-intro-overview
- **File**: `images/module-06/m06-intro-overview.png`
- **Page**: (intro/header)
- **Alt text**: A welcoming module banner showing containers on a private bridge network communicating by name
- **Status**: Queued
- **Goal**: Set up the day's frame — Docker networks isolate and connect.
- **Prompt**:
  Goal: editorial illustration for a programming textbook
  Scene: A bridge labeled `bridge network` with three containers connected: `web`, `api`, `db`. Speech bubbles: web says "GET /users to api:8000", api says "SELECT to db:5432". A side note: "containers find each other by name on the same network."
  Style: Head First book illustration style, clean lines, slightly whimsical and humorous, warm colors, educational
  Aspect ratio: 16:9
  Background: white
  Text in image: network name, container names
  Avoid: photorealistic, dark, scary, complex UI screenshots

#### m06-multi-container-application
- **File**: `images/module-06/m06-multi-container-application.png`
- **Page**: Multi-Container Application
- **Alt text**: A web + api + db three-tier setup running across three containers with named connections between them
- **Status**: Queued
- **Goal**: Show a real three-tier app on Docker networks.
- **Prompt**:
  Goal: editorial illustration for a programming textbook
  Scene: Three containers labeled `frontend`, `backend`, `postgres`, all on a custom network labeled `app-net`. Connections: frontend → backend (HTTP), backend → postgres (TCP). A user's browser hits the frontend port from the host.
  Style: Head First book illustration style, clean lines, slightly whimsical and humorous, warm colors, educational
  Aspect ratio: 16:9
  Background: white
  Text in image: container names, connection labels
  Avoid: photorealistic, dark, scary, complex UI screenshots

#### m06-cleanup
- **File**: `images/module-06/m06-cleanup.png`
- **Page**: Cleanup
- **Alt text**: A cleanup scene with docker container prune, image prune, volume prune, and network prune sweeping unused resources
- **Status**: Queued
- **Goal**: Anchor the cleanup commands students will run today.
- **Prompt**:
  Goal: editorial illustration for a programming textbook
  Scene: A janitor robot labeled `docker prune` sweeping four piles labeled `containers`, `images`, `volumes`, `networks`. Each command has a one-liner: `docker container prune`, `docker image prune`, `docker volume prune`, `docker network prune`.
  Style: Head First book illustration style, clean lines, slightly whimsical and humorous, warm colors, educational
  Aspect ratio: 16:9
  Background: white
  Text in image: prune commands
  Avoid: photorealistic, dark, scary, complex UI screenshots

## Module 07: Docker Compose (Part 1)

#### m07-intro-overview
- **File**: `images/module-07/m07-intro-overview.png`
- **Page**: (intro/header)
- **Alt text**: A welcoming module banner showing docker-compose.yml as a single file describing many containers and their wiring
- **Status**: Queued
- **Goal**: Set up the day's frame — Compose declares the whole stack.
- **Prompt**:
  Goal: editorial illustration for a programming textbook
  Scene: A `docker-compose.yml` file blueprint. From it, three labeled services (`web`, `api`, `db`) emerge as containers, all connected on a network and sharing volumes. A small caption: "one file, one stack."
  Style: Head First book illustration style, clean lines, slightly whimsical and humorous, warm colors, educational
  Aspect ratio: 16:9
  Background: white
  Text in image: compose file, service names
  Avoid: photorealistic, dark, scary, complex UI screenshots

#### m07-first-compose-file
- **File**: `images/module-07/m07-first-compose-file.png`
- **Page**: Your First Compose File
- **Alt text**: A minimal docker-compose.yml with a single service, dissected with annotations on services, image, ports, and volumes
- **Status**: Queued
- **Goal**: Anatomy of the first Compose file.
- **Prompt**:
  Goal: editorial illustration for a programming textbook
  Scene: A YAML file open: `services: > web: > image: nginx > ports: > "8080:80" > volumes: > "./site:/usr/share/nginx/html"`. Each block has a callout label.
  Style: Head First book illustration style, clean lines, slightly whimsical and humorous, warm colors, educational
  Aspect ratio: 16:9
  Background: white
  Text in image: YAML keys, callouts
  Avoid: photorealistic, dark, scary, complex UI screenshots

#### m07-multi-service-application
- **File**: `images/module-07/m07-multi-service-application.png`
- **Page**: Multi-Service Application
- **Alt text**: A docker-compose.yml describing a web + api + postgres stack with depends_on edges
- **Status**: Queued
- **Goal**: Show a realistic multi-service Compose file.
- **Prompt**:
  Goal: editorial illustration for a programming textbook
  Scene: A YAML file with three services `web`, `api`, `db`. Arrows in the file show `depends_on`. To the side: a `docker compose up` runs the whole stack with one command.
  Style: Head First book illustration style, clean lines, slightly whimsical and humorous, warm colors, educational
  Aspect ratio: 16:9
  Background: white
  Text in image: service names, depends_on
  Avoid: photorealistic, dark, scary, complex UI screenshots

## Module 08: Docker Compose (Part 2)

#### m08-intro-overview
- **File**: `images/module-08/m08-intro-overview.png`
- **Page**: (intro/header)
- **Alt text**: A welcoming module banner showing environment variables and .env files driving Compose configuration
- **Status**: Queued
- **Goal**: Set up the day's frame — config and secrets via env.
- **Prompt**:
  Goal: editorial illustration for a programming textbook
  Scene: A friendly robot reads a `.env` file and pours the values into placeholders inside a `compose.yml`. Side note: "twelve-factor: config from the environment."
  Style: Head First book illustration style, clean lines, slightly whimsical and humorous, warm colors, educational
  Aspect ratio: 16:9
  Background: white
  Text in image: .env, compose.yml
  Avoid: photorealistic, dark, scary, complex UI screenshots

#### m08-environment-variables-env-files
- **File**: `images/module-08/m08-environment-variables-env-files.png`
- **Page**: Environment Variables and .env Files
- **Alt text**: Three layers of environment variable resolution — shell, .env file, and compose.yml — with precedence labeled
- **Status**: Queued
- **Goal**: Disambiguate where env vars come from in Compose.
- **Prompt**:
  Goal: editorial illustration for a programming textbook
  Scene: A precedence ladder. Top: shell env vars (highest priority). Middle: `.env` file in project root. Bottom: `environment:` block in `compose.yml`. Each rung labeled with a small example. A note: "shell wins ties."
  Style: Head First book illustration style, clean lines, slightly whimsical and humorous, warm colors, educational
  Aspect ratio: 16:9
  Background: white
  Text in image: precedence ladder
  Avoid: photorealistic, dark, scary, complex UI screenshots

## Module 09: Docker Hub and Registries

#### m09-intro-overview
- **File**: `images/module-09/m09-intro-overview.png`
- **Page**: (intro/header)
- **Alt text**: A welcoming module banner showing Docker Hub as a global registry with developers pushing and pulling images
- **Status**: Queued
- **Goal**: Set up the day's frame — registries are where images live.
- **Prompt**:
  Goal: editorial illustration for a programming textbook
  Scene: A central building labeled "Docker Hub." Developers around the world push their images in (`docker push`) and pull others' images down (`docker pull`). A side panel lists alternatives: GitHub Container Registry, AWS ECR, Google Artifact Registry.
  Style: Head First book illustration style, clean lines, slightly whimsical and humorous, warm colors, educational
  Aspect ratio: 16:9
  Background: white
  Text in image: registry names
  Avoid: photorealistic, dark, scary, complex UI screenshots

#### m09-docker-hub-account
- **File**: `images/module-09/m09-docker-hub-account.png`
- **Page**: Docker Hub Account
- **Alt text**: A Docker Hub signup flow showing username creation, login from CLI, and the personal namespace
- **Status**: Queued
- **Goal**: Walk through account setup so students can publish.
- **Prompt**:
  Goal: editorial illustration for a programming textbook
  Scene: A signup card showing a chosen username. A terminal below shows `docker login` succeeding. A folder labeled `username/` appears as the personal namespace where images will live.
  Style: Head First book illustration style, clean lines, slightly whimsical and humorous, warm colors, educational
  Aspect ratio: 16:9
  Background: white
  Text in image: username, login command
  Avoid: photorealistic, dark, scary, complex UI screenshots

#### m09-build-tag-push
- **File**: `images/module-09/m09-build-tag-push.png`
- **Page**: Build, Tag, and Push
- **Alt text**: The three-step publish workflow — docker build, docker tag, docker push — with the resulting image visible on Docker Hub
- **Status**: Queued
- **Goal**: Cement the publish workflow in one image.
- **Prompt**:
  Goal: editorial illustration for a programming textbook
  Scene: Three numbered panels. 1) `docker build -t myapp .`. 2) `docker tag myapp campbellreed/myapp:1.0`. 3) `docker push campbellreed/myapp:1.0`. Final panel: the image appears in the user's Docker Hub repo.
  Style: Head First book illustration style, clean lines, slightly whimsical and humorous, warm colors, educational
  Aspect ratio: 16:9
  Background: white
  Text in image: command lines, panel numbers
  Avoid: photorealistic, dark, scary, complex UI screenshots

#### m09-pull-and-run-from-hub
- **File**: `images/module-09/m09-pull-and-run-from-hub.png`
- **Page**: Pull and Run from Docker Hub
- **Alt text**: Another developer pulling the previously pushed image and running it on their machine, demonstrating distribution
- **Status**: Queued
- **Goal**: Show the consumer side of distribution.
- **Prompt**:
  Goal: editorial illustration for a programming textbook
  Scene: A second developer on a different machine runs `docker run campbellreed/myapp:1.0`. The image is pulled from Docker Hub and starts running. Both machines show the same output. A speech bubble: "no install dance."
  Style: Head First book illustration style, clean lines, slightly whimsical and humorous, warm colors, educational
  Aspect ratio: 16:9
  Background: white
  Text in image: pull command, output
  Avoid: photorealistic, dark, scary, complex UI screenshots

---

## Summary

- **Total queued images**: 29
- **Modules affected**: 10 (every module 00-09)
- **Pages-without-images covered**: 29 — the 10 module-intro pages (the text before the first H2) plus 19 Hands-On task pages that lacked an inline image
- **Note**: `Submission` H2 sections are intentionally not illustrated — they are short procedural rubric blocks.
