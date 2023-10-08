
from datetime import datetime, date
from sqlalchemy import and_, or_, cast, Date
from sqlalchemy.orm import Session
from typing import List, Tuple

import models


def get_person(db: Session, person_id: int) -> models.Person:
    return db.query(models.Person).filter(models.Person.id == person_id).first()


def get_persons(db: Session, skip: int = 0, limit: int = 1000) -> List[models.Person]:
    return db.query(models.Person).offset(skip).limit(limit).all()


def create_person(db: Session, person: models.Person) -> models.Person:
    db.add(person)
    db.commit()
    db.refresh(person)
    return person


def get_connections(db: Session, person_id: int, start_date: date, end_date: date, meters: float) -> List[Tuple[models.Exposure, models.Person, models.Location]]:
    results = db.query(models.Exposure, models.Person, models.Location).filter(
        and_(
            or_(
                and_(models.Exposure.person_a == person_id, models.Exposure.person_b == models.Person.id, models.Exposure.location_a == models.Location.id),
                and_(models.Exposure.person_b == person_id, models.Exposure.person_a == models.Person.id, models.Exposure.location_b == models.Location.id)),
            models.Exposure.date_exposed >= cast(start_date, Date),
            models.Exposure.date_exposed <= cast(end_date, Date),
            models.Exposure.min_distance < meters,
            
        )).all()
    
    return results