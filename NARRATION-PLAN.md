# Docker Fundamentals — Narration Plan

This plan enumerates every `> 🎙️` narration block in `source/`,
organized by source module → block index (1-based, in source order)→
full text → character count → ElevenLabs credit estimate
(`eleven_multilingual_v2`: 1 character = 1 credit).

Already-generated blocks are marked **DONE** based on the presence of the
matching `audio/<source-stem>/NN_<source-stem>.mp3` file. Missing blocks
are marked **MISSING** — they are the focus of any next narration run.

> Voice: ElevenLabs Rachel (course default). Run `uv run --with elevenlabs python scripts/generate_narration.py` to fill in the MISSING blocks below — the script numbers blocks by position and skips ones whose MP3 already exists.

## Totals

- **Modules with narration:** 10
- **Total narration blocks:** 113
- **Total characters:** 33,684
- **Generated (DONE):** 106 blocks, 30,982 chars
- **Outstanding (MISSING):** 7 blocks, 2,702 chars
- **Estimated ElevenLabs credits to finish:** ~2,702 (multilingual_v2, 1 char = 1 credit)

---

## `module-00-what-is-docker.md`

- Blocks: **11** | Chars: **3,221** | DONE: **11** | MISSING: **0** (0 chars)

### Block 1 — DONE

_341 chars · ~341 credits_

> Docker is a platform for running applications in containers, which are lightweight, isolated environments that package your code with everything it needs to run. Think of a container as a self-contained box with your application, its libraries, dependencies, and configuration all bundled together. No more "it works on my machine" problems.

### Block 2 — DONE

_389 chars · ~389 credits_

> Containers and virtual machines both provide isolation, but they work very differently. A virtual machine virtualizes the hardware and runs a full guest operating system, which makes it heavy — gigabytes in size and minutes to start. A container virtualizes the operating system instead, sharing the host kernel while isolating the process. This makes containers tiny, fast, and efficient.

### Block 3 — DONE

_349 chars · ~349 credits_

> Docker has a simple client-server architecture. You type commands into the Docker CLI, which sends them to the Docker Daemon running in the background. The daemon manages images and containers. An image is like a class in object-oriented programming — it's a read-only template. A container is like an object — it's a running instance of that image.

### Block 4 — DONE

_315 chars · ~315 credits_

> Let's get Docker installed on your machine. The steps vary by operating system, but the goal is the same — get the Docker daemon running so you can start launching containers. If you're on Linux, you'll install Docker Engine directly. On Mac or Windows, you'll use Docker Desktop, which bundles everything together.

### Block 5 — DONE

_238 chars · ~238 credits_

> Now let's make sure everything is working by running your very first container. The hello-world image is Docker's built-in smoke test — it pulls a tiny image, runs it, and prints a message confirming your installation is set up correctly.

### Block 6 — DONE

_303 chars · ~303 credits_

> Now that you've run your first container, let's see what Docker left behind. The docker images command shows downloaded images, and docker ps shows running containers. Add the dash-a flag to also see stopped containers. Then you'll clean up by removing the container and image, leaving your system tidy.

### Block 7 — DONE

_285 chars · ~285 credits_

> Good practice means cleaning up after yourself. Docker containers and images stick around on disk until you explicitly remove them. Let's remove the hello-world container and image so your system stays tidy. This cleanup habit will save you disk space as you work through more modules.

### Block 8 — DONE

_238 chars · ~238 credits_

> Let's get hands-on with a real container. You're going to launch an interactive Ubuntu environment, explore it, install software, then exit and start a new one to prove that containers are ephemeral — each one starts fresh from the image.

### Block 9 — DONE

_273 chars · ~273 credits_

> Now let's do something practical — run a real web server. You'll launch Nginx in detached mode, map a port from your host into the container, and access it in your browser. This is the pattern you'll use constantly with Docker: run a service, map a port, and connect to it.

### Block 10 — DONE

_216 chars · ~216 credits_

> When you're done with a container, you stop it first, then remove it. Stopping sends a graceful shutdown signal, and removing deletes the container from your system. You'll do this constantly as you work with Docker.

### Block 11 — DONE

_274 chars · ~274 credits_

> That wraps up your first module. You've installed Docker, run your first container, explored an interactive Ubuntu environment, and launched a web server. These are the building blocks for everything that follows. Make sure you capture your terminal output before moving on.

