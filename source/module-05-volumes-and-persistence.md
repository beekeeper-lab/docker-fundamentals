# Module 6: Volumes and Persistence

> 🏷️ Useful Soon

> 🎯 **Teach:** How to persist data across container lifecycles using Docker volumes and bind mounts.
> **See:** Named volumes surviving container destruction, live-editing with bind mounts, and database persistence.
> **Feel:** Confident that you can manage data in Docker without losing it.

> 🔄 **Where this fits:** You've learned that containers are ephemeral — data disappears when a container is removed. Volumes solve that problem. This is essential knowledge before working with databases in Docker Compose (Modules 8 and 9).

## Why Volumes Matter

> 🎯 **Teach:** Why containers lose data by default and the two strategies Docker provides for persistence.
> **See:** A side-by-side comparison of named volumes and bind mounts with concrete use cases.
> **Feel:** Motivated to always plan a persistence strategy before running stateful containers.

> 🎙️ Containers are ephemeral — when you remove a container, its data is gone. This is great for stateless applications, but terrible for databases, file uploads, or anything that needs to survive a restart. Docker provides two solutions: named volumes, which Docker manages for you, and bind mounts, which map a specific directory from your host into the container.

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

> 🎙️ Here's a quick comparison to help you decide which to use. Named volumes are managed by Docker and are best for production data like databases. Bind mounts point to a specific directory on your host and are best for development where you want to edit files live.

### Comparison

| Feature | Named Volume | Bind Mount |
|---------|-------------|------------|
| Managed by | Docker | You |
| Location | Docker storage dir | Anywhere on host |
| Pre-populated | Yes (from image) | No (overwrites) |
| Use case | Databases, persistent data | Development, config |
| Portability | Works everywhere | Host-path specific |

> 💡 **Remember this one thing:** Named volumes for production data (databases, uploads). Bind mounts for development (live code editing). Don't mix them up — bind mounts overwrite what's in the image, while named volumes preserve it.

## Named Volumes

> 🎯 **Teach:** How to create, use, and share named volumes between containers.
> **See:** Data persisting across container restarts and being shared between containers.
> **Feel:** Trust that Docker volumes reliably store your data.

> 🎙️ Named volumes are Docker-managed storage that exists independently of any container. You create a volume, mount it into a container, write data, destroy the container, and the data is still there. You can even mount the same volume into multiple containers to share data between them.

> 🎙️ Let's start by creating a named volume. The docker volume create command creates a volume that Docker manages for you. You can then list all volumes and inspect one to see where Docker actually stores the data on your host filesystem.

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

## Bind Mounts

> 🎯 **Teach:** How bind mounts map host directories into containers for live development workflows.
> **See:** Editing a file on the host and seeing the change instantly in the running container.
> **Feel:** Excited about a development workflow that eliminates rebuilds.

> 🎙️ Bind mounts are the developer's best friend. Instead of Docker managing the storage, you map a directory from your host machine directly into the container. Edit a file on your host, and the change is instantly visible inside the container. This means you can use your favorite editor and tools while the application runs inside Docker — no rebuild needed.

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

> 🎙️ Now for the magic. Edit the HTML file on your host machine and then curl the page again. You'll see the change immediately without restarting or rebuilding anything. This is the development workflow that makes bind mounts so valuable.

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

## Database Persistence

> 🎯 **Teach:** Why databases absolutely require volumes and what happens without them.
> **See:** Data loss without a volume versus data survival with a volume — side by side.
> **Feel:** A healthy fear of running databases without volumes.

> 🎙️ This is the most important demonstration in this module. You're going to run a PostgreSQL database without a volume, insert data, destroy the container, recreate it, and watch your data vanish. Then you'll do the same thing with a volume and see that the data survives. This is why you must always use volumes with databases.

> 🎙️ First you'll run Postgres without a volume and see what happens when the container is destroyed. Pay close attention to the error you get when you try to query the table after recreating the container. That error is the whole reason volumes exist.

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

## Volume Management

> 🎯 **Teach:** How to list, inspect, remove, and prune Docker volumes to keep your system clean.
> **See:** Commands for auditing and cleaning up unused volumes.
> **Feel:** Confident maintaining a tidy Docker environment as part of your regular workflow.

> 🎙️ Like images and containers, volumes need housekeeping. Docker provides commands to list, inspect, and remove volumes. Orphaned volumes from deleted containers can accumulate over time, so periodically running docker volume prune keeps your system clean.

> 🎙️ Let's do some housekeeping. You can list all volumes on your system, inspect individual ones to see their details, and remove ones you no longer need. Getting in the habit of cleaning up unused volumes will keep your Docker environment tidy.

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

> 🎙️ You now understand the two main ways to persist data in Docker. Named volumes are your go-to for databases and production data, while bind mounts are essential for development workflows. The database demonstration showed you exactly why running a database without a volume is a recipe for data loss. Keep these patterns in mind as you move into Docker Compose.

## Submission

Save a file named `Day_06_Output.md` in this folder containing the terminal output from each task.

### Grading Criteria

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
