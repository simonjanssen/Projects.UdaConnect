from kafka import KafkaProducer
from time import sleep 
from loguru import logger 

TOPIC_NAME = "locations"
KAFKA_SERVER = "localhost:9092"


while True:
    producer = KafkaProducer(bootstrap_servers=KAFKA_SERVER)
    producer.send(TOPIC_NAME, b"Test Message!")  # messages should be binary
    producer.flush()
    logger.debug("Message sent")
    sleep(3)