from sqlalchemy.orm import Session

import models, schemas


def get_location(db: Session, location_id: int):
    return db.query(models.Location).filter(models.Location.id == location_id).first()
