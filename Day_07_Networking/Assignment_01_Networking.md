# Day 7 Assignment: Networking

## Overview

- **Topic:** Container Networking, Port Mapping, and Container-to-Container Communication
- **Type:** Technical / Hands-On
- **Estimated Time:** 30 minutes

## Background

### Docker Network Types

| Type | Description |
|------|-------------|
| `bridge` | Default. Containers on the same bridge can communicate. |
| `host` | Container shares the host's network (no isolation). |
| `none` | No networking at all. |
| Custom bridge | User-defined bridge with DNS-based container discovery. |

### Port Mapping

```bash
docker run -p 8080:80 nginx
#            ↑     ↑
#         host   container
```

`-p host:container` maps a host port to a container port.

### Custom Networks

Containers on the **default bridge** can only communicate by IP address. Containers on a **custom bridge** can find each other **by name** (built-in DNS).

```bash
docker network create my-net
docker run --network my-net --name api my-api
docker run --network my-net --name web my-web
# web can reach api at http://api:5000
```

---

## Part 1: Port Mapping

### Task A: Map Different Ports

```bash
docker run -d -p 8080:80 --name web1 nginx
docker run -d -p 8081:80 --name web2 nginx
docker run -d -p 8082:80 --name web3 nginx
```

Three Nginx containers, each on a different host port:

```bash
curl -s http://localhost:8080 | head -5
curl -s http://localhost:8081 | head -5
curl -s http://localhost:8082 | head -5
```

All three respond independently on different ports.

```bash
docker stop web1 web2 web3 && docker rm web1 web2 web3
```

### Task B: Random Port Mapping

```bash
docker run -d -P --name random-port nginx
docker port random-port
```

`-P` (capital P) maps all exposed ports to random host ports. `docker port` shows the mapping.

```bash
docker stop random-port && docker rm random-port
```

---

## Part 2: Default Bridge Network

### Task C: Inspect the Default Network

```bash
docker network ls
docker network inspect bridge
```

The default `bridge` network is always present.

### Task D: Communication on Default Bridge

```bash
docker run -d --name server1 nginx
docker run -d --name server2 nginx
```

Get server1's IP:

```bash
docker inspect --format='{{.NetworkSettings.IPAddress}}' server1
```

Try to reach server1 from server2 by IP:

```bash
docker exec server2 curl -s http://<server1-ip>
```

It works! Now try by name:

```bash
docker exec server2 sh -c 'curl -s http://server1 2>&1 || echo "Cannot resolve hostname — expected on default bridge"'
```

DNS resolution does NOT work on the default bridge network.

```bash
docker stop server1 server2 && docker rm server1 server2
```

---

## Part 3: Custom Bridge Networks

### Task E: Create a Custom Network

```bash
docker network create app-network
docker network ls
```

### Task F: Run Containers on the Custom Network

```bash
docker run -d --name api --network app-network nginx
docker run -d --name frontend --network app-network nginx
```

Test DNS resolution by name:

```bash
docker exec frontend curl -s http://api
```

It works! Custom bridge networks provide automatic DNS resolution between containers. This is the standard way to connect services.

### Task G: Isolate Networks

Create a second network and show containers can't cross:

```bash
docker network create isolated-network
docker run -d --name isolated-app --network isolated-network nginx

docker exec frontend sh -c 'curl -s --max-time 2 http://isolated-app 2>&1 || echo "Cannot reach isolated-app — different network"'
```

Containers on different networks are isolated from each other.

---

## Part 4: Multi-Container Application

### Task H: Build a Simple Two-Service App

Create a Python API:

```bash
mkdir ~/docker-network-demo
cd ~/docker-network-demo
```

Create `api.py`:

```python
from flask import Flask, jsonify
app = Flask(__name__)

@app.route("/api/greeting")
def greeting():
    return jsonify({"message": "Hello from the API service!"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
```

Create `Dockerfile.api`:

```dockerfile
FROM python:3.12-slim
WORKDIR /app
RUN pip install --no-cache-dir flask
COPY api.py .
EXPOSE 5000
CMD ["python", "api.py"]
```

Build and run on the custom network:

```bash
docker build -f Dockerfile.api -t my-api .
docker run -d --name api-service --network app-network my-api
```

Test from another container on the same network:

```bash
docker run --rm --network app-network python:3.12-slim \
    python3 -c "import urllib.request; print(urllib.request.urlopen('http://api-service:5000/api/greeting').read().decode())"
```

The container resolved `api-service` by name and got the response.

---

## Part 5: Cleanup

### Task I: Remove Everything

```bash
docker stop api frontend isolated-app api-service 2>/dev/null
docker rm api frontend isolated-app api-service 2>/dev/null
docker network rm app-network isolated-network
docker network ls
```

---

## Submission

Save a file named `Day_07_Output.md` in this folder containing the terminal output from each task.

## Grading Criteria

| Criteria | Points |
|----------|--------|
| Multiple containers mapped to different host ports | 10 |
| Default bridge inspected and IP-based communication shown | 15 |
| DNS failure on default bridge demonstrated | 10 |
| Custom network created | 10 |
| DNS resolution works on custom network | 15 |
| Network isolation between different networks shown | 10 |
| Two-service app communicating by name | 20 |
| All resources cleaned up | 10 |
| **Total** | **100** |
