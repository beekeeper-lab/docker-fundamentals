# Image Plan

Total images: 38 (all generated)

## Generation Cost Log

| Metric | Value |
|--------|-------|
| Model | `gemini-3-pro-image-preview` (Nano Banana Pro) |
| Images generated | 38 |
| Total tokens | 74,262 |
| Average tokens/image | 1,954 |
| Total generation time | 835s (22.0s avg per image) |
| **Estimated total cost** | **$5.20** |
| Cost per image | ~$0.14 |
| Generated on | 2026-04-09 |

---

## Module 00: What Is Docker

### Image 1: hero-docker-world
- **File**: `images/module-00/hero-docker-world.png`
- **Page**: 1 (What Is Docker?)
- **Placement**: after the H2 heading, before narration block
- **Description**: A friendly whale (Docker mascot style) carrying colorful shipping containers on its back, sailing across a calm ocean toward a harbor full of servers. Sets the tone for the course — Docker makes shipping software easy and fun.
- **Status**: Generated
- **Prompt**:
  Goal: editorial illustration for a programming textbook
  Scene: A friendly cartoon whale carrying colorful shipping containers on its back, sailing across a calm ocean toward a harbor. The containers are labeled with tiny icons representing apps (a gear, a flask, a database cylinder). The harbor has small server buildings. The mood is optimistic and adventurous.
  Style: Head First book illustration style, clean lines, slightly whimsical and humorous, warm colors, educational
  Aspect ratio: 16:9
  Background: white
  Text in image: minimal or none
  Avoid: photorealistic, dark, scary, complex UI screenshots

### Image 2: containers-vs-vms
- **File**: `images/module-00/containers-vs-vms.png`
- **Page**: 2 (Containers vs Virtual Machines)
- **Placement**: after the comparison table
- **Description**: Side-by-side architectural comparison showing a VM stack (hardware → hypervisor → full guest OS → app) versus a container stack (hardware → host OS → Docker engine → apps sharing the kernel). The VM side looks heavy and tall, the container side looks light and compact. Helps students immediately grasp why containers are faster and smaller.
- **Status**: Generated
- **Prompt**:
  Goal: editorial illustration for a programming textbook
  Scene: Side-by-side comparison of two architectural stacks. Left side labeled "Virtual Machine": tall heavy stack with layers for Hardware, Hypervisor, Guest OS (shown as a thick heavy block), and a small App on top. Right side labeled "Container": shorter lighter stack with Hardware, Host OS, Docker Engine (thin layer), and multiple small App boxes sitting directly on it. The VM side looks heavy and overloaded, the container side looks nimble and efficient. Use visual weight and color to emphasize the difference.
  Style: Head First book illustration style, clean lines, slightly whimsical and humorous, warm colors, educational
  Aspect ratio: 16:9
  Background: white
  Text in image: minimal labels only (VM, Container, OS, App)
  Avoid: photorealistic, dark, scary, complex UI screenshots

### Image 3: docker-architecture
- **File**: `images/module-00/docker-architecture.png`
- **Page**: 3 (Docker Architecture)
- **Placement**: after the ASCII architecture diagram
- **Description**: Flow diagram showing a developer at a terminal (Docker CLI) sending commands to the Docker Daemon (shown as a friendly engine), which manages a library of Images (blueprints) and running Containers (active instances). Reinforces the client-server model and the class/object metaphor.
- **Status**: Generated
- **Prompt**:
  Goal: editorial illustration for a programming textbook
  Scene: A developer sitting at a laptop labeled "Docker CLI" with a speech bubble saying a command. An arrow goes to a friendly engine character labeled "Docker Daemon." The daemon has two shelves: one with blueprint documents labeled "Images" and one with small running machines labeled "Containers." An arrow shows an image being used to create a container. The mood is friendly and explanatory.
  Style: Head First book illustration style, clean lines, slightly whimsical and humorous, warm colors, educational
  Aspect ratio: 16:9
  Background: white
  Text in image: minimal labels (CLI, Daemon, Images, Containers)
  Avoid: photorealistic, dark, scary, complex UI screenshots

### Image 4: container-ephemeral
- **File**: `images/module-00/container-ephemeral.png`
- **Page**: 6 (Run a Real Container)
- **Placement**: after the isolation demonstration (Task G)
- **Description**: Two identical containers side by side. The first has curl installed (shown as a small package icon inside). The second is brand new from the same image with no curl — a question mark where the package would be. Shows that containers start fresh each time and changes don't persist.
- **Status**: Generated
- **Prompt**:
  Goal: editorial illustration for a programming textbook
  Scene: Two identical shipping containers side by side, both created from the same blueprint image above them. Container 1 has a small "curl" package icon inside it with a checkmark. Container 2 is freshly created and empty inside, with a question mark where the package would be. A speech bubble from Container 2 says "curl? never heard of it." An arrow shows Container 1 being removed and Container 2 starting fresh.
  Style: Head First book illustration style, clean lines, slightly whimsical and humorous, warm colors, educational
  Aspect ratio: 16:9
  Background: white
  Text in image: minimal labels
  Avoid: photorealistic, dark, scary, complex UI screenshots

