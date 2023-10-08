#!/bin/bash

cp -f ../../build/types/* ./

docker build -t udaconnect-exposure-service:latest -f Dockerfile .