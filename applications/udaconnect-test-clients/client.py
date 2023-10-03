
import argparse
from datetime import datetime
import httpx
from time import sleep
from random import randint, random
from loguru import logger
import time

parser = argparse.ArgumentParser()
parser.add_argument("-i", "--id", type=int, required=True)
args = parser.parse_args()

while True:
    location = {
        "person_id": args.id,
        "longitude": "123.456",
        "latitude": "123.456",
        "creation_time": datetime.now().isoformat()
    }

    t1 = time.perf_counter()
    r = httpx.post("http://localhost:8080/locations", json=location)
    t2 = time.perf_counter()

    assert r.status_code == 201
    logger.debug(f"client{args.id:03d} | created {location['creation_time']} | time: {(t2-t1):.06f}")
    sleep(random())