### Image 5: port-mapping
- **File**: `images/module-00/port-mapping.png`
- **Page**: 7 (Running a Web Server)
- **Placement**: after the Nginx run command
- **Description**: Diagram showing a laptop (host machine) with port 8080 connected via a bridge/tunnel to a container with port 80 and an Nginx logo inside. A browser window shows the Nginx welcome page. Clarifies the host:container port mapping concept.
- **Status**: Generated
- **Prompt**:
  Goal: editorial illustration for a programming textbook
  Scene: A laptop on the left with "Port 8080" labeled on it. A colorful bridge or tunnel connects it to a shipping container on the right with "Port 80" labeled on it and an Nginx logo inside. A small browser window floats above the laptop showing a welcome page. Arrows show the request flowing from browser to host port to container port. The bridge is labeled "-p 8080:80".
  Style: Head First book illustration style, clean lines, slightly whimsical and humorous, warm colors, educational
  Aspect ratio: 16:9
  Background: white
  Text in image: port numbers and -p flag label
  Avoid: photorealistic, dark, scary, complex UI screenshots

---

## Module 01: Images and Containers

### Image 1: hero-image-layers
- **File**: `images/module-01/hero-image-layers.png`
- **Page**: 1 (Docker Images)
- **Placement**: after the H2 heading
- **Description**: A stack of transparent layers forming a Docker image, like a layer cake or geological cross-section. Each layer is labeled with what it adds (base OS, Python, pip packages, app code). Sets the visual metaphor for the entire module.
- **Status**: Generated
- **Prompt**:
  Goal: editorial illustration for a programming textbook
  Scene: A tall stack of semi-transparent colorful layers, like a geological cross-section or fancy layer cake. Bottom layer is thick and labeled "Base OS (Debian)", middle layers are progressively thinner labeled "Python Runtime", "pip packages", and top thin layer labeled "Your App Code." A magnifying glass examines one layer. The stack has a tag hanging off it reading "python:3.12-slim". The mood is curious and educational.
  Style: Head First book illustration style, clean lines, slightly whimsical and humorous, warm colors, educational
  Aspect ratio: 16:9
  Background: white
  Text in image: layer labels
  Avoid: photorealistic, dark, scary, complex UI screenshots

### Image 2: image-size-comparison
- **File**: `images/module-01/image-size-comparison.png`
- **Page**: 3 (Pulling Images)
- **Placement**: after the size comparison list
- **Description**: Three Python image boxes of dramatically different sizes — full (huge crate), slim (medium box), and alpine (tiny package). Size labels show 1GB, 150MB, 50MB. Makes the size difference viscerally clear.
- **Status**: Generated
- **Prompt**:
  Goal: editorial illustration for a programming textbook
  Scene: Three shipping crates in a row, all labeled "Python 3.12" but dramatically different sizes. Left: an enormous crate labeled "full" with "~1 GB" and overflowing with tools. Middle: a medium box labeled "slim" with "~150 MB" looking tidy. Right: a tiny compact package labeled "alpine" with "~50 MB" looking minimal and sleek. A developer character looks between them with a thought bubble showing a balance scale weighing size vs features.
  Style: Head First book illustration style, clean lines, slightly whimsical and humorous, warm colors, educational
  Aspect ratio: 16:9
  Background: white
  Text in image: size labels and variant names
  Avoid: photorealistic, dark, scary, complex UI screenshots

### Image 3: multiple-versions
- **File**: `images/module-01/multiple-versions.png`
- **Page**: 4 (Running Containers from Different Images)
- **Placement**: after the side-by-side Python versions demo
- **Description**: Three containers running simultaneously on one machine — Python 3.12, Python 3.11, and Node.js 20 — each in its own isolated box with no conflicts. Shows Docker's superpower of parallel version isolation.
- **Status**: Generated
- **Prompt**:
  Goal: editorial illustration for a programming textbook
  Scene: A single laptop or server at the bottom. Three containers float above it, each with a different language logo and version: Python 3.12 (blue), Python 3.11 (slightly different blue), Node.js 20 (green). Each container has a happy face and they wave at each other but have clear walls between them. A speech bubble says "No conflicts!" The mood is cheerful, showing peaceful coexistence.
  Style: Head First book illustration style, clean lines, slightly whimsical and humorous, warm colors, educational
  Aspect ratio: 16:9
  Background: white
  Text in image: version labels
  Avoid: photorealistic, dark, scary, complex UI screenshots

### Image 4: container-flags
- **File**: `images/module-01/container-flags.png`
- **Page**: 6 (Running Containers with Options)
- **Placement**: after the environment variables task
- **Description**: A container with control knobs and switches on its side, each labeled with a flag: -e (environment), --rm (auto-cleanup), -w (working directory), -d (detached), -p (ports). Shows that containers are configurable at runtime.
- **Status**: Generated
- **Prompt**:
  Goal: editorial illustration for a programming textbook
  Scene: A shipping container with a control panel on its side, like a mixing board or dashboard. Each knob or switch is labeled with a Docker flag: "-e" (environment dial), "--rm" (self-destruct toggle), "-w" (working directory compass), "-d" (background/detach switch), "-p" (port mapping slider). A developer adjusts the knobs with a thoughtful expression. The mood is playful and empowering.
  Style: Head First book illustration style, clean lines, slightly whimsical and humorous, warm colors, educational
  Aspect ratio: 16:9
  Background: white
  Text in image: flag labels on knobs
  Avoid: photorealistic, dark, scary, complex UI screenshots

---

## Module 02: Container Management

