# Federated Learning Clinical Safety Server

[![Tests](https://github.com/AlexDobsonPleming/federated-learning-clinical-safety-server/actions/workflows/ci.yml/badge.svg)](https://github.com/AlexDobsonPleming/federated-learning-clinical-safety-server/actions/workflows/ci.yml)

[![Docker-Compose Smoke Test](https://github.com/AlexDobsonPleming/federated-learning-clinical-safety-server/actions/workflows/compose-test.yml/badge.svg)](https://github.com/AlexDobsonPleming/federated-learning-clinical-safety-server/actions/workflows/compose-test.yml)

This is the documentation for the Federated Learning Clinical Safety Dashboard Server! This project provides a Django REST API for managing safety statics about FL models and their local counterparts.

---

## Deployment with Docker

```bash
docker compose -f docker-compose.demo.yml up --build --force-recreate --remove-orphans

#if you're on vht-dev and don't have access to modern docker
docker-compose -f docker-compose.demo.yml up --build --force-recreate --remove-orphans
```

Deploys with the default demo credentials:
```
Username: demo
Password: demo123
```

### HTTPS with ngrok

HTTPS is necessary for secure front-end integration to prevent mixed-mode requests.

This project is optimised to use ngrok for tunneling out of vht-dev.

You will need to [install it from here](https://dashboard.ngrok.com/get-started/setup/linux).

Once installed you can run it from:
```bash
nohup ./ngrok http --url=<your ngrok url> 0.0.0.0:8000 > ngrok.log 2>&1
```

## Development prerequisites

Before you begin, ensure you have the following installed:

* Python 3.10+

---

## Setup & Installation

1. Clone the repository:

   ```bash
   git clone git@github.com:AlexDobsonPleming/federated-learning-clinical-safety-server.git
   cd federated-learning-clinical-safety-server
   ```

2. Create and activate a virtual environment:

```bash
python3 -m venv .venv
```    

```bash
source .venv/bin/activate
```

3. Install Python dependencies:

   ```bash
   pip install -r requirements.txt
   ```

---

## Database & Migrations

Run migrations:

```bash
python manage.py migrate
```

---

## Create Superuser

```bash
python manage.py createsuperuser
```

---

## Seed Initial Data (optional: for demonstration purposes)

```bash
python manage.py seed_flmodels
```

---

## Running the Server

```bash
python manage.py runserver
```

The API will be available at `http://127.0.0.1:8000/api/`

#### Running a public server

```bash
nohup python3 manage.py runserver 0.0.0.0:8000 &
```
This server will bind to 0.0.0.0:8000

Combined with ngrok this will make your api pubicly accessible in development mode.

---

## Front-End Client

Please follow corresponding instructions on the [front-end repository](https://github.com/AlexDobsonPleming/federated-learning-clinical-safety-client).

## Available Management Commands

* `seed_flmodels`: Seed sample FLModel data.
* `create_uploader <username>`: Create machine user with API token (no password login).

---

## 🔧 API SDK

An [SDK is available](https://github.com/AlexDobsonPleming/federated-learning-clinical-safety-sdk) for accessing the api in a typesafe manner.

### Testing the docker integration tests

The SDK is tested against this api with integration tests built with docker.

Test the compose file with:
```bash
docker compose -f docker-compose.test.yml up -d --build
```