---

## `module-01-images-and-containers.md`

- Blocks: **11** | Chars: **2,997** | DONE: **11** | MISSING: **0** (0 chars)

### Block 1 — DONE

_386 chars · ~386 credits_

> An image is a layered, read-only template identified by a registry, repository, and tag. For example, python colon 3.12 dash slim means the Python image, version 3.12, in the slim variant. Tags let you pick exactly the version and size you need. Understanding tags is critical because pulling the wrong variant can mean the difference between a 50 megabyte image and a 1 gigabyte image.

### Block 2 — DONE

_332 chars · ~332 credits_

> Tags identify specific versions of an image. The latest tag is the default, but it doesn't always mean the newest version. Slim variants remove build tools and extra packages. Alpine variants use Alpine Linux as the base, making them the smallest option. Choosing the right variant is one of the simplest optimizations you can make.

### Block 3 — DONE

_262 chars · ~262 credits_

> Under the hood, every Docker image is made up of layers stacked on top of each other. Each layer represents a change, like installing a package or copying a file. Docker caches and reuses these layers across images, which saves both download time and disk space.

### Block 4 — DONE

_242 chars · ~242 credits_

> Let's see the size differences for yourself. You're going to pull three variants of the Python image — the full version, the slim version, and the Alpine version. Then you'll compare their sizes and see why choosing the right variant matters.

### Block 5 — DONE

_224 chars · ~224 credits_

> The docker inspect command reveals everything Docker knows about an image — its layers, environment variables, entry point, and more. You can also use format strings to pull out specific fields, which is handy for scripting.

### Block 6 — DONE

_287 chars · ~287 credits_

> One of Docker's superpowers is the ability to run different languages and different versions side by side with zero conflicts. You can run Python 3.12 and Python 3.11 at the same time, on the same machine, with no installation and no version conflicts. Try doing that without containers!

### Block 7 — DONE

_237 chars · ~237 credits_

> By default, Docker assigns random names to containers like "quirky underscore einstein." That's fine for quick tests, but in real work you'll want to name your containers so you can reference them easily in logs, exec, and stop commands.

### Block 8 — DONE

_273 chars · ~273 credits_

> You can dig deeper into a running container using docker inspect and docker stats. Inspect shows you the container's internal IP address, mount points, and configuration. Stats gives you a live dashboard of CPU, memory, and network usage across all your running containers.

### Block 9 — DONE

_216 chars · ~216 credits_

> Before moving on, let's clean up the containers you created. Stopping and removing containers after you're done with them is a habit you should build early. It keeps your system from filling up with stale containers.

### Block 10 — DONE

_279 chars · ~279 credits_

> Docker gives you fine-grained control over container behavior at runtime. You can inject environment variables, set the working directory, and tell Docker to automatically clean up the container when it exits. These flags are things you'll use in almost every docker run command.

### Block 11 — DONE

_259 chars · ~259 credits_

> Great work on this module. You now know how to pull images, compare variants, run containers from different language runtimes, and control container behavior with flags. These skills form the foundation for building your own custom images in the next modules.

---

## `module-02-container-management.md`

- Blocks: **11** | Chars: **3,211** | DONE: **11** | MISSING: **0** (0 chars)

### Block 1 — DONE

_335 chars · ~335 credits_

> A container moves through a series of states: created, running, paused, stopped, and removed. Understanding this lifecycle is essential because you'll use different commands at each stage. A stopped container can be restarted. A paused container freezes all processes but keeps them in memory. And a removed container is gone for good.

### Block 2 — DONE

_251 chars · ~251 credits_

> Let's start by creating a long-running container that stays up so you can practice managing it. You'll use Nginx again since it runs as a background service and won't exit immediately. This container will be your playground for the next several tasks.

### Block 3 — DONE

_313 chars · ~313 credits_

> Pausing is different from stopping. When you pause a container, all its processes are frozen in place using Linux cgroups, but they stay in memory. When you unpause, everything resumes exactly where it left off. This is useful when you need to temporarily free up CPU without losing the container's current state.

### Block 4 — DONE

_328 chars · ~328 credits_

> Container logs are your primary debugging tool. Every container captures standard output and standard error, and you can view it anytime with docker logs. The tail flag shows the last N lines, the since flag shows recent logs, and the dash-f flag follows the log stream in real-time, just like tail dash-f on a regular log file.

