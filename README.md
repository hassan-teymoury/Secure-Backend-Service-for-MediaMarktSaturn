# A Secure Backend Service Template for FASTAPI framework


## Introduction

In this repository I have tried to create a secure template for my backend projects using FastAPI which includes the following facilities:

- __Schemas__ to prevent the sql injection attacks
- __JWT (Json Web Tokens)__ Authentication and Authorization
- __Hashing__ user password with passlib to have encrypted credentials
- __Kubernetes__ configuration file example which can be set up with postgres secrets and project docker image and container.

    *You can find the Kubernetes config file in : __`devops/k8s/backend-core-manifiest-stage.yaml`__*

- __CORS__ Middleware configuration to prevent the requests from specific domains
- __Docker Compose__ Configuration
- __Test Scripts__ for database and routs
- __Using All CRUD operations__ for different models (tables)
- __Using Sqlalchemy ORM__ To facilitate the CRUD operations on tables in database



## Getting started with docker compose

To launch the API in your local host, first you need to specify the database connection settings for env variables in  __`app/database.py`, `Dockerfile`, `docker-compose.yaml` and `devops/k8s/backend-core-manifiest-stage.yaml`__.

After setting the env variables for database connection, you can launch the fastapi app using the following commands

```bash

git clone https://github.com/hassan-teymoury/Secure-Backend-Service-for-MediaMarktSaturn.git

cd Secure-Backend-Service-for-MediaMarktSaturn

docker compose build

docker compose up -d

```

__*Important Note*__ : If you have the postgresql server in your pc, make sure that it's down when you want to launch this app. 

To stop the postgresql server in ubuntu you can run the following command:

`sudo systemctl stop postgresql`