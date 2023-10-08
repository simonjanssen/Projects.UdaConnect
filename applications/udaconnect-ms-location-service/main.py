
from kafka import KafkaConsumer
from time import sleep 
from loguru import logger 
import json 
import os
from sqlalchemy.orm import Session

import models, crud
from database import SessionLocal, engine
models.Base.metadata.create_all(bind=engine)

KAFKA_TOPIC = os.getenv("KAFKA_TOPIC")
KAFKA_SERVER = os.getenv("KAFKA_SERVER")
KAFKA_GROUP_ID = os.getenv("KAFKA_GROUP_ID")
CYCLE_TIME = int(os.getenv("CYCLE_TIME", 60))

consumer = KafkaConsumer(
    KAFKA_TOPIC, 
    bootstrap_servers=[KAFKA_SERVER], 
    group_id = KAFKA_GROUP_ID,
    auto_offset_reset="latest", 
    enable_auto_commit=True,
    value_deserializer=lambda m: json.loads(m.decode('utf-8'))
)

try:
    while True:
        logger.info("Entering polling cycle")
        topic_partition = consumer.poll()
        
        if topic_partition:
            values = []
            for tp, records in topic_partition.items():
                for r, record in enumerate(records):
                    topic = tp.topic
                    partition = tp.partition
                    offset = record.offset
                    key = record.key
                    value = record.value
                    values.append(value)
                    logger.debug(f"{(r+1):03d}/{len(records):03d} Topic: {topic}, Partition: {partition}, Offset: {offset}, Key: {key}, Value: {value}")
            
            try:
                db = SessionLocal()
                crud.create_locations(db, values)
                logger.debug(f"Added {len(values)} location entries")
            finally:
                db.close()

        sleep(CYCLE_TIME)

finally:
    consumer.unsubscribe()
    consumer.close()