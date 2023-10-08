#!/bin/bash

docker run --rm -it \
    -e DB_HOST=postgres \
    -e DB_PORT=5432 \
    -e DB_USER=admin \
    -e DB_PASSWORD=secret \
    -e DB_NAME=udaconnect \
    udaconnect-ms-exposure-service:latest