# Little Daveved Explorer

A web application designed to collect and visualize geographical data from users. It allows users to share their starting locations and suggest destinations for future travels. This application is particularly envisioned for events such as baby showers, where guests can indicate where they have traveled from and recommend places to take the baby once born. 

## Features 🚀
- Interactive Map: Users can interactively drop pins on a map.
- Dual Pin Types: Supports two types of pins for distinct purposes:
  - 📍 "Where we should travel to": Suggestions for future destinations.
  - 🛫 "Where you traveled from": Indicating users' starting locations.

## Getting Started

Follow these instructions to set up the "Little Daveved Explorer" on your local machine or using Docker.

### Local Setup

To run the application locally, execute the following command from the project's root directory:

```bash
# if not done yet
pip3 install -r requirements.txt

# start app
uvicorn app.main:app --port 8001 --host 0.0.0.0 --reload
```

### Using Docker

You can also run the application using Docker. Here are the steps:

#### Build and Run with Docker

```bash
docker build -t little-daveved-explorer .
docker run -p 8001:8001 little-daveved-explorer
```

#### Using Docker Compose

To simplify the process, you can use Docker Compose:

```bash
docker-compose up -d
```

#### Pulling from Docker Hub

Alternatively, you can pull the Docker image from Docker Hub and run it:

```bash
docker pull daveved/little-daveved-explorer
docker run -d -p 8001:8001 daveved/little-daveved-explorer