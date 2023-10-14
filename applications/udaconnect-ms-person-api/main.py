from contextlib import asynccontextmanager
from datetime import date
from fastapi import FastAPI, status, HTTPException, Path, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from loguru import logger 
import os 
from typing import Annotated

import schemas 

import grpc
import definitions_pb2
import definitions_pb2_grpc
from google.protobuf.json_format import MessageToDict


gRPC_HOST = os.getenv("gRPC_HOST")
gRPC_PORT = os.getenv("gRPC_PORT")


stubs = {}

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.debug(f"Setting up channel for {gRPC_HOST}:{gRPC_PORT}..")
    channel = grpc.aio.insecure_channel(f"{gRPC_HOST}:{gRPC_PORT}")
    #await channel.channel_ready()
    stubs["persons"] = definitions_pb2_grpc.PersonServiceStub(channel)
    stubs["connections"] = definitions_pb2_grpc.ConnectionServiceStub(channel)
    yield
    await channel.close()


origins = [
    "http://localhost:30101",
]

app = FastAPI(title="PersonAPI", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", include_in_schema=False)
def root():
    return RedirectResponse(url="/docs")


@app.get("/persons", status_code=status.HTTP_200_OK, response_model=list[schemas.Person])
async def get_persons():
    pb_request = definitions_pb2.EmptyMessage()
    pb_response = await stubs["persons"].GetPersons(pb_request)
    response = MessageToDict(pb_response, preserving_proto_field_name=True)
    if not response:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Nobody there")
    return response["persons"]


@app.post("/persons", status_code=status.HTTP_201_CREATED, response_model=schemas.Person)
async def create_person(person: schemas.Person):
    pb_request = definitions_pb2.PersonRequestMessage(id=person.id)
    pb_response = await stubs["persons"].GetPerson(pb_request)
    response = MessageToDict(pb_response, preserving_proto_field_name=True)
    if response:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="This person already exists!")
    pb_request = definitions_pb2.PersonMessage(**dict(person))
    pb_response = await stubs["persons"].CreatePerson(pb_request)
    response = MessageToDict(pb_response, preserving_proto_field_name=True)
    return response


@app.get("/persons/{person_id}", status_code=status.HTTP_200_OK, response_model=schemas.Person)
async def get_person(person_id: Annotated[int, Path(description="person identifier", example=1)]):
    pb_request = definitions_pb2.PersonRequestMessage(id=person_id)
    pb_response = await stubs["persons"].GetPerson(pb_request)
    response = MessageToDict(pb_response, preserving_proto_field_name=True)
    if not response:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Person not found")
    return response


@app.get("/persons/{person_id}/connection", status_code=status.HTTP_200_OK, response_model=list[schemas.Connection])
async def get_connection(
    person_id: Annotated[int, Path(description="person identifier", example=1)], 
    start_date: Annotated[date, Query(description="lower bound of date range", example="2023-10-01")], 
    end_date: Annotated[date, Query(description="upper bound of date range", example="2023-11-01")], 
    distance: Annotated[float, Query(description="proximity to a given user in meters", example=5.0)] = 5.0
):
    pb_request = definitions_pb2.ConnectionRequestMessage(
        person_id = person_id,
        start_date = start_date.isoformat(),
        end_date = end_date.isoformat(),
        meters = distance
    )
    pb_response = await stubs["connections"].GetConnections(pb_request)
    response = MessageToDict(pb_response, preserving_proto_field_name=True)
    if not response:
        return []
    else:
        return response["connections"]