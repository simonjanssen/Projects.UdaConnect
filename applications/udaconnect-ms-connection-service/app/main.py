from concurrent import futures
from datetime import datetime
from loguru import logger 
import time

import grpc
import definitions_pb2
import definitions_pb2_grpc


class ConnectionServicer(definitions_pb2_grpc.ConnectionServiceServicer):

    def Get(self, request, context):

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
    

logger.info("Initializing gRPC server")
server = grpc.server(futures.ThreadPoolExecutor(max_workers=2))
definitions_pb2_grpc.add_ConnectionServiceServicer_to_server(ConnectionServicer(), server)

logger.info("Server starting on port 5005")
server.add_insecure_port("[::]:5005")
server.start()

try:
    while True:
        time.sleep(86400)
except Exception as ex:
    server.stop(0)