### Block 5 — DONE

_293 chars · ~293 credits_

> Logs are only useful if there's something in them. Let's generate some log entries by making requests to your Nginx container, and then try a busybox container that produces a steady stream of heartbeat messages. This will give you real data to practice filtering with tail, since, and follow.

### Block 6 — DONE

_290 chars · ~290 credits_

> Docker exec is one of your most powerful tools. It lets you run any command inside a running container without stopping it. You can check configuration files, run diagnostics, or open a full interactive shell. Think of it as SSH-ing into your container, except it's built right into Docker.

### Block 7 — DONE

_244 chars · ~244 credits_

> Running individual commands with exec is great, but sometimes you need to poke around interactively. By adding the dash-i and dash-t flags, you can open a full bash shell inside the container and explore it just like you would any Linux system.

### Block 8 — DONE

_253 chars · ~253 credits_

> Docker cp lets you copy files between your host machine and a container in both directions. This is useful for pulling configuration files out of a container to inspect them, or pushing custom files into a running container without rebuilding the image.

### Block 9 — DONE

_327 chars · ~327 credits_

> In the real world, you'll often have many containers running at once. Docker provides commands for managing them in bulk — stopping multiple containers at once, pruning all stopped containers, and checking how much disk space Docker is using. These housekeeping commands keep your system clean and your resources under control.

### Block 10 — DONE

_309 chars · ~309 credits_

> Docker system df is like the du command for Docker. It shows you exactly how much disk space your images, containers, and volumes are consuming. If things are getting out of hand, docker system prune is your nuclear option — it removes all stopped containers, unused networks, and dangling images in one shot.

### Block 11 — DONE

_268 chars · ~268 credits_

> You've now mastered the full container lifecycle — starting, stopping, pausing, logging, exec-ing, and copying files. These operational skills are what separate someone who can run Docker from someone who can actually manage and debug containers in a real environment.

---

## `module-03-dockerfiles-part-1.md`

- Blocks: **12** | Chars: **3,396** | DONE: **11** | MISSING: **1** (383 chars)

### Block 1 — DONE

_399 chars · ~399 credits_

> A Dockerfile is a text file with instructions for building a Docker image. Think of it as a recipe: each instruction adds a layer to the image. FROM sets the base image, WORKDIR sets your working directory, COPY brings files in from your host, RUN executes commands during the build, and CMD sets what runs when the container starts. These five instructions cover ninety percent of what you'll need.

### Block 2 — DONE

_217 chars · ~217 credits_

> Take a look at the table above. These seven instructions are your Dockerfile vocabulary. You won't need all of them in every Dockerfile, but FROM, WORKDIR, COPY, RUN, and CMD will appear in almost every one you write.

### Block 3 — DONE

_200 chars · ~200 credits_

> Let's build your first custom Docker image. You'll create a simple Python script, write a Dockerfile for it, build the image, and run it. This is the core Docker workflow you'll use hundreds of times.

### Block 4 — DONE

_225 chars · ~225 credits_

> Now it's time to build and run your image. The docker build command reads your Dockerfile and creates an image. The dash t flag gives it a name and version tag. Then docker run creates a container from that image and runs it.

### Block 5 — DONE

_369 chars · ~369 credits_

> Now let's build something more real — a Flask web application. This is where you'll see an important optimization pattern: copy and install your requirements file first, then copy your application code. Docker caches each layer, so if you only change your app code, it skips the dependency installation step entirely. This saves huge amounts of time during development.

### Block 6 — DONE

_278 chars · ~278 credits_

> Time to build and run your Flask app. Notice the dash d flag, which runs the container in detached mode so it stays running in the background. The dash p flag maps port 5000 on your host to port 5000 inside the container, so you can access the web app from your browser or curl.

### Block 7 — DONE

_325 chars · ~325 credits_

> Not every containerized app needs a programming language runtime. Here you'll build a simple static website served by Nginx. The Dockerfile is just two lines: start from the Nginx Alpine image, and copy your HTML file into the right directory. Alpine-based images are tiny — your entire web server will be under 50 megabytes.

### Block 8 — DONE

_207 chars · ~207 credits_

> Build this image and run it on port 8080. Since Nginx listens on port 80 inside the container, you'll map 8080 on your host to 80 in the container. After verifying it works with curl, clean up the container.

