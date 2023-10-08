from sqlalchemy import insert
from sqlalchemy.orm import Session
from typing import List

import models


def create_location(db: Session, location: dict) -> None:
    db.add(models.Location(**location))
    db.commit()
    return

def create_locations(db: Session, locations: List[dict]) -> None:
    db.execute(insert(models.Location), locations)
    db.commit()
    return