### Image 1: hero-lifecycle
- **File**: `images/module-02/hero-lifecycle.png`
- **Page**: 1 (Container Lifecycle)
- **Placement**: after the ASCII lifecycle diagram
- **Description**: A colorful state machine diagram showing container states as stations on a circular track: Created, Running, Paused, Stopped, Removed. Trains (containers) move between stations with labeled signals (start, stop, pause, kill, rm). Replaces the hard-to-read ASCII diagram with a memorable visual.
- **Status**: Generated
- **Prompt**:
  Goal: editorial illustration for a programming textbook
  Scene: A circular railway track with stations at different points. Stations are labeled: "Created" (starting station), "Running" (busy active station with green light), "Paused" (frozen station with snowflake), "Stopped" (red light station), "Removed" (exit gate). Small train cars (containers) move between stations. Track segments are labeled with commands: start, stop, pause, unpause, kill, restart, rm. The mood is playful and organized.
  Style: Head First book illustration style, clean lines, slightly whimsical and humorous, warm colors, educational
  Aspect ratio: 16:9
  Background: white
  Text in image: state names and command labels
  Avoid: photorealistic, dark, scary, complex UI screenshots

### Image 2: docker-exec
- **File**: `images/module-02/docker-exec.png`
- **Page**: 4 (Executing Commands in Running Containers)
- **Placement**: after the exec introduction
- **Description**: A running container with a side door. A developer reaches in through the door to run commands inside without stopping the container. The container keeps running happily while being inspected. Illustrates that exec is non-disruptive.
- **Status**: Generated
- **Prompt**:
  Goal: editorial illustration for a programming textbook
  Scene: A running shipping container with an engine humming (motion lines). A side access door is open, and a developer reaches inside with a wrench and magnifying glass. Inside the container you can see files, processes, and a terminal. The container keeps running with a green status light. A label says "docker exec" on the door. The mood is practical and reassuring — you can inspect without breaking things.
  Style: Head First book illustration style, clean lines, slightly whimsical and humorous, warm colors, educational
  Aspect ratio: 16:9
  Background: white
  Text in image: "docker exec" label
  Avoid: photorealistic, dark, scary, complex UI screenshots

### Image 3: docker-cp
- **File**: `images/module-02/docker-cp.png`
- **Page**: 5 (Copying Files)
- **Placement**: after the copy introduction
- **Description**: Bidirectional file transfer between host and container. A laptop on the left and a container on the right, with files flying in both directions along labeled arrows (docker cp host→container, docker cp container→host).
- **Status**: Generated
- **Prompt**:
  Goal: editorial illustration for a programming textbook
  Scene: A laptop on the left labeled "Host" and a shipping container on the right labeled "Container." Files (shown as paper documents with icons) fly between them on two curved arrows. Top arrow goes left-to-right labeled "docker cp file container:/path" and bottom arrow goes right-to-left labeled "docker cp container:/path file." The mood is dynamic, showing easy file exchange.
  Style: Head First book illustration style, clean lines, slightly whimsical and humorous, warm colors, educational
  Aspect ratio: 16:9
  Background: white
  Text in image: direction labels
  Avoid: photorealistic, dark, scary, complex UI screenshots

### Image 4: system-cleanup
- **File**: `images/module-02/system-cleanup.png`
- **Page**: 6 (Bulk Operations)
- **Placement**: after docker system df
- **Description**: A cluttered Docker workspace being cleaned up. Stopped containers, dangling images, and unused networks shown as clutter being swept away by docker system prune. A clean workspace emerges. Motivates good cleanup habits.
- **Status**: Generated
- **Prompt**:
  Goal: editorial illustration for a programming textbook
  Scene: Split scene. Left side: a messy workshop with stopped containers (boxes with X marks), dangling images (faded blueprints), unused networks (disconnected cables) piled up. A gauge shows "disk usage: HIGH." Right side: the same workshop after cleanup, tidy and organized, gauge shows "disk usage: LOW." A broom labeled "docker system prune" sweeps between the two sides. The mood is satisfying, like a before/after cleaning.
  Style: Head First book illustration style, clean lines, slightly whimsical and humorous, warm colors, educational
  Aspect ratio: 16:9
  Background: white
  Text in image: "before" and "after" labels
  Avoid: photorealistic, dark, scary, complex UI screenshots

---

## Module 03: Dockerfiles Part 1

### Image 1: hero-dockerfile-recipe
- **File**: `images/module-03/hero-dockerfile-recipe.png`
- **Page**: 1 (Dockerfile Basics)
- **Placement**: after the H2 heading
- **Description**: A Dockerfile shown as a recipe card in a kitchen. Each instruction (FROM, WORKDIR, COPY, RUN, CMD) is a step in the recipe. A chef (developer) follows the recipe to bake an image (shown as a finished cake coming out of an oven labeled "docker build"). Sets up the recipe metaphor for the module.
- **Status**: Generated
- **Prompt**:
  Goal: editorial illustration for a programming textbook
  Scene: A kitchen scene where a developer wearing a chef hat holds a recipe card labeled "Dockerfile." The recipe has steps: FROM (pick a base ingredient), COPY (add your ingredients), RUN (mix and cook), CMD (serve). An oven labeled "docker build" has a finished layer cake labeled "my-app:1.0" coming out of it. The mood is warm, creative, and approachable.
  Style: Head First book illustration style, clean lines, slightly whimsical and humorous, warm colors, educational
  Aspect ratio: 16:9
  Background: white
  Text in image: instruction labels on recipe steps
  Avoid: photorealistic, dark, scary, complex UI screenshots

