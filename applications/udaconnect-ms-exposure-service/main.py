
from sqlalchemy.orm import Session
from sqlalchemy.sql import text
from typing import List, Dict
from datetime import datetime, timedelta

from . import models, crud, schemas
from .database import SessionLocal, engine
models.Base.metadata.create_all(bind=engine)

# handover by request
start_date = datetime.now().isoformat()
end_date = datetime.now().isoformat()
person_id = 1
meters = 5.0

try:
    db = SessionLocal()
    locations: List = db.query(models.Location).filter(models.Location.person_id == person_id).filter(models.Location.creation_time < end_date).filter(models.Location.creation_time >= start_date).all()
    persons: List = db.query(models.Person).all()
    person_map: Dict[str, models.Person] = {person.id: person for person in persons}

    data = []
    for location in locations:
        data.append(
            {
                "person_id": person_id,
                "longitude": location.longitude,
                "latitude": location.latitude,
                "meters": meters,
                "start_date": start_date.strftime("%Y-%m-%d"),
                "end_date": (end_date + timedelta(days=1)).strftime("%Y-%m-%d"),
            }
        )

    

    query = text(
        """
        SELECT  person_id, id, ST_X(coordinate), ST_Y(coordinate), creation_time
        FROM    location
        WHERE   ST_DWithin(coordinate::geography,ST_SetSRID(ST_MakePoint(:latitude,:longitude),4326)::geography, :meters)
        AND     person_id != :person_id
        AND     TO_DATE(:start_date, 'YYYY-MM-DD') <= creation_time
        AND     TO_DATE(:end_date, 'YYYY-MM-DD') > creation_time;
        """
    )

    result: List[models.Connection] = []
    for line in tuple(data):
        for (exposed_person_id, location_id, exposed_lat, exposed_long, exposed_time,) in db.engine.execute(query, **line):
            location = models.Location(id=location_id, person_id=exposed_person_id, creation_time=exposed_time)
            location.set_wkt_with_coords(exposed_lat, exposed_long)
            result.append(models.Connection(person=person_map[exposed_person_id], location=location))

finally:
    db.close()