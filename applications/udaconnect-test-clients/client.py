
import argparse
from datetime import datetime
import httpx
import math
from time import sleep
from random import randint, random, randrange
from loguru import logger
import time

parser = argparse.ArgumentParser()
parser.add_argument("-i", "--id", type=int, required=True)
args = parser.parse_args()

def randfloat(lower, upper):
    return (upper-lower) * random() + lower


while True:

    latitude = randfloat(-90, 90)
    longitude = randfloat(-180, 180)

    location = {
        "person_id": args.id,
        "longitude": longitude,
        "latitude": latitude,
        "creation_time": datetime.now().isoformat()
    }

    t1 = time.perf_counter()
    r = httpx.post("http://localhost:30102/locations", json=location)
    t2 = time.perf_counter()

    assert r.status_code == 201
    logger.debug(f"client{args.id:03d} | created {location['creation_time']} | time: {(t2-t1):.06f}")
    sleep(randint(5, 10))

