# Day 3 Assignment: Container Management

## Overview

- **Topic:** Starting, Stopping, Restarting, Logging, and Executing Commands in Containers
- **Type:** Technical / Hands-On
- **Estimated Time:** 30 minutes

## Background

### Container Lifecycle

```
Created → Running → Paused → Running → Stopped → Removed
           ↑                                        |
           └────────── Restarted ───────────────────┘
```

### Management Commands

| Command | Purpose |
|---------|---------|
| `docker start <name>` | Start a stopped container |
| `docker stop <name>` | Gracefully stop (SIGTERM, then SIGKILL after 10s) |
| `docker kill <name>` | Force stop immediately (SIGKILL) |
| `docker restart <name>` | Stop and start again |
| `docker pause <name>` | Freeze all processes |
| `docker unpause <name>` | Resume frozen processes |
| `docker rm <name>` | Remove a stopped container |
| `docker logs <name>` | View container output |
| `docker exec <name> <cmd>` | Run a command in a running container |
| `docker cp` | Copy files between container and host |

---

## Part 1: Container Lifecycle

### Task A: Create a Long-Running Container

```bash
docker run -d --name my-app nginx
docker ps
```

### Task B: Stop and Start

```bash
docker stop my-app
docker ps            # Not listed — it's stopped
docker ps -a         # Listed with status "Exited"
docker start my-app
docker ps            # Running again
```

### Task C: Pause and Unpause

```bash
docker pause my-app
docker ps            # Status shows "Paused"
docker unpause my-app
docker ps            # Back to "Up"
```

### Task D: Restart

```bash
docker restart my-app
docker ps
```

Notice the "Up" time resets — the container was fully stopped and restarted.

---

## Part 2: Logs

### Task E: View Container Logs

```bash
docker logs my-app
```

Shows all output from the container since it started.

Useful flags:

```bash
docker logs --tail 5 my-app       # Last 5 lines
docker logs --since 1m my-app     # Last 1 minute
docker logs -f my-app             # Follow (live stream) — Ctrl+C to stop
```

### Task F: Generate Some Logs

Open another terminal and make some requests to generate log entries:

```bash
curl http://localhost:80 2>/dev/null || docker exec my-app curl -s http://localhost
```

Or use a container that produces lots of output:

```bash
docker run -d --name log-demo busybox sh -c 'while true; do echo "$(date): heartbeat"; sleep 2; done'
docker logs -f log-demo
```

Press `Ctrl+C` to stop following. Then:

```bash
docker logs --tail 3 log-demo
docker stop log-demo && docker rm log-demo
```

---

## Part 3: Executing Commands in Running Containers

### Task G: Run Commands with `docker exec`

```bash
docker exec my-app hostname
docker exec my-app cat /etc/nginx/nginx.conf
docker exec my-app ls /usr/share/nginx/html/
```

`exec` runs a command inside a **running** container without stopping it.

### Task H: Open an Interactive Shell

```bash
docker exec -it my-app bash
```

You're now inside the running Nginx container. Explore:

```bash
ls /usr/share/nginx/html/
cat /usr/share/nginx/html/index.html
echo "<h1>Modified from inside!</h1>" > /usr/share/nginx/html/index.html
exit
```

The Nginx container is still running — `exec` didn't affect it.

### Task I: Verify the Change

```bash
docker exec my-app cat /usr/share/nginx/html/index.html
```

The file was modified inside the running container. But remember — this change is ephemeral. If you remove and recreate the container, it's gone.

---

## Part 4: Copying Files

### Task J: Copy Files Between Host and Container

Copy a file FROM a container to your host:

```bash
docker cp my-app:/etc/nginx/nginx.conf ./nginx.conf
cat nginx.conf
```

Copy a file TO a container from your host:

```bash
echo "<h1>Hello from the host!</h1>" > custom-index.html
docker cp custom-index.html my-app:/usr/share/nginx/html/index.html
docker exec my-app cat /usr/share/nginx/html/index.html
```

---

## Part 5: Bulk Operations

### Task K: Managing Multiple Containers

Start several containers:

```bash
docker run -d --name app1 nginx
docker run -d --name app2 nginx
docker run -d --name app3 nginx
docker ps
```

Stop all at once:

```bash
docker stop app1 app2 app3
```

Remove all stopped containers:

```bash
docker container prune
```

`prune` removes ALL stopped containers. Answer `y` to confirm.

### Task L: System Cleanup

```bash
docker system df
```

This shows disk usage by images, containers, and volumes. Clean everything unused:

```bash
docker system prune
```

Also clean up the remaining containers:

```bash
docker stop my-app && docker rm my-app
```

---

## Submission

Save a file named `Day_03_Output.md` in this folder containing the terminal output from each task.

## Grading Criteria

| Criteria | Points |
|----------|--------|
| Container started, stopped, and restarted | 10 |
| Pause and unpause demonstrated | 10 |
| Logs viewed with --tail, --since, and -f | 15 |
| `docker exec` used to run commands | 15 |
| Interactive shell opened in running container | 10 |
| File modified inside container | 10 |
| Files copied with `docker cp` (both directions) | 15 |
| Multiple containers managed and pruned | 10 |
| `docker system df` output captured | 5 |
| **Total** | **100** |