### Image 2: layer-caching
- **File**: `images/module-03/layer-caching.png`
- **Page**: 3 (A Web Application)
- **Placement**: after the "Key detail" about requirements.txt ordering
- **Description**: Two rebuild scenarios side by side. Left: requirements.txt copied after app code — changing app.py forces pip install to rerun. Right: requirements.txt copied first — changing app.py skips pip install (cached). Shows the dramatic speed difference from proper ordering.
- **Status**: Generated
- **Prompt**:
  Goal: editorial illustration for a programming textbook
  Scene: Two build pipelines side by side. Left pipeline labeled "Slow Rebuild": layers stack up with ALL layers rebuilding (red flashing), a clock shows 2 minutes. Right pipeline labeled "Fast Rebuild": bottom layers show "CACHED" stamps (green checkmarks), only the top app layer rebuilds, clock shows 5 seconds. The key difference highlighted: "Copy requirements FIRST, app code LAST." A developer on the right looks happy, developer on left looks impatient.
  Style: Head First book illustration style, clean lines, slightly whimsical and humorous, warm colors, educational
  Aspect ratio: 16:9
  Background: white
  Text in image: CACHED labels, time indicators
  Avoid: photorealistic, dark, scary, complex UI screenshots

### Image 3: three-apps
- **File**: `images/module-03/three-apps.png`
- **Page**: 5 (Understanding the Build Process)
- **Placement**: after listing custom images
- **Description**: Three completed Docker images displayed as trophies or products: a Python CLI app, a Flask web server, and an Nginx static site. Shows the progression and variety of what you can containerize.
- **Status**: Generated
- **Prompt**:
  Goal: editorial illustration for a programming textbook
  Scene: A display shelf with three completed Docker images shown as product boxes. Left: "hello-docker:1.0" with a Python snake logo and "CLI App" label. Middle: "flask-app:1.0" with a flask/beaker icon and "Web API" label. Right: "my-site:1.0" with an Nginx logo and "Static Site" label. A developer stands proudly in front of the shelf. A banner reads "You built these!" The mood is celebratory and encouraging.
  Style: Head First book illustration style, clean lines, slightly whimsical and humorous, warm colors, educational
  Aspect ratio: 16:9
  Background: white
  Text in image: image names and type labels
  Avoid: photorealistic, dark, scary, complex UI screenshots

---

## Module 04: Dockerfiles Part 2

### Image 1: hero-multistage
- **File**: `images/module-04/hero-multistage.png`
- **Page**: 1 (Layer Optimization)
- **Placement**: after the H2 heading
- **Description**: A factory assembly line with two stages. Stage 1 is a messy workshop with heavy tools (compiler, JDK, build tools). Stage 2 is a clean showroom with only the finished product. A conveyor belt moves just the compiled binary from stage 1 to stage 2, leaving all the build tools behind.
- **Status**: Generated
- **Prompt**:
  Goal: editorial illustration for a programming textbook
  Scene: A factory with two rooms connected by a conveyor belt. Room 1 "Build Stage" is messy with heavy tools, compilers, source code papers scattered around. A large crate labeled "500 MB" sits there. The conveyor belt carries only a tiny package (the compiled binary) to Room 2 "Runtime Stage" which is clean, minimal, and organized. A small box labeled "50 MB" sits there. The mood is clever and efficient — leave the mess behind, ship only what matters.
  Style: Head First book illustration style, clean lines, slightly whimsical and humorous, warm colors, educational
  Aspect ratio: 16:9
  Background: white
  Text in image: stage labels and size comparisons
  Avoid: photorealistic, dark, scary, complex UI screenshots

### Image 2: dockerignore
- **File**: `images/module-04/dockerignore.png`
- **Page**: 3 (.dockerignore)
- **Placement**: after the .dockerignore file example
- **Description**: A project folder with files color-coded green (included: app.py, requirements.txt) and red (excluded: .git, .env, __pycache__, node_modules). A bouncer at the "docker build" gate checks each file against the .dockerignore list, letting only green files through.
- **Status**: Generated
- **Prompt**:
  Goal: editorial illustration for a programming textbook
  Scene: A project folder spilling out files. A bouncer character stands at a gate labeled "docker build." Files approach the gate: app.py and requirements.txt (green, smiling) get waved through. Files like .env (with a SECRET stamp), .git (heavy folder), __pycache__ (dusty), and node_modules (enormous) are blocked with a red hand. The bouncer holds a clipboard labeled ".dockerignore." The mood is humorous security — keeping the riffraff out.
  Style: Head First book illustration style, clean lines, slightly whimsical and humorous, warm colors, educational
  Aspect ratio: 16:9
  Background: white
  Text in image: file names on the files
  Avoid: photorealistic, dark, scary, complex UI screenshots

### Image 3: best-practices
- **File**: `images/module-04/best-practices.png`
- **Page**: 4 (Best Practices)
- **Placement**: after the best practices Dockerfile
- **Description**: An annotated Dockerfile shown as a blueprint with callout bubbles highlighting each best practice: specific tag, non-root USER, cache-friendly COPY order, --no-cache-dir, PYTHONDONTWRITEBYTECODE, EXPOSE documentation.
- **Status**: Generated
- **Prompt**:
  Goal: editorial illustration for a programming textbook
  Scene: A large blueprint-style document showing a Dockerfile. Callout bubbles with icons point to different lines: a pin icon at "FROM python:3.12-slim" says "Specific tag, not latest"; a shield icon at "USER appuser" says "Non-root for security"; a rocket icon at the COPY order says "Dependencies first for caching"; a broom icon at "--no-cache-dir" says "Keep image clean." The mood is professional and thorough — a pre-flight checklist.
  Style: Head First book illustration style, clean lines, slightly whimsical and humorous, warm colors, educational
  Aspect ratio: 16:9
  Background: white
  Text in image: callout text for each practice
  Avoid: photorealistic, dark, scary, complex UI screenshots

