# Day 6 Assignment: Volumes and Persistence

## Overview

- **Topic:** Docker Volumes, Bind Mounts, and Persisting Data
- **Type:** Technical / Hands-On
- **Estimated Time:** 30 minutes

## Background

Containers are **ephemeral** — when you remove a container, its data is gone. Docker provides two ways to persist data:

### Named Volumes (Docker-Managed)

Docker manages the storage location. Best for data you don't need to access directly from the host.

```bash
docker volume create my-data
docker run -v my-data:/app/data my-app
```

### Bind Mounts (Host Directory)

Map a specific host directory into the container. Best for development (live code editing).

```bash
docker run -v /path/on/host:/path/in/container my-app
docker run -v $(pwd):/app my-app
```

### Comparison

| Feature | Named Volume | Bind Mount |
|---------|-------------|------------|
| Managed by | Docker | You |
| Location | Docker storage dir | Anywhere on host |
| Pre-populated | Yes (from image) | No (overwrites) |
| Use case | Databases, persistent data | Development, config |
| Portability | Works everywhere | Host-path specific |

---

## Part 1: Named Volumes

### Task A: Create and Use a Volume

```bash
docker volume create app-data
docker volume ls
docker volume inspect app-data
```

### Task B: Write Data to a Volume

```bash
docker run --rm -v app-data:/data alpine sh -c 'echo "Hello from container 1" > /data/message.txt'
```

### Task C: Read Data from Another Container

```bash
docker run --rm -v app-data:/data alpine cat /data/message.txt
```

The data persists even though the first container was removed! The volume exists independently.

### Task D: Prove Persistence

```bash
docker run --rm -v app-data:/data alpine sh -c 'echo "Second message" >> /data/message.txt'
docker run --rm -v app-data:/data alpine cat /data/message.txt
```

Both messages are there. Data accumulates across containers.

---

## Part 2: Bind Mounts

### Task E: Set Up a Development Workflow

```bash
mkdir ~/docker-dev
cd ~/docker-dev
```

Create `index.html`:

```html
<h1>Hello from Docker!</h1>
<p>Edit this file and refresh your browser.</p>
```

Run Nginx with a bind mount:

```bash
docker run -d -p 8080:80 -v $(pwd):/usr/share/nginx/html --name dev-server nginx
```

Visit `http://localhost:8080` or:

```bash
curl http://localhost:8080
```

### Task F: Live Editing

Edit `index.html` on your host:

```bash
echo "<h1>Updated!</h1><p>Changed without rebuilding.</p>" > index.html
curl http://localhost:8080
```

The change is **instant** — no rebuild, no restart. The container sees the host file directly. This is why bind mounts are essential for development.

### Task G: Clean Up

```bash
docker stop dev-server && docker rm dev-server
```

---

## Part 3: Database Persistence

### Task H: Run a Database Without a Volume

```bash
docker run -d --name db-no-vol -e POSTGRES_PASSWORD=secret postgres:16-alpine
sleep 3
docker exec db-no-vol psql -U postgres -c "CREATE TABLE test(id int, name text);"
docker exec db-no-vol psql -U postgres -c "INSERT INTO test VALUES (1, 'Campbell');"
docker exec db-no-vol psql -U postgres -c "SELECT * FROM test;"
```

Now destroy and recreate:

```bash
docker stop db-no-vol && docker rm db-no-vol
docker run -d --name db-no-vol -e POSTGRES_PASSWORD=secret postgres:16-alpine
sleep 3
docker exec db-no-vol psql -U postgres -c "SELECT * FROM test;" 2>&1
```

The table is gone — all data lost.

### Task I: Run a Database With a Volume

```bash
docker stop db-no-vol && docker rm db-no-vol
docker volume create pg-data
docker run -d --name db-with-vol -e POSTGRES_PASSWORD=secret -v pg-data:/var/lib/postgresql/data postgres:16-alpine
sleep 3
docker exec db-with-vol psql -U postgres -c "CREATE TABLE test(id int, name text);"
docker exec db-with-vol psql -U postgres -c "INSERT INTO test VALUES (1, 'Campbell');"
docker exec db-with-vol psql -U postgres -c "SELECT * FROM test;"
```

Destroy and recreate with the same volume:

```bash
docker stop db-with-vol && docker rm db-with-vol
docker run -d --name db-with-vol -e POSTGRES_PASSWORD=secret -v pg-data:/var/lib/postgresql/data postgres:16-alpine
sleep 3
docker exec db-with-vol psql -U postgres -c "SELECT * FROM test;"
```

The data survived! The volume persists independently of the container.

---

## Part 4: Volume Management

### Task J: List and Inspect Volumes

```bash
docker volume ls
docker volume inspect pg-data
```

### Task K: Remove Volumes

```bash
docker stop db-with-vol && docker rm db-with-vol
docker volume rm pg-data
docker volume rm app-data
docker volume ls
```

Remove all unused volumes:

```bash
docker volume prune
```

---

## Submission

Save a file named `Day_06_Output.md` in this folder containing the terminal output from each task.

## Grading Criteria

| Criteria | Points |
|----------|--------|
| Named volume created and inspected | 10 |
| Data written and read across containers | 15 |
| Bind mount used for live development | 15 |
| Live editing demonstrated (change reflected without rebuild) | 10 |
| Database WITHOUT volume — data loss shown | 15 |
| Database WITH volume — data persistence shown | 20 |
| Volumes listed, inspected, and cleaned up | 10 |
| All containers cleaned up | 5 |
| **Total** | **100** |
