from sqlalchemy.orm import Session

from . import models, schemas


def get_persons(db: Session, skip: int = 0, limit: int = 1000):
    return db.query(models.Person).offset(skip).limit(limit).all()


def get_person_by_id(db: Session, id: int):
    return db.query(models.Person).filter(models.Person.id == id).first() 


def create_person(db: Session, person: schemas.Person):
    db_person = models.Person(id=person.id, first_name=person.first_name, last_name=person.last_name, company_name=person.company_name)
    db.add(db_person)
    db.commit()
    db.refresh(db_person)
    return db_person