---

## Module 05: Volumes and Persistence

### Image 1: hero-persistence
- **File**: `images/module-05/hero-persistence.png`
- **Page**: 1 (Why Volumes Matter)
- **Placement**: after the H2 heading
- **Description**: Two scenes side by side. Left: a container is destroyed and its data (files, database records) falls into a void — "Data lost!" Right: a container is destroyed but a volume (shown as a safe or vault) keeps the data intact — "Data safe!" Immediately establishes why volumes matter.
- **Status**: Generated
- **Prompt**:
  Goal: editorial illustration for a programming textbook
  Scene: Split scene. Left panel labeled "Without Volume": a container explodes and documents, database records, and files fall into a dark void. A speech bubble cries "My data!" Right panel labeled "With Volume": the same container explodes but all the data is safely stored in a glowing vault/safe labeled "Volume" that stands independently. A speech bubble says "Still here!" The mood contrasts loss with security.
  Style: Head First book illustration style, clean lines, slightly whimsical and humorous, warm colors, educational
  Aspect ratio: 16:9
  Background: white
  Text in image: "Without Volume" / "With Volume" labels
  Avoid: photorealistic, dark, scary, complex UI screenshots

### Image 2: volumes-vs-binds
- **File**: `images/module-05/volumes-vs-binds.png`
- **Page**: 1 (Why Volumes Matter)
- **Placement**: after the comparison table
- **Description**: Named volume shown as a Docker-managed storage locker (location hidden, Docker handles it) versus bind mount shown as a direct cable from a specific host folder into the container. Clarifies the architectural difference between the two persistence approaches.
- **Status**: Generated
- **Prompt**:
  Goal: editorial illustration for a programming textbook
  Scene: Two setups side by side. Left "Named Volume": Docker engine manages a storage locker behind the scenes, container connects to it with a clean interface, developer doesn't see where data lives. Right "Bind Mount": a visible cable runs from a specific folder on the developer's laptop directly into the container, files are visible and editable on both sides. Labels highlight key differences: "Docker manages" vs "You manage", "Production" vs "Development."
  Style: Head First book illustration style, clean lines, slightly whimsical and humorous, warm colors, educational
  Aspect ratio: 16:9
  Background: white
  Text in image: type labels and key differences
  Avoid: photorealistic, dark, scary, complex UI screenshots

### Image 3: live-editing
- **File**: `images/module-05/live-editing.png`
- **Page**: 3 (Bind Mounts)
- **Placement**: after the live editing demonstration
- **Description**: A developer editing an HTML file on their laptop while a container running Nginx instantly reflects the change. No rebuild step, no restart — the change flows through the bind mount in real time.
- **Status**: Generated
- **Prompt**:
  Goal: editorial illustration for a programming textbook
  Scene: A developer types on a laptop, editing index.html. A glowing connection (bind mount) links the laptop's folder to a running Nginx container. The container's web page updates instantly — shown as a browser window changing from "Hello" to "Updated!" in real-time. A clock icon shows "0 seconds" for the update. No rebuild or restart step visible. The mood is magical and productive.
  Style: Head First book illustration style, clean lines, slightly whimsical and humorous, warm colors, educational
  Aspect ratio: 16:9
  Background: white
  Text in image: minimal, showing the instant update
  Avoid: photorealistic, dark, scary, complex UI screenshots

### Image 4: database-persistence
- **File**: `images/module-05/database-persistence.png`
- **Page**: 4 (Database Persistence)
- **Placement**: after the volume vs no-volume database comparison
- **Description**: Two PostgreSQL containers. Top row: container without volume is destroyed, data table shows "relation does not exist" error. Bottom row: container with volume is destroyed and recreated, data table shows "Campbell" record intact. The definitive visual argument for always using volumes with databases.
- **Status**: Generated
- **Prompt**:
  Goal: editorial illustration for a programming textbook
  Scene: Two-row comparison. Top row "No Volume": PostgreSQL container with data (table showing a row), then container removed (poof), then new container with empty database and red error message "relation does not exist." Bottom row "With Volume": PostgreSQL container with data, then container removed (poof) but a volume cylinder remains, then new container reconnects to volume and data is intact with green checkmark. The mood is a cautionary tale with a happy resolution.
  Style: Head First book illustration style, clean lines, slightly whimsical and humorous, warm colors, educational
  Aspect ratio: 16:9
  Background: white
  Text in image: "No Volume" / "With Volume" labels, error message
  Avoid: photorealistic, dark, scary, complex UI screenshots

---

## Module 06: Networking

### Image 1: hero-networking
- **File**: `images/module-06/hero-networking.png`
- **Page**: 1 (Docker Network Types)
- **Placement**: after the H2 heading
- **Description**: Four network types shown as neighborhoods: bridge (houses on a street), host (house directly on the highway), none (isolated island), custom bridge (gated community with a directory/phone book). Gives students a mental model for each type.
- **Status**: Generated
- **Prompt**:
  Goal: editorial illustration for a programming textbook
  Scene: A bird's eye view of four neighborhoods representing network types. "Bridge": houses along a street, they can see each other but only by address numbers. "Host": a house sitting directly on a major highway with no fences. "None": a house on a remote island with no roads. "Custom Bridge": a gated community with a directory board at the entrance where houses can look up each other by name. Each neighborhood is labeled clearly. The mood is architectural and organized.
  Style: Head First book illustration style, clean lines, slightly whimsical and humorous, warm colors, educational
  Aspect ratio: 16:9
  Background: white
  Text in image: network type labels
  Avoid: photorealistic, dark, scary, complex UI screenshots

