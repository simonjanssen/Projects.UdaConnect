from contextlib import asynccontextmanager
from fastapi import BackgroundTasks, Depends, FastAPI, status, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.responses import RedirectResponse
import json 
from kafka import KafkaProducer
from sqlalchemy.orm import Session
import os

import crud, models, schemas
from database import SessionLocal, engine
models.Base.metadata.create_all(bind=engine)

KAFKA_SERVER = os.getenv("KAFKA_SERVER")
KAFKA_TOPIC = os.getenv("KAFKA_TOPIC")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

producers = {}


@asynccontextmanager
async def lifespan(app: FastAPI):
    # https://fastapi.tiangolo.com/advanced/events/
    producers["locations"] = KafkaProducer(bootstrap_servers=KAFKA_SERVER, value_serializer=lambda v: json.dumps(v).encode('utf-8'))
    yield
    producers["locations"].close()


def send_to_kafka(topic: str, location: schemas.LocationIngest):
    message_json = jsonable_encoder(location)
    producers["locations"].send(topic, message_json)
    producers["locations"].flush()


app = FastAPI(title="LocationAPI", lifespan=lifespan)


@app.get("/", include_in_schema=False)
def root():
    return RedirectResponse(url="/docs")


@app.post("/locations", status_code=status.HTTP_201_CREATED, response_model=schemas.LocationIngest)
async def post_location(location: schemas.LocationIngest, background_tasks: BackgroundTasks):
    background_tasks.add_task(send_to_kafka, KAFKA_TOPIC, location)
    return location


@app.get("/locations/{location_id}", status_code=status.HTTP_200_OK, response_model=schemas.LocationRetrieve)
def get_location(location_id: int, db: Session = Depends(get_db)):
    location = crud.get_location(db, location_id=location_id)
    if location is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Location not found")
    return location