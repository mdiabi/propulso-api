# Propulso FastAPI Backend

This repository contains a FastAPI backend that can be easily deployed using Docker.

## Prerequisites

Make sure you have [Docker](https://docs.docker.com/get-docker/) installed on your system.

## Usage

### Build Docker Image

Build the Docker image for the FastAPI backend:

```bash
docker build -t my-fastapi-app .
```

### Run Docker Container

Run a Docker container based on the built image:

```bash
docker run -d -p 8000:8000 my-fastapi-app
```

This command starts a container in detached mode and maps port 8000 from the host to the container.

### Accessing the API

The FastAPI server is now running. You can access it at:

```
http://localhost:8000
```

### Swagger Documentation

The API documentation (Swagger UI) can be accessed at:

```
http://localhost:8000/docs
```

Use the Swagger documentation to explore the available endpoints, send requests, and view responses.

## Configuration

### Environment Variables

There are no specific environment variables required for this application in its current state. However, you can configure environment variables if needed in the Dockerfile or FastAPI application.