### Image 2: port-mapping-multi
- **File**: `images/module-06/port-mapping-multi.png`
- **Page**: 2 (Port Mapping)
- **Placement**: after the three Nginx containers on different ports
- **Description**: Three containers all listening on port 80 internally, but mapped to different host ports (8080, 8081, 8082). Shows how port mapping enables running multiple identical services simultaneously.
- **Status**: Generated
- **Prompt**:
  Goal: editorial illustration for a programming textbook
  Scene: A host machine (laptop) with three doors on its side, labeled 8080, 8081, and 8082. Each door has a tunnel leading to a separate Nginx container, each listening on port 80 internally. All three containers are identical but isolated. Arrows show requests coming to different host ports and reaching different containers. The mood is organized and clear.
  Style: Head First book illustration style, clean lines, slightly whimsical and humorous, warm colors, educational
  Aspect ratio: 16:9
  Background: white
  Text in image: port numbers
  Avoid: photorealistic, dark, scary, complex UI screenshots

### Image 3: dns-comparison
- **File**: `images/module-06/dns-comparison.png`
- **Page**: 3-4 (Default Bridge vs Custom Bridge)
- **Placement**: after the DNS failure demonstration
- **Description**: Two panels. Left (default bridge): containers try to call each other by name and get "host not found" errors, can only use IP addresses. Right (custom bridge): containers call each other by name and a built-in DNS server resolves them instantly. Shows why custom networks are essential.
- **Status**: Generated
- **Prompt**:
  Goal: editorial illustration for a programming textbook
  Scene: Two panels. Left panel "Default Bridge": two containers try to talk. Container A says "Hey server1!" but gets a confused "???" response and a red X. A note says "must use IP: 172.17.0.2". Right panel "Custom Bridge": same two containers, but now a friendly DNS character in the middle translates names to IPs. Container A says "Hey server1!" and DNS routes it correctly with a green checkmark. The mood contrasts frustration with ease.
  Style: Head First book illustration style, clean lines, slightly whimsical and humorous, warm colors, educational
  Aspect ratio: 16:9
  Background: white
  Text in image: container names and DNS labels
  Avoid: photorealistic, dark, scary, complex UI screenshots

### Image 4: network-isolation
- **File**: `images/module-06/network-isolation.png`
- **Page**: 4 (Custom Bridge Networks)
- **Placement**: after the network isolation demonstration
- **Description**: Two custom networks shown as fenced areas. Containers inside each network can talk freely, but containers in different networks cannot reach each other. A container in Network A tries to reach one in Network B and hits a wall.
- **Status**: Generated
- **Prompt**:
  Goal: editorial illustration for a programming textbook
  Scene: Two fenced enclosures side by side. Left fence labeled "app-network" contains containers "api" and "frontend" chatting happily with green arrows. Right fence labeled "isolated-network" contains container "isolated-app" alone. A dashed red arrow from "frontend" tries to reach "isolated-app" but hits the fence and bounces back with a red X. The mood shows security through isolation.
  Style: Head First book illustration style, clean lines, slightly whimsical and humorous, warm colors, educational
  Aspect ratio: 16:9
  Background: white
  Text in image: network and container names
  Avoid: photorealistic, dark, scary, complex UI screenshots

---

## Module 07: Docker Compose Part 1

### Image 1: hero-compose
- **File**: `images/module-07/hero-compose.png`
- **Page**: 1 (What Is Docker Compose?)
- **Placement**: after the H2 heading
- **Description**: Before/after comparison. Left: a developer juggling multiple docker run commands (long command strings flying around, tangled flags). Right: the same developer calmly holding a single YAML file while all containers run harmoniously. Shows the simplification Compose brings.
- **Status**: Generated
- **Prompt**:
  Goal: editorial illustration for a programming textbook
  Scene: Split scene. Left "Before Compose": a frazzled developer juggling multiple long command strings (docker run -d -p --name --network...) that tangle around them like spaghetti. Multiple terminals are open. Right "After Compose": the same developer relaxed, holding a single clean document labeled "docker-compose.yml." Three containers run peacefully behind them, connected with neat lines. The mood contrasts chaos with simplicity.
  Style: Head First book illustration style, clean lines, slightly whimsical and humorous, warm colors, educational
  Aspect ratio: 16:9
  Background: white
  Text in image: "Before" / "After" labels
  Avoid: photorealistic, dark, scary, complex UI screenshots

