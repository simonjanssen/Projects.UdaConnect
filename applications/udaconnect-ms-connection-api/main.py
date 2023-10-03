

from contextlib import asynccontextmanager
from fastapi import BackgroundTasks, Depends, FastAPI, status, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.responses import RedirectResponse

import schemas 

import grpc
import definitions_pb2
import definitions_pb2_grpc
from google.protobuf.json_format import MessageToDict


stubs = {}

@asynccontextmanager
async def lifespan(app: FastAPI):
    channel = grpc.aio.insecure_channel("localhost:5005")
    stubs["connections"] = definitions_pb2_grpc.ConnectionServiceStub(channel)
    yield
    await channel.close()


app = FastAPI(title="ConnectionAPI", lifespan=lifespan)


@app.get("/", include_in_schema=False)
def root():
    return RedirectResponse(url="/docs")


@app.get("/persons/{person_id}/connection", status_code=status.HTTP_200_OK, response_model=list[schemas.Connection])
async def get_connection(person_id: int):
    pb_request = definitions_pb2.PersonIdMessage(id=person_id)
    pb_response = await stubs["connections"].Get(pb_request)
    response = MessageToDict(pb_response, preserving_proto_field_name=True)["connections"]
    return response