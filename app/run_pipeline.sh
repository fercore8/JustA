#!/bin/bash

# Build the Docker images for the client, server, parser, and GUI
docker build -t client client/
docker build -t server server/
docker build -t parser parser/
docker build -t gui gui/

# Create a Docker network for the services to communicate on
docker network create microservice-network

# Start the services using Docker Compose
docker-compose up -d

# Scale the client, server, and parser services horizontally
#docker-compose up --scale client=5 --scale server=3 --scale parser=2  # test this line