### Block 9 — DONE

_320 chars · ~320 credits_

> One of Docker's most important features is layer caching. When you rebuild an image, Docker checks each instruction against its cache. If nothing changed, it reuses the cached layer. But the moment one layer changes, every layer after it must be rebuilt. That's why instruction order matters so much in your Dockerfiles.

### Block 10 — DONE

_176 chars · ~176 credits_

> Let's take a moment to see all the custom images you've built in this module. The docker images command lists everything, and you can filter it with grep to see just your work.

### Block 11 — DONE

_297 chars · ~297 credits_

> Great work. You've gone from writing your first Dockerfile to building three different types of applications: a simple Python script, a Flask web server, and a static Nginx site. You also saw how layer caching can speed up your builds dramatically. Save your output and Dockerfiles for submission.

### Block 12 — **MISSING**

_383 chars · ~383 credits_

> Here's your checklist for submission. Capture the terminal output from every task, and paste in the Dockerfiles you wrote — the simple Python one, the Flask one, and the static Nginx one. The grading rubric rewards the layer caching demonstration and proof that all three images appear in your images list. Take a minute to clean up any stray containers before you zip everything up.

---

## `module-04-dockerfiles-part-2.md`

- Blocks: **12** | Chars: **3,591** | DONE: **11** | MISSING: **1** (409 chars)

### Block 1 — DONE

_403 chars · ~403 credits_

> Every RUN, COPY, and ADD instruction creates a new layer in your image. More layers mean larger images and slower builds. The solution is to combine related commands into single RUN instructions. Instead of three separate RUN lines for apt-get update, install, and clean, combine them into one. This can dramatically reduce your image size because intermediate files don't get stored in separate layers.

### Block 2 — DONE

_259 chars · ~259 credits_

> Let's see this in practice. You're going to build two versions of the same image: one with separate RUN instructions for each pip install, and one that combines them using a requirements file. Then you'll use docker history to compare the layers side by side.

### Block 3 — DONE

_334 chars · ~334 credits_

> Multi-stage builds are a game-changer. The idea is simple: use one stage to build your application, and a second stage to run it. Only the final stage goes into your image. So the compiler, build tools, and source code are all left behind. For compiled languages like Java or Go, this can reduce your image size by 90 percent or more.

### Block 4 — DONE

_252 chars · ~252 credits_

> Now let's see multi-stage builds in action with Java. You'll use the full JDK to compile your code in the first stage, then copy just the compiled class file into a lightweight JRE image. Compare the sizes afterward and you'll see a massive difference.

### Block 5 — DONE

_260 chars · ~260 credits_

> Multi-stage builds work for Python too, though the size savings are less dramatic than with compiled languages. The key benefit here is separating your build environment from your runtime environment, keeping your final image clean and free of build artifacts.

### Block 6 — DONE

_314 chars · ~314 credits_

> A .dockerignore file tells Docker which files to exclude from the build context. Without one, Docker sends everything in your project directory to the daemon, including your git history, virtual environments, node modules, and secrets. A good dockerignore file makes your builds faster and your images more secure.

### Block 7 — DONE

_282 chars · ~282 credits_

> Creating a dockerignore file is quick and you should do it for every project. List the files and directories that have no business being in your image. At a minimum, always exclude your git directory, Python cache files, virtual environments, and any environment files with secrets.

### Block 8 — DONE

_205 chars · ~205 credits_

> Now let's prove that the dockerignore file actually works. You'll create some files that should be excluded, like a dot env file with secrets, then build the image and verify those files are not inside it.

### Block 9 — DONE

_301 chars · ~301 credits_

> Let's put everything together. A production-ready Dockerfile should use a specific base image tag, run as a non-root user, optimize layer caching, suppress Python bytecode generation, and document the port with EXPOSE. This is the template you should use for every Python application you containerize.

### Block 10 — DONE

_263 chars · ~263 credits_

> Build this image and then check who the process is running as. When you run the whoami command inside the container, it should print appuser, not root. This confirms that even if someone exploits your application, they won't have root access inside the container.

### Block 11 — DONE

_309 chars · ~309 credits_

> You've covered a lot of ground in this module. You know how to optimize layers, use multi-stage builds to shrink your images, exclude unnecessary files with dockerignore, and apply security best practices like non-root users. These techniques are what separate a quick prototype from a production-ready image.

