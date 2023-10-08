#!/bin/bash

cp -f ../../build/types/* ./

docker build -t udaconnect-ms-location-service:latest -f Dockerfile .