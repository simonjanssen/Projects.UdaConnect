from sqlalchemy import and_, or_, cast, Date
from sqlalchemy.dialects.postgresql import insert as postgres_upsert
from sqlalchemy.orm import Session
from sqlalchemy.sql import text
from typing import List, Dict
from datetime import datetime, timedelta
import os 
from time import sleep, perf_counter
from loguru import logger
import numpy as np 
from haversine import haversine_vector, Unit

import models
from database import SessionLocal, engine
models.Base.metadata.create_all(bind=engine)

CYCLE_TIME = int(os.getenv("CYCLE_TIME", 60))
assert CYCLE_TIME > 0


while True:

    t1 = perf_counter()

    try:
        locations = {}
        exposures = []
        db = SessionLocal()

        # get all persons
        persons = db.query(models.Person).all()
        person_ids = [person.id for person in persons]
        logger.debug(f"Person ids: {person_ids}")

        # pre-fetch all locations by person id
        today = (datetime.now() - timedelta(seconds=CYCLE_TIME*10)).date()
        for person_id in person_ids:
            locations[person_id] = db.query(models.Location).filter(
                and_(
                    models.Location.person_id == person_id,
                    cast(models.Location.creation_time, Date) == today
                )).order_by(models.Location.creation_time).all()
            
            logger.debug(f"Locations filtered for {person_id}/{today}: {len(locations[person_id])}")
        
        # generate pairs
        person_pairs = []
        for person_a in person_ids:
            for person_b in person_ids:
                if person_a < person_b:
                    person_pairs.append((person_a, person_b))
        logger.debug(f"Exposure pairs: {person_pairs}")

        # calculate distances
        for (person_a, person_b) in person_pairs:

            locations_a = locations[person_a]
            locations_b = locations[person_b]

            if not locations_a or not locations_b:
                continue

            points_a = [(location.latitude, location.longitude) for location in locations_a]
            points_b = [(location.latitude, location.longitude) for location in locations_b]
            distances = haversine_vector(points_b, points_a, Unit.METERS, comb=True)
            min_idx_flattened = np.argmin(distances)
            min_idx = np.unravel_index(min_idx_flattened, distances.shape)
            min_distance = distances[min_idx]
            min_location_a = locations_a[min_idx[0]]
            min_location_b = locations_b[min_idx[1]]

            exposure = {
                "person_a": min_location_a.person_id,
                "person_b": min_location_b.person_id,
                "location_a": min_location_a.id,
                "location_b": min_location_b.id,
                "date_exposed": today.isoformat(),
                "min_distance": min_distance
            }

            logger.debug(exposure)
            exposures.append(exposure)

        if exposures:
            upsert_stmt = postgres_upsert(models.Exposure).values(exposures)
            upsert_stmt = upsert_stmt.on_conflict_do_update(
                index_elements = [models.Exposure.person_a, models.Exposure.person_b, models.Exposure.date_exposed], 
                set_ = dict(
                    location_a = upsert_stmt.excluded.location_a, 
                    location_b = upsert_stmt.excluded.location_b, 
                    min_distance = upsert_stmt.excluded.min_distance ) )
            db.execute(upsert_stmt)
            db.commit()

    finally:
        del locations
        del exposures
        db.close()
    
    t2 = perf_counter()
    logger.info(f"Execution time: {(t2-t1):.06f}s")

    sleep(CYCLE_TIME)