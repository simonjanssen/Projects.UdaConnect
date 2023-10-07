#!/bin/bash

cp -f ../../build/types/* ./

docker build -t udaconnect-ms-location-api:latest -f Dockerfile .