### Block 12 — **MISSING**

_409 chars · ~409 credits_

> For this submission, include every Dockerfile you wrote — the layer comparison pair, the Java multi-stage, the Python multi-stage, and the final best-practices one. Paste the docker history output so I can see the layer sizes, and include the before-and-after image sizes for the multi-stage builds. The non-root user demonstration is worth the most points, so don't forget to show that whoami prints appuser.

---

## `module-05-volumes-and-persistence.md`

- Blocks: **12** | Chars: **3,508** | DONE: **11** | MISSING: **1** (351 chars)

### Block 1 — DONE

_361 chars · ~361 credits_

> Containers are ephemeral — when you remove a container, its data is gone. This is great for stateless applications, but terrible for databases, file uploads, or anything that needs to survive a restart. Docker provides two solutions: named volumes, which Docker manages for you, and bind mounts, which map a specific directory from your host into the container.

### Block 2 — DONE

_262 chars · ~262 credits_

> Here's a quick comparison to help you decide which to use. Named volumes are managed by Docker and are best for production data like databases. Bind mounts point to a specific directory on your host and are best for development where you want to edit files live.

### Block 3 — DONE

_284 chars · ~284 credits_

> Named volumes are Docker-managed storage that exists independently of any container. You create a volume, mount it into a container, write data, destroy the container, and the data is still there. You can even mount the same volume into multiple containers to share data between them.

### Block 4 — DONE

_234 chars · ~234 credits_

> Let's start by creating a named volume. The docker volume create command creates a volume that Docker manages for you. You can then list all volumes and inspect one to see where Docker actually stores the data on your host filesystem.

### Block 5 — DONE

_356 chars · ~356 credits_

> Bind mounts are the developer's best friend. Instead of Docker managing the storage, you map a directory from your host machine directly into the container. Edit a file on your host, and the change is instantly visible inside the container. This means you can use your favorite editor and tools while the application runs inside Docker — no rebuild needed.

### Block 6 — DONE

_234 chars · ~234 credits_

> Now for the magic. Edit the HTML file on your host machine and then curl the page again. You'll see the change immediately without restarting or rebuilding anything. This is the development workflow that makes bind mounts so valuable.

### Block 7 — DONE

_325 chars · ~325 credits_

> This is the most important demonstration in this module. You're going to run a PostgreSQL database without a volume, insert data, destroy the container, recreate it, and watch your data vanish. Then you'll do the same thing with a volume and see that the data survives. This is why you must always use volumes with databases.

### Block 8 — DONE

_247 chars · ~247 credits_

> First you'll run Postgres without a volume and see what happens when the container is destroyed. Pay close attention to the error you get when you try to query the table after recreating the container. That error is the whole reason volumes exist.

### Block 9 — DONE

_253 chars · ~253 credits_

> Like images and containers, volumes need housekeeping. Docker provides commands to list, inspect, and remove volumes. Orphaned volumes from deleted containers can accumulate over time, so periodically running docker volume prune keeps your system clean.

### Block 10 — DONE

_241 chars · ~241 credits_

> Let's do some housekeeping. You can list all volumes on your system, inspect individual ones to see their details, and remove ones you no longer need. Getting in the habit of cleaning up unused volumes will keep your Docker environment tidy.

### Block 11 — DONE

_360 chars · ~360 credits_

> You now understand the two main ways to persist data in Docker. Named volumes are your go-to for databases and production data, while bind mounts are essential for development workflows. The database demonstration showed you exactly why running a database without a volume is a recipe for data loss. Keep these patterns in mind as you move into Docker Compose.

### Block 12 — **MISSING**

_351 chars · ~351 credits_

> The most important piece of this submission is the database demonstration — the side-by-side proof that data disappears without a volume and survives with one. Capture both sequences in your output file. Also include your bind mount live-editing demo so I can see the change reflected instantly. Clean up all volumes and containers before you wrap up.

---

## `module-06-networking.md`

- Blocks: **11** | Chars: **3,290** | DONE: **10** | MISSING: **1** (370 chars)

### Block 1 — DONE

_401 chars · ~401 credits_

> Docker provides several network types. The default bridge network connects all containers but doesn't support DNS, so containers can only find each other by IP address. Custom bridge networks add DNS resolution, so containers can find each other by name. The host network removes isolation entirely, and the none network disables networking. For almost all use cases, you want a custom bridge network.

