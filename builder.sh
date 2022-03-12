#!/bin/bash

# docker-compose stop web
# docker-compose stop kibana
# docker-compose stop elasticsearch
# docker-compose rm -f

# Start up the containers
docker-compose up -d --build

# Check that containers are up and running
docker-compose ps

# run the web app
docker-compose logs -f web