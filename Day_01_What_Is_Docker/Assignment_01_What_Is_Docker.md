# Day 1 Assignment: What Is Docker

## Overview

- **Topic:** Containers vs VMs, Docker Architecture, and Installation
- **Type:** Technical / Hands-On
- **Estimated Time:** 30 minutes

## Background

### What Is Docker?

Docker is a platform for running applications in **containers** — lightweight, isolated environments that package your code with everything it needs to run (libraries, dependencies, config).

### Containers vs Virtual Machines

| Feature | Container | Virtual Machine |
|---------|-----------|-----------------|
| Size | Megabytes | Gigabytes |
| Startup | Seconds | Minutes |
| OS | Shares host kernel | Full guest OS |
| Isolation | Process-level | Hardware-level |
| Overhead | Minimal | Significant |

A VM virtualizes the **hardware** (runs a full OS). A container virtualizes the **operating system** (shares the host kernel, isolates the process).

### Docker Architecture

```
Docker Client (CLI)
    ↓ commands
Docker Daemon (dockerd)
    ↓ manages
Images → Containers
```

- **Image** — A read-only template (like a class in OOP). Contains the OS, your app, and dependencies.
- **Container** — A running instance of an image (like an object). Isolated, ephemeral.
- **Docker Daemon** — Background service that manages containers.
- **Docker CLI** — Command-line tool you interact with.

---

## Part 1: Install Docker

### Task A: Install Docker

Follow the instructions for your OS:

- **Linux:** Install Docker Engine
  ```bash
  # Ubuntu/Debian
  sudo apt update
  sudo apt install docker.io
  sudo systemctl start docker
  sudo systemctl enable docker
  sudo usermod -aG docker $USER
  ```
  Log out and back in for the group change to take effect.

- **macOS:** Install [Docker Desktop](https://www.docker.com/products/docker-desktop/)
- **Windows:** Install [Docker Desktop](https://www.docker.com/products/docker-desktop/) with WSL 2 backend

### Task B: Verify Installation

```bash
docker --version
docker info
```

`docker --version` shows the installed version. `docker info` shows details about the Docker daemon (containers, images, storage driver, etc.).

### Task C: Test with Hello World

```bash
docker run hello-world
```

This command:
1. Looks for the `hello-world` image locally
2. Doesn't find it → downloads it from Docker Hub
3. Creates a container from the image
4. Runs the container (prints a message)
5. Container exits

Read the output — it explains exactly what happened.

---

## Part 2: Explore Docker Commands

### Task D: See What Happened

```bash
docker images
```

You should see the `hello-world` image listed. It was downloaded (pulled) from Docker Hub.

```bash
docker ps
```

No running containers — `hello-world` already exited. Show ALL containers (including stopped):

```bash
docker ps -a
```

You should see the stopped `hello-world` container with an `Exited` status.

### Task E: Clean Up

```bash
docker rm $(docker ps -a -q --filter ancestor=hello-world)
docker rmi hello-world
docker images
docker ps -a
```

- `docker rm` removes stopped containers
- `docker rmi` removes images
- Now both lists should be clean

---

## Part 3: Run a Real Container

### Task F: Run an Interactive Ubuntu Container

```bash
docker run -it ubuntu bash
```

Flags:
- `-i` — Interactive (keep STDIN open)
- `-t` — Allocate a terminal (TTY)

You're now inside an Ubuntu container! Explore:

```bash
cat /etc/os-release
whoami
ls /
pwd
hostname
```

You're running a full Ubuntu environment, but it started in seconds and uses barely any resources. This is the power of containers.

Install something inside the container:

```bash
apt update
apt install -y curl
curl --version
```

Exit the container:

```bash
exit
```

### Task G: Prove Isolation

Run another Ubuntu container:

```bash
docker run -it ubuntu bash
```

Check for curl:

```bash
which curl
```

It's not there! Each container starts fresh from the image. The curl you installed in the previous container is gone because containers are **ephemeral** — changes don't persist unless you explicitly save them.

Exit:

```bash
exit
```

---

## Part 4: Running a Web Server

### Task H: Run Nginx

```bash
docker run -d -p 8080:80 --name my-nginx nginx
```

Flags:
- `-d` — Detached mode (runs in background)
- `-p 8080:80` — Map port 8080 on your machine to port 80 in the container
- `--name my-nginx` — Give the container a name

Check it's running:

```bash
docker ps
```

Open a browser and go to `http://localhost:8080` — you should see the Nginx welcome page.

Or test from the terminal:

```bash
curl http://localhost:8080
```

### Task I: Stop and Remove

```bash
docker stop my-nginx
docker rm my-nginx
```

---

## Submission

Save a file named `Day_01_Output.md` in this folder containing the terminal output from each task.

## Grading Criteria

| Criteria | Points |
|----------|--------|
| Docker installed and version confirmed | 10 |
| `docker info` output captured | 10 |
| `hello-world` run and output understood | 10 |
| `docker images` and `docker ps -a` output shown | 10 |
| Interactive Ubuntu container explored | 15 |
| Isolation demonstrated (curl missing in second container) | 15 |
| Nginx container run with port mapping | 15 |
| Browser or curl confirmed Nginx working | 10 |
| Containers cleaned up | 5 |
| **Total** | **100** |