### Block 2 — DONE

_300 chars · ~300 credits_

> Port mapping is how you make a container's service accessible from outside Docker. Think of it like forwarding a port on your router — you pick a port on your host machine and connect it to a port inside the container. Without port mapping, your container's service is invisible to the outside world.

### Block 3 — DONE

_322 chars · ~322 credits_

> Port mapping lets you expose container services to your host machine. You can map any host port to any container port. This means you can run three Nginx containers on ports 8080, 8081, and 8082, all serving port 80 internally. Capital P maps all exposed ports to random host ports, which is useful for avoiding conflicts.

### Block 4 — DONE

_257 chars · ~257 credits_

> In this first task, you'll run three separate Nginx containers, each mapped to a different host port. This shows how multiple containers can all listen on the same internal port without any conflict, because each one gets its own isolated network namespace.

### Block 5 — DONE

_254 chars · ~254 credits_

> Sometimes you don't care which host port is used — you just need the container to be reachable. Capital P lets Docker pick a random available port for you. This is handy when running multiple instances where you don't want to manually track port numbers.

### Block 6 — DONE

_257 chars · ~257 credits_

> Let's explore the default bridge network and see its limitations. Containers on the default bridge can communicate by IP address, but DNS resolution — looking up a container by its name — does not work. This is a major limitation that custom networks solve.

### Block 7 — DONE

_329 chars · ~329 credits_

> Custom bridge networks are how you should always connect containers. When you create a custom network and attach containers to it, Docker runs an embedded DNS server that lets containers find each other by name. This is the foundation of service discovery — and it's exactly what Docker Compose does automatically under the hood.

### Block 8 — DONE

_293 chars · ~293 credits_

> Network isolation is just as important as connectivity. By placing containers on separate custom networks, you can ensure they cannot communicate with each other at all. This is a key security feature — your frontend network doesn't need to talk directly to your database network, for example.

### Block 9 — DONE

_276 chars · ~276 credits_

> Let's put networking into practice by building a two-service application. You'll create a Python Flask API, containerize it, put it on a custom network, and call it from another container using its service name. This is the exact pattern that Docker Compose automates for you.

### Block 10 — DONE

_231 chars · ~231 credits_

> Great work connecting containers across networks. Before you finish, make sure to clean up all the containers and networks you created. Leaving unused resources around wastes memory and can cause port conflicts in future exercises.

### Block 11 — **MISSING**

_370 chars · ~370 credits_

> For submission, capture the full sequence — multiple containers on different host ports, the DNS failure on the default bridge, and the DNS success on your custom network. The two-service application where containers find each other by name is the capstone of this module, so make sure that output is clear. Remember to tear down every network and container you created.

---

## `module-07-docker-compose-part-1.md`

- Blocks: **11** | Chars: **3,403** | DONE: **10** | MISSING: **1** (383 chars)

### Block 1 — DONE

_391 chars · ~391 credits_

> Docker Compose lets you define and run multi-container applications with a single YAML file. Instead of running multiple docker run commands with networks and volumes and environment variables, you describe everything declaratively in a docker-compose.yml file. One command — docker compose up — brings the entire stack to life. One command — docker compose down — tears it all down cleanly.

### Block 2 — DONE

_263 chars · ~263 credits_

> Here are the commands you'll use every day with Docker Compose. You don't need to memorize all of them right now — just know that "up" starts everything, "down" stops everything, and "ps" shows you what's running. Those three will get you through most situations.

### Block 3 — DONE

_282 chars · ~282 credits_

> Let's start simple. You'll create a docker-compose.yml with a single Nginx service, a bind mount for live editing, and a port mapping. Then you'll learn the four essential Compose commands: up, ps, logs, and down. These four commands cover 90 percent of your daily Compose workflow.

### Block 4 — DONE

_274 chars · ~274 credits_

> Now bring it to life. The "docker compose up dash d" command starts all your services in the background. Then you'll check that everything is running and test it with curl. This three-step pattern — up, ps, test — is your standard workflow for launching any Compose project.

### Block 5 — DONE

_342 chars · ~342 credits_

> Now let's build something more realistic — a frontend served by Nginx that proxies API requests to a Flask backend. This is a very common pattern in web development. Nginx serves static files and reverse-proxies API calls to the backend service. The two services find each other by name because Compose creates a shared network automatically.

