
# Power Plants API

## Overview

This API provides access to power plant data, allowing users to fetch top power plants based on specific metrics, obtain state-specific power plant data, and more.

## Prerequisites

- Docker

### Ensuring Docker is Running

Before starting the API, ensure that Docker is up and running on your system. If you haven't installed Docker, you can download and install it from [Docker's official website](https://www.docker.com/products/docker-desktop).

## Setup & Running

1. Clone the repository:
   ```bash
   git clone git@github.com:omarkahwaji/power_plants.git
   ```

2. To start the service using Docker Compose, execute:
   ```bash
   make compose
   ```

3. The API will be accessible at `http://localhost:8000`.

## Makefile Commands

- **Linting the Code**:
   ```bash
   make lint
   ```

- **Testing the Code**:
   ```bash
   make test
   ```

- **Building the Docker Image**:
   ```bash
   make docker-build
   ```

- **Cleaning Python Artifacts**:
   ```bash
   make clean-pyc
   ```

- **Cleaning Build Artifacts**:
   ```bash
   make clean-build
   ```

- **Clean All (Python + Build Artifacts)**:
   ```bash
   make clean
   ```

## Available Endpoints

1. **Root Endpoint**:
   Fetches a welcome message.
   ```bash
   curl -X 'GET' \
     -H 'accept: application/json' \
     'http://localhost:8000/'
   ```

2. **Top Plants Endpoint**:
   Returns the top `n` power plants based on a specified metric.
   ```bash
   curl -X 'GET' \
     -H 'accept: application/json' \
     -H 'Content-Type: application/json' \
     -d '{
           "top_number": 5,
           "metric": "Plant annual net generation (MWh)"
         }' \
     'http://localhost:8000/plants/top'

   ```

3. **States Info Endpoint**:
   Provides a summary based on a metric for all states.
   ```bash
   curl -X 'GET' \
     -H 'accept: application/json' \
     -H 'Content-Type: application/json' \
     -d '{
           "metric": "Plant annual net generation (MWh)"
         }' \
     'http://localhost:8000/plants/states'

   ```

4. **State-specific Endpoint**:
   Returns data for power plants in a specific state, e.g., "CA" for California.
   ```bash
   curl -X 'GET' \
     -H 'accept: application/json' \
     -H 'Content-Type: application/json' \
     -d '{
           "state": "CA"
         }' \
     'http://localhost:8000/plants/state/{state}'

   ```

5. **Health Check Endpoint**:
   Returns a 200 OK status if the service is healthy.
   ```bash
   curl -X GET "http://localhost:8000/health"
   ```



## Docs

Swagger documentations are available at `http://localhost:8000/Docs`.

## Shutdown

To shut down the service and remove the containers, execute:
```bash
docker-compose down
```

---
