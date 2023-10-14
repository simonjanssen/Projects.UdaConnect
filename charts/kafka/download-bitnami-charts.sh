#!/bin/bash

rm -rf charts-main 

rm -f *.zip*

wget https://github.com/bitnami/charts/archive/refs/heads/main.zip

unzip main.zip

rm -f main.zip

cp -r ./charts-main/bitnami/kafka/* ./

rm -rf charts-main