### Block 6 — DONE

_297 chars · ~297 credits_

> Time to start the stack and verify that everything is wired together. You'll hit the frontend directly and also test the API proxy route. If the proxy works, it means Nginx is forwarding requests to the Flask container using the service name "api" — exactly how service discovery works in Compose.

### Block 7 — DONE

_230 chars · ~230 credits_

> Logs are your best friend when debugging multi-container applications. Docker Compose lets you view logs from all services at once, or filter to just one service. When something goes wrong, this is the first place you should look.

### Block 8 — DONE

_358 chars · ~358 credits_

> Let's add PostgreSQL to our stack. This is where you see the real power of Compose — adding a service is just a few lines of YAML. You'll add the database, give it a named volume for persistence, pass credentials through environment variables, and connect it to the API. The API can reach the database at hostname "db" because Compose handles the networking.

### Block 9 — DONE

_314 chars · ~314 credits_

> When you change your docker-compose.yml, you need to bring the stack down and back up for changes to take effect. Compose is smart about this — it only recreates containers whose configuration has changed. The database container will start fresh, and the API now has database connection details in its environment.

### Block 10 — DONE

_269 chars · ~269 credits_

> Docker compose exec lets you run commands inside a running service container. Here you'll use it to connect to PostgreSQL and run SQL queries. This is exactly how you'd interact with your database during development — no need to install PostgreSQL on your host machine.

### Block 11 — **MISSING**

_383 chars · ~383 credits_

> Include every docker-compose.yml you wrote in this module — the single Nginx service, the Nginx-and-Flask stack, and the full version with PostgreSQL added. Paste the terminal output showing docker compose up, ps, and logs for each. The reverse proxy test, where Nginx forwards to the API by service name, is a favorite question on the quiz, so make sure that output is in your file.

---

## `module-08-docker-compose-part-2.md`

- Blocks: **11** | Chars: **3,763** | DONE: **10** | MISSING: **1** (413 chars)

### Block 1 — DONE

_382 chars · ~382 credits_

> Managing configuration is one of the most important parts of any deployment. Docker Compose gives you three ways to set environment variables: inline in the YAML file, from an external env file, and through shell variable substitution. The .env file approach is the most common because it keeps secrets out of your docker-compose.yml, which you can safely commit to version control.

### Block 2 — DONE

_329 chars · ~329 credits_

> Let's set up a project that demonstrates all three approaches to environment variables. You'll create a dot-env file with your configuration, a Flask app that reads those variables, and a Compose file that wires everything together. Pay attention to how the variable values flow from the dot-env file into the running containers.

### Block 3 — DONE

_357 chars · ~357 credits_

> One of the best things about using dot-env files is that you can swap configurations without changing your docker-compose.yml at all. You'll create a separate production env file and launch the same stack with completely different settings. This is how teams manage different environments — development, staging, and production — with the same Compose file.

### Block 4 — DONE

_386 chars · ~386 credits_

> Health checks let Docker monitor whether a service is actually ready, not just running. A database container might be running but still initializing. With a health check, Docker can tell the difference. And with condition service_healthy in depends_on, your API won't start until the database is truly ready to accept connections. This eliminates the fragile "sleep 5 and hope" pattern.

### Block 5 — DONE

_268 chars · ~268 credits_

> Now let's see health checks in action. Start the stack and watch the database service transition from "starting" to "healthy." The API service will wait patiently until the database reports healthy before it starts up. This is reliable, deterministic startup ordering.

### Block 6 — DONE

_385 chars · ~385 credits_

> Profiles let you define optional services that only start when you ask for them. This is perfect for development tools, debug utilities, or cache services that you don't always need. A service without a profile always starts. A service with a profile only starts when you pass the dash-dash-profile flag. This keeps your default stack lean while making extra tools available on demand.

### Block 7 — DONE

_236 chars · ~236 credits_

> Let's add two optional services — Adminer for database administration and Redis for caching. By putting them behind profiles, they won't start by default. Your core stack stays lean, and you only bring in extra tools when you need them.

### Block 8 — DONE

_343 chars · ~343 credits_

> In production, you want services that recover automatically from crashes. Restart policies tell Docker what to do when a container exits. The "unless-stopped" policy restarts containers on failure and on system reboot, but respects a manual stop. Resource limits prevent a single service from consuming all available memory or CPU on the host.

