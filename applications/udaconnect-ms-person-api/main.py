from contextlib import asynccontextmanager
from fastapi import FastAPI, status, HTTPException
from fastapi.responses import RedirectResponse
from loguru import logger 
import os 

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


app = FastAPI(title="PersonAPI", lifespan=lifespan)


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
    pb_request = definitions_pb2.PersonIdMessage(id=person.id)
    pb_response = await stubs["persons"].GetPerson(pb_request)
    response = MessageToDict(pb_response, preserving_proto_field_name=True)
    if response:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="This person already exists!")
    pb_request = definitions_pb2.PersonMessage(**dict(person))
    pb_response = await stubs["persons"].CreatePerson(pb_request)
    response = MessageToDict(pb_response, preserving_proto_field_name=True)
    return response


@app.get("/persons/{person_id}", status_code=status.HTTP_200_OK, response_model=schemas.Person)
async def get_person(person_id: int):
    pb_request = definitions_pb2.PersonIdMessage(id=person_id)
    pb_response = await stubs["persons"].GetPerson(pb_request)
    response = MessageToDict(pb_response, preserving_proto_field_name=True)
    if not response:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Person not found")
    return response


@app.get("/persons/{person_id}/connection", status_code=status.HTTP_200_OK, response_model=list[schemas.Connection])
async def get_connection(person_id: int):
    pb_request = definitions_pb2.PersonIdMessage(id=person_id)
    pb_response = await stubs["connections"].GetConnections(pb_request)
    response = MessageToDict(pb_response, preserving_proto_field_name=True)["connections"]
    return response