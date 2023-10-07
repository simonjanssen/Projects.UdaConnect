
import argparse
from datetime import datetime
import httpx
import math
from time import sleep
from random import randint, random
from loguru import logger
import time

parser = argparse.ArgumentParser()
parser.add_argument("-i", "--id", type=int, required=True)
args = parser.parse_args()

d = 1.0
t = 0.0

while True:

    s = 1 if args.id == 1 else -1
    x = d * math.cos(s * t/(100*math.pi))
    y = d * math.sin(s * t/(100*math.pi))

    location = {
        "person_id": args.id,
        "longitude": x,
        "latitude": y,
        "creation_time": datetime.now().isoformat()
    }

    t1 = time.perf_counter()
    r = httpx.post("http://localhost:8002/locations", json=location)
    t2 = time.perf_counter()

    t += t1

    assert r.status_code == 201
    logger.debug(f"client{args.id:03d} | created {location['creation_time']} | time: {(t2-t1):.06f}")
    sleep(randint(5, 10))

