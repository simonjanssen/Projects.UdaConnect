#!/bin/bash

cp -f ../../build/types/* ./

docker build -t udaconnect-ms-person-api:latest -f Dockerfile .