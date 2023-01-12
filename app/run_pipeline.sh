#!/bin/bash

# Build the server image
docker build -t my-server .

# Build the application
docker-compose build

# Start the application using Docker Compose
docker-compose up

# Create a Docker network for the services to communicate on
docker network create app-tier
docker network connect app-tier app-rabbitmq-1
# Scale the client, server, and parser services horizontally
#docker-compose up --scale client=5 --scale server=3 --scale parser=2  # test this line
