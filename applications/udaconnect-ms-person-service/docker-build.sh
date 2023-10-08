#!/bin/bash

cp -f ../../build/types/* ./

docker build -t udaconnect-ms-person-service:latest -f Dockerfile .