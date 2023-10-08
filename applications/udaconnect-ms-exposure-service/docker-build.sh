#!/bin/bash

cp -f ../../build/types/* ./

docker build -t udaconnect-ms-exposure-service:latest -f Dockerfile .