### Block 9 — DONE

_334 chars · ~334 credits_

> Now you'll add a restart policy and resource limits to your API service. The restart policy tells Docker to automatically restart the container if it crashes. Resource limits prevent a runaway process from consuming all available CPU or memory on your host machine. Together, these two settings make your services much more resilient.

### Block 10 — DONE

_330 chars · ~330 credits_

> You've now covered the advanced features that make Docker Compose production-ready — environment management, health checks, profiles, restart policies, and resource limits. These are the tools that separate a quick demo from a robust deployment. Make sure to clean up with "docker compose down dash v" before submitting your work.

### Block 11 — **MISSING**

_413 chars · ~413 credits_

> For submission, include both your dot-env file and your dot-env dot production file so I can see that you swapped configurations cleanly. Capture the health check transitioning from starting to healthy, and the proof that your API waited for the database before starting. Show the profile commands starting Adminer and Redis on demand. Bring everything down with compose down dash v before you zip up the results.

---

## `module-09-docker-hub-and-registries.md`

- Blocks: **11** | Chars: **3,304** | DONE: **10** | MISSING: **1** (393 chars)

### Block 1 — DONE

_339 chars · ~339 credits_

> Docker Hub is the default public registry for Docker images. Every time you've run docker pull nginx or docker run python, you've been downloading from Docker Hub. Now it's your turn to push images there. You'll create an account, tag your images with your username, and push them so anyone in the world can pull and run your applications.

### Block 2 — DONE

_345 chars · ~345 credits_

> Understanding the image naming convention is essential. The full name includes the registry, your username, the repository name, and a tag. When you omit the registry, Docker assumes Docker Hub. When you omit the username, Docker assumes it's an official image. Tags let you version your images so users can pin to exactly the release they need.

### Block 3 — DONE

_249 chars · ~249 credits_

> First, you need a Docker Hub account. It's free for public repositories. Once you've signed up, you log in from the command line with docker login. This authenticates you so you can push images. Your username becomes part of every image you publish.

### Block 4 — DONE

_308 chars · ~308 credits_

> The publish workflow has three steps: build the image, tag it with your Docker Hub username and version numbers, and push it. You'll create multiple tags for the same image — a specific version like 1.0.0, a minor version like 1.0, and latest. This gives users flexibility in how they pin their dependencies.

### Block 5 — DONE

_280 chars · ~280 credits_

> Now you'll build your image and create multiple tags pointing to it. This is a key concept — tags are just labels, not separate copies. One image can have many tags, and they all share the same layers. You'll create a specific version tag, a minor version tag, and the latest tag.

### Block 6 — DONE

_238 chars · ~238 credits_

> Now simulate what someone else would experience when using your image. Remove all local copies, then pull and run from Docker Hub. This proves that your image is fully self-contained and anyone can use it with a single docker run command.

### Block 7 — DONE

_336 chars · ~336 credits_

> Software evolves, and your images should evolve with proper versioning. When you release a new version, build the image, tag it with the new version number, update the latest tag to point to it, and push all the tags. Users pinned to 1.0.0 keep getting 1.0.0. Users on latest get your newest code. This is semantic versioning in action.

### Block 8 — DONE

_226 chars · ~226 credits_

> Here's where versioning really pays off. You'll run both version 1.0.0 and version 1.1.0 side by side on different ports. This is how you can test a new release against the old one, or gradually roll out updates in production.

### Block 9 — DONE

_290 chars · ~290 credits_

> Publishing images comes with responsibility. You should scan your images for known vulnerabilities, run as a non-root user, avoid including secrets, and follow the best practices you've learned throughout this course. Think of this checklist as your pre-flight inspection before publishing.

### Block 10 — DONE

_300 chars · ~300 credits_

> You've completed the full Docker image lifecycle — from building and tagging to pushing, pulling, updating, and scanning. Before wrapping up, clean everything off your local machine. The docker system prune command with the dash a flag removes all unused images, containers, and networks in one shot.

### Block 11 — **MISSING**

_393 chars · ~393 credits_

> This is the final submission for the Docker course — congratulations on making it this far. Include the link to your public Docker Hub repository so I can pull your image myself. Capture the push, the pull-and-run, the version update, and the two versions running side by side. Confirm you completed the full security checklist. You now have a containerized application published to the world.

---

