#!/bin/bash

# Build the application
docker-compose build

# Start the application using Docker Compose
docker-compose up

## Scale the client, server, and parser services horizontally
#docker-compose up --scale client=5 --scale server=3 --scale parser=2