### Image 2: compose-yaml-anatomy
- **File**: `images/module-07/compose-yaml-anatomy.png`
- **Page**: 1 (What Is Docker Compose?)
- **Placement**: after the basic structure YAML example
- **Description**: An annotated docker-compose.yml shown as a blueprint with callout bubbles explaining each section: services (the containers), ports (external access), volumes (data persistence), environment (configuration), depends_on (startup order).
- **Status**: Generated
- **Prompt**:
  Goal: editorial illustration for a programming textbook
  Scene: A large blueprint document showing a docker-compose.yml structure. Callout bubbles with icons point to sections: "services" section has a container icon and says "Your containers"; "ports" section has a plug icon and says "External access"; "volumes" section has a disk icon and says "Persistent data"; "environment" section has a gear icon and says "Configuration"; "depends_on" section has an arrow icon and says "Startup order." The mood is organized and explanatory.
  Style: Head First book illustration style, clean lines, slightly whimsical and humorous, warm colors, educational
  Aspect ratio: 16:9
  Background: white
  Text in image: section labels and callout text
  Avoid: photorealistic, dark, scary, complex UI screenshots

### Image 3: three-tier-stack
- **File**: `images/module-07/three-tier-stack.png`
- **Page**: 3 (Multi-Service Application) or 4 (Adding a Database)
- **Placement**: after adding PostgreSQL to the stack
- **Description**: A three-tier architecture diagram: Nginx (frontend) reverse-proxying to Flask (API) connecting to PostgreSQL (database) with a named volume. Arrows show request flow from browser through the stack. Shows the complete web application pattern.
- **Status**: Generated
- **Prompt**:
  Goal: editorial illustration for a programming textbook
  Scene: A vertical three-tier architecture. Top tier: browser sending request to Nginx container (labeled "Frontend / Reverse Proxy"). Middle tier: Flask container (labeled "API") receiving proxied requests from Nginx. Bottom tier: PostgreSQL container (labeled "Database") with a volume cylinder attached. Arrows flow down from browser through each tier. A surrounding box labeled "docker-compose.yml" wraps all three tiers. The mood is architectural and professional.
  Style: Head First book illustration style, clean lines, slightly whimsical and humorous, warm colors, educational
  Aspect ratio: 16:9
  Background: white
  Text in image: tier labels and service names
  Avoid: photorealistic, dark, scary, complex UI screenshots

---

## Module 08: Docker Compose Part 2

### Image 1: hero-env-vars
- **File**: `images/module-08/hero-env-vars.png`
- **Page**: 1 (Environment Variables)
- **Placement**: after the H2 heading
- **Description**: Three paths for environment variables flowing into a container: inline YAML values, .env file (kept out of git), and shell variable substitution with ${} syntax. Shows the three configuration approaches at a glance.
- **Status**: Generated
- **Prompt**:
  Goal: editorial illustration for a programming textbook
  Scene: A container in the center with three incoming pipes. Pipe 1 "Inline" comes from a YAML document with values written directly. Pipe 2 ".env File" comes from a secret document with a lock icon (kept out of version control). Pipe 3 "Shell" comes from a terminal with ${VAR} syntax. All three pipes merge into the container's "environment" intake. The mood is organized and shows three valid approaches.
  Style: Head First book illustration style, clean lines, slightly whimsical and humorous, warm colors, educational
  Aspect ratio: 16:9
  Background: white
  Text in image: pipe labels
  Avoid: photorealistic, dark, scary, complex UI screenshots

### Image 2: health-check-startup
- **File**: `images/module-08/health-check-startup.png`
- **Page**: 3 (Health Checks and Dependencies)
- **Placement**: after the health check explanation
- **Description**: A timeline showing database container transitioning from "starting" to "healthy" (with pg_isready checks), and only then does the API container start. Shows the condition: service_healthy dependency in action versus a fragile "sleep and hope" approach.
- **Status**: Generated
- **Prompt**:
  Goal: editorial illustration for a programming textbook
  Scene: A timeline flowing left to right. Database container starts with a yellow "Starting" status and a doctor character running health checks (stethoscope). After several checks, status turns green "Healthy." Only then does the API container start up, with an arrow from the healthy database to the API's start. Below, a crossed-out bad approach: "sleep 5 && start" with a red X. The mood contrasts reliable vs fragile startup.
  Style: Head First book illustration style, clean lines, slightly whimsical and humorous, warm colors, educational
  Aspect ratio: 16:9
  Background: white
  Text in image: status labels and timeline markers
  Avoid: photorealistic, dark, scary, complex UI screenshots

### Image 3: profiles
- **File**: `images/module-08/profiles.png`
- **Page**: 4 (Profiles)
- **Placement**: after the profiles explanation
- **Description**: A Compose stack shown as a building. Core services (API, DB) are always-on ground floor tenants. Optional services (Adminer, Redis) are on upper floors behind locked doors labeled "debug" and "cache" — they only appear when you use the --profile key.
- **Status**: Generated
- **Prompt**:
  Goal: editorial illustration for a programming textbook
  Scene: A building with floors. Ground floor "Always On" has API and DB containers brightly lit and active. Upper floors have doors with signs: "debug" floor has Adminer behind a locked door, "cache" floor has Redis behind another locked door. A developer holds keys labeled "--profile debug" and "--profile cache." When a key is used, that floor lights up. The mood shows selective activation — lean by default, extensible on demand.
  Style: Head First book illustration style, clean lines, slightly whimsical and humorous, warm colors, educational
  Aspect ratio: 16:9
  Background: white
  Text in image: profile names and service labels
  Avoid: photorealistic, dark, scary, complex UI screenshots

