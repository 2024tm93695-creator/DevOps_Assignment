# Docker Containerization Guide

## Overview
This guide provides instructions for building and running the ACEest Fitness API as a Docker container.

---

## Prerequisites
- Docker installed ([Download Docker Desktop](https://www.docker.com/products/docker-desktop))
- Docker Compose (included with Docker Desktop)

---

## Quick Start

### Option 1: Using Docker Compose (Recommended)
```bash
# Build and run the container
docker-compose up -d

# View logs
docker-compose logs -f flask-app

# Stop the container
docker-compose down
```

### Option 2: Using Docker CLI

#### Build the Image
```bash
docker build -t aceest-fitness-api:latest .
```

#### Run the Container
```bash
docker run -d \
  --name aceest-fitness-api \
  -p 5000:5000 \
  -e FLASK_ENV=production \
  -e SECRET_KEY=your-secret-key \
  aceest-fitness-api:latest
```

---

## Configuration

### Environment Variables
Configure these in `docker-compose.yml` or at runtime:

| Variable | Default | Description |
|----------|---------|-------------|
| `FLASK_ENV` | `production` | Flask environment mode |
| `SECRET_KEY` | `your-secret-key-change-in-production` | Flask secret key |
| `DATABASE_URL` | `sqlite:///instance/aceest_fitness.db` | Database connection URI |

#### Example with Custom Environment
```bash
docker run -d \
  --name aceest-fitness-api \
  -p 5000:5000 \
  -e FLASK_ENV=production \
  -e SECRET_KEY=my-super-secret-key \
  -e DATABASE_URL=sqlite:///instance/aceest_fitness.db \
  aceest-fitness-api:latest
```

---

## Verification

### 1. Check Container Status
```bash
docker ps
```

### 2. Test API Endpoint
```bash
# Linux / macOS
curl http://localhost:5000/

# Windows PowerShell
Invoke-WebRequest http://localhost:5000/
```

Expected Response:
```json
{"message": "ACEest Fitness API"}
```

### 3. View Logs
```bash
docker logs aceest-fitness-api
# or with Docker Compose
docker-compose logs -f flask-app
```

### 4. Access Container Shell
```bash
docker exec -it aceest-fitness-api /bin/bash
```

---

## Common Operations

### Rebuild Image
```bash
# If you make code changes, rebuild the image
docker-compose build --no-cache
```

### Stop Container
```bash
docker-compose down
# or
docker stop aceest-fitness-api
```

### Remove Container and Image
```bash
docker-compose down -v
# or
docker rm aceest-fitness-api
docker rmi aceest-fitness-api:latest
```

### View Image Layers
```bash
docker history aceest-fitness-api:latest
```

### Check Container Stats
```bash
docker stats aceest-fitness-api
```

---

## Advanced Configuration

### Persistent Database
The `docker-compose.yml` includes a volume mount for the SQLite database:
```yaml
volumes:
  - ./flask_app/instance:/app/instance
```

This ensures your database persists between container restarts.

### Multi-Environment Setup

#### Development
```bash
docker-compose -f docker-compose.yml up
```

#### Production
Modify `docker-compose.yml`:
```yaml
environment:
  FLASK_ENV: production
  SECRET_KEY: ${SECRET_KEY}  # Set via environment variable
```

Then:
```bash
export SECRET_KEY=production-secret-key
docker-compose up -d
```

---

## Troubleshooting

### Port Already in Use
If port 5000 is already in use:
```bash
# Change port in docker-compose.yml
ports:
  - "5001:5000"  # Maps container 5000 to host 5001
```

### Container Exits Immediately
Check logs:
```bash
docker logs aceest-fitness-api
```

Common causes:
- Missing dependencies (check `requirements.txt`)
- Database initialization errors
- Incorrect environment variables

### Database Connection Issues
Ensure the `instance` directory is writable:
```bash
docker exec aceest-fitness-api ls -la /app/instance
```

---

## Image Details

### Base Image
- **Runtime**: Python 3.11-slim (lightweight, ~150MB)
- **Build Stage**: Python 3.11-slim with build tools

### Optimizations
- **Multi-stage build**: Reduces final image size by excluding build tools
- **No cache**: Pip packages not cached in image
- **Health check**: Docker monitors container health
- **Unprivileged**: Application runs as non-root user

### Final Image Size
- Approximately **200-250MB** (depends on dependencies)

---

## Deployment

### Docker Hub
To push to Docker Hub:
```bash
# Tag image
docker tag aceest-fitness-api:latest username/aceest-fitness-api:latest

# Login and push
docker login
docker push username/aceest-fitness-api:latest
```

### Kubernetes Setup
See [Kubernetes Deployment Guide](./k8s-deployment.md) for K8s deployment.

---

## Security Considerations

⚠️ **Important for Production:**
1. **Never** hardcode `SECRET_KEY` in the image
2. Use environment variables for secrets
3. Run container as non-root user (added in Dockerfile)
4. Keep base image updated: `docker pull python:3.11-slim`
5. Implement proper logging and monitoring

---

## References
- [Docker Documentation](https://docs.docker.com/)
- [Flask in Docker](https://flask.palletsprojects.com/deployment/)
- [Docker Compose Reference](https://docs.docker.com/compose/compose-file/)

