import argparse
from concurrent import futures
from datetime import datetime
from loguru import logger 
import time

import models
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


def PersonMessage_to_PersonModel(person: definitions_pb2.PersonMessage) -> models.Person:
    return models.Person(
        id = person.id,
        first_name = person.first_name,
        last_name = person.last_name,
        company_name = person.company_name
    )


class PersonServicer(definitions_pb2_grpc.PersonServiceServicer):

    def GetPerson(self, request, context):
        db = SessionLocal()
        try:
            person = db.query(models.Person).filter(models.Person.id == request.id).first()
            if person:
                personMessage = PersonModel_to_PersonMessage(person)
            else:
                personMessage = definitions_pb2.EmptyMessage()
        finally:
            db.close()
        return personMessage

    def GetPersons(self, request, context):
        db = SessionLocal()
        skip, limit = 0, 1000  # todo pass skip, limit as request param
        try:
            persons = db.query(models.Person).offset(skip).limit(limit).all()
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
            db_person = PersonMessage_to_PersonModel(request)
            db.add(db_person)
            db.commit()
            db.refresh(db_person)
        finally:
            db.close()
        return request


class ConnectionServicer(definitions_pb2_grpc.ConnectionServiceServicer):

    def GetConnections(self, request, context):

        logger.debug("Creating dummy PersonMessage object")
        personMessage = definitions_pb2.PersonMessage(
            id = 1,
            first_name = "Thomas",
            last_name = "Mueller",
            company_name = "FC Bayern",
            registration_time = datetime.now().isoformat()
        )

        logger.debug("Creating dummy LocationMessage object")
        locationMessage = definitions_pb2.LocationMessage(
            id = 1,
            person_id = 1,
            longitude = 123.456,
            latitude = 123.456,
            creation_time = datetime.now().isoformat()
        )

        logger.debug("Creating dummy ConnectionMessage object")
        connectionMessage = definitions_pb2.ConnectionMessage(
            person = personMessage,
            location = locationMessage
        )

        logger.debug("Creating dummy ConnectionMessageList object")
        connectionMessageList = definitions_pb2.ConnectionMessageList(
            connections = [connectionMessage]
        )

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