### Image 4: restart-policies
- **File**: `images/module-08/restart-policies.png`
- **Page**: 5 (Restart Policies and Resource Limits)
- **Placement**: after the restart policies explanation
- **Description**: A container that crashes (falls over), then automatically gets back up with a "restart: unless-stopped" spring mechanism underneath. A separate gauge shows CPU and memory limits preventing the container from consuming too much. Shows resilience and resource control.
- **Status**: Generated
- **Prompt**:
  Goal: editorial illustration for a programming textbook
  Scene: A container falls over (crash), but a spring mechanism labeled "restart: unless-stopped" bounces it back upright automatically. A sequence shows: running → crash → bounce back → running again. Next to it, a separate gauge/dashboard shows CPU and Memory dials with limits marked: "256M memory max" and "0.5 CPU max." The mood is resilient and controlled — things crash, but Docker handles it.
  Style: Head First book illustration style, clean lines, slightly whimsical and humorous, warm colors, educational
  Aspect ratio: 16:9
  Background: white
  Text in image: policy name and resource limits
  Avoid: photorealistic, dark, scary, complex UI screenshots

---

## Module 09: Docker Hub and Registries

### Image 1: hero-publish
- **File**: `images/module-09/hero-publish.png`
- **Page**: 1 (Docker Hub)
- **Placement**: after the H2 heading
- **Description**: A developer pushing a Docker image up to Docker Hub (shown as a cloud warehouse). Other developers around the world pull it down. Shows the publish/consume cycle and Docker Hub's role as a central registry.
- **Status**: Generated
- **Prompt**:
  Goal: editorial illustration for a programming textbook
  Scene: A developer at a laptop pushes an image (shown as a package with a tag) upward to a cloud labeled "Docker Hub" (with a whale logo). The cloud warehouse stores many images. Other developers around the world (shown as small figures at different laptops) pull images down from the cloud. Arrows show "docker push" going up and "docker pull" coming down. The mood is global and collaborative.
  Style: Head First book illustration style, clean lines, slightly whimsical and humorous, warm colors, educational
  Aspect ratio: 16:9
  Background: white
  Text in image: "docker push" / "docker pull" labels
  Avoid: photorealistic, dark, scary, complex UI screenshots

### Image 2: image-naming
- **File**: `images/module-09/image-naming.png`
- **Page**: 1 (Docker Hub)
- **Placement**: after the naming convention section
- **Description**: An image name broken down into its four components (registry/username/repository:tag) with examples showing official images (no username), personal images, and alternative registries (ghcr.io). A visual decoder ring for image names.
- **Status**: Generated
- **Prompt**:
  Goal: editorial illustration for a programming textbook
  Scene: A large image name "ghcr.io/myuser/my-app:1.0.0" is broken into segments with colored brackets. Each segment has a label and example: Registry (ghcr.io, or "Docker Hub if omitted"), Username (myuser, or "official if omitted"), Repository (my-app), Tag (1.0.0). Below, three example images show the pattern: "nginx:alpine" (official), "myuser/demo:1.0" (personal), "ghcr.io/owner/repo:latest" (GitHub). The mood is decoder/reference style.
  Style: Head First book illustration style, clean lines, slightly whimsical and humorous, warm colors, educational
  Aspect ratio: 16:9
  Background: white
  Text in image: segment labels and examples
  Avoid: photorealistic, dark, scary, complex UI screenshots

### Image 3: semantic-versioning
- **File**: `images/module-09/semantic-versioning.png`
- **Page**: 5 (Versioning and Updates)
- **Placement**: after the tagging strategy table
- **Description**: A version tree showing how tags 1.0.0, 1.0, 1, and latest all point to the same image, and how releasing 1.1.0 moves the latest and 1 pointers but leaves 1.0.0 unchanged. Shows immutable vs mutable tags visually.
- **Status**: Generated
- **Prompt**:
  Goal: editorial illustration for a programming textbook
  Scene: A timeline with two release points. At release 1.0.0: four labels (1.0.0, 1.0, 1, latest) all point to the same image. At release 1.1.0: the 1.0.0 and 1.0 labels stay on the old image (immutable), while "1" and "latest" move to point at the new image. The old image is labeled "still available" and the new one "now default." Arrows show which tags moved and which didn't. The mood is organized version management.
  Style: Head First book illustration style, clean lines, slightly whimsical and humorous, warm colors, educational
  Aspect ratio: 16:9
  Background: white
  Text in image: version tags and movement arrows
  Avoid: photorealistic, dark, scary, complex UI screenshots

### Image 4: security-checklist
- **File**: `images/module-09/security-checklist.png`
- **Page**: 6 (Image Security and Best Practices)
- **Placement**: after the best practices checklist
- **Description**: A pre-flight checklist for publishing Docker images, styled as an aircraft preflight card. Items include: specific base tag, non-root user, no cached pip files, .dockerignore present, PYTHONDONTWRITEBYTECODE set, layer caching optimized, EXPOSE documented, semantic versioning used. The capstone visual for the entire course.
- **Status**: Generated
- **Prompt**:
  Goal: editorial illustration for a programming textbook
  Scene: A clipboard styled as a pilot's pre-flight checklist, held by a developer. Items listed with checkboxes: "Specific base tag (not latest)", "Non-root USER", "--no-cache-dir with pip", ".dockerignore present", "PYTHONDONTWRITEBYTECODE=1", "Dependencies before app code", "EXPOSE port documented", "Semantic version tags." A stamp at the bottom reads "CLEARED FOR LAUNCH." The mood is professional, thorough, and final — the capstone of the course.
  Style: Head First book illustration style, clean lines, slightly whimsical and humorous, warm colors, educational
  Aspect ratio: 16:9
  Background: white
  Text in image: checklist items
  Avoid: photorealistic, dark, scary, complex UI screenshots
