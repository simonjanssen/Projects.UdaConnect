#!/bin/bash

rm -r /mnt/data
mkdir -p /mnt/data/postgres
mkdir -p /mnt/data/pgadmin
mkdir -p /mnt/data/kafka
chown -R 5050:5050 /mnt/data/pgadmin
chown -R 1001:1001 /mnt/data/kafka 