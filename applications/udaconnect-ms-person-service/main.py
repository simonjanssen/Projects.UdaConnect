import argparse
from concurrent import futures
from datetime import datetime
from loguru import logger 
import time

import models, crud
from database import SessionLocal, engine
models.Base.metadata.create_all(bind=engine)

import grpc
import definitions_pb2
import definitions_pb2_grpc


def PersonModel_to_PersonMessage(person: models.Person) -> definitions_pb2.PersonMessage:
    return definitions_pb2.PersonMessage(
        id = person.id,
        first_name = person.first_name,
        last_name = person.last_name,
        company_name = person.company_name
    )


def LocationModel_to_LocationMessage(location: models.Location) -> definitions_pb2.LocationMessage:
    return definitions_pb2.LocationMessage(
        id = location.id,
        person_id = location.person_id,
        latitude = location.latitude,
        longitude = location.longitude,
        creation_time = location.creation_time.isoformat()
    )


def PersonMessage_to_PersonModel(person: definitions_pb2.PersonMessage) -> models.Person:
    return models.Person(
        id = person.id,
        first_name = person.first_name,
        last_name = person.last_name,
        company_name = person.company_name
    )


def PersonLocationModel_to_ConnectionMessage(person: models.Person, location: models.Location) -> definitions_pb2.ConnectionMessage:
    personMessage = PersonModel_to_PersonMessage(person)
    locationMessage = LocationModel_to_LocationMessage(location)
    return definitions_pb2.ConnectionMessage(
        person=personMessage,
        location=locationMessage
    )


class PersonServicer(definitions_pb2_grpc.PersonServiceServicer):

    def GetPerson(self, request, context):
        db = SessionLocal()
        try:
            person = crud.get_person(db, request.id)
            if person:
                personMessage = PersonModel_to_PersonMessage(person)
            else:
                personMessage = definitions_pb2.EmptyMessage()
        finally:
            db.close()
        return personMessage

    def GetPersons(self, request, context):
        db = SessionLocal()
        try:
            persons = crud.get_persons(db)
            if persons:
                personMessageList = definitions_pb2.PersonMessageList(persons=[PersonModel_to_PersonMessage(person) for person in persons])
            else:
                personMessageList = definitions_pb2.EmptyMessage()
        finally:
            db.close()
        return personMessageList

    def CreatePerson(self, request, context):
        db = SessionLocal()
        try:
            person = PersonMessage_to_PersonModel(request)
            person = crud.create_person(db, person)
        finally:
            db.close()
        return PersonModel_to_PersonMessage(person)


class ConnectionServicer(definitions_pb2_grpc.ConnectionServiceServicer):

    def GetConnections(self, request, context):

        db = SessionLocal()
        try:
            connections = crud.get_connections(db, request.person_id, request.start_date, request.end_date, request.meters)
            connectionMessages = [PersonLocationModel_to_ConnectionMessage(person, location) for (_, person, location) in connections]
            connectionMessageList = definitions_pb2.ConnectionMessageList(connections=connectionMessages)
        finally:
            db.close()
        return connectionMessageList


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--host", type=str, required=True)
    parser.add_argument("--port", type=str, required=True)
    args = parser.parse_args()

    logger.info("Initializing gRPC server")
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=2))
    definitions_pb2_grpc.add_PersonServiceServicer_to_server(PersonServicer(), server)
    definitions_pb2_grpc.add_ConnectionServiceServicer_to_server(ConnectionServicer(), server)

    logger.info(f"Server starting on port {args.port}")
    server.add_insecure_port(f"{args.host}:{args.port}")
    server.start()

    try:
        while True:
            time.sleep(86400)
    except Exception as ex:
        server.stop(0)
