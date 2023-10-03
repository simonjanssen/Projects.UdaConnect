from contextlib import asynccontextmanager
from fastapi import BackgroundTasks, Depends, FastAPI, status, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.responses import RedirectResponse
import json 
from sqlalchemy.orm import Session
import os

from . import crud, models, schemas
from .database import SessionLocal, engine
models.Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


app = FastAPI(title="PersonAPI")


@app.get("/", include_in_schema=False)
def root():
    return RedirectResponse(url="/docs")


@app.get("/persons", status_code=status.HTTP_200_OK, response_model=list[schemas.Person])
def get_persons(db: Session = Depends(get_db)):
    persons = crud.get_persons(db)
    if persons is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No person found")
    return persons


@app.post("/persons", status_code=status.HTTP_201_CREATED, response_model=schemas.Person)
def create_person(person: schemas.Person, db: Session = Depends(get_db)):
    db_person = crud.get_person_by_id(db, id=person.id)
    if db_person:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="This person already exists!")
    return crud.create_person(db, person=person)


@app.get("/persons/{person_id}", status_code=status.HTTP_200_OK, response_model=schemas.Person)
def get_person(person_id: int, db: Session = Depends(get_db)):
    person = crud.get_person_by_id(db, id=person_id)
    if person is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Person not found")
    return person