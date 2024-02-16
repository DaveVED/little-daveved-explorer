# little-daveved-web-app

A web app built for "Little David".

## Components (or Features)

- :mag_right: Explorer :mag_right: -- A micro site that allows people travling to the baby shower to drop pens on a map. Suggesting places for us to take you, and where they travled from. 

## Usage

All commands should be from the projects root directory.

### Local Startup

```bash
uvicorn daveved.main:app --port 8001 --host 0.0.0.0 --reload
```

### Docker
```bash
docker build -t little-daveved-web-app .
docker run -p 8001:8001 little-daveved-web-app
```

### Docker Compose
```bash
docker-compose up -d
```

### Docker Hub
```bash
docker pull daveved/little-daveved-web-app
docker run -d -p 8001:8001 daveved/little-daveved-web-app
```