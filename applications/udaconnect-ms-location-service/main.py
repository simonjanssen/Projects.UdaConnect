
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

logger.debug(f"init kafka consumer {KAFKA_SERVER} for {KAFKA_TOPIC}")
consumer = KafkaConsumer(
    KAFKA_TOPIC, 
    bootstrap_servers=[KAFKA_SERVER], 
    group_id = KAFKA_GROUP_ID,
    auto_offset_reset="latest", 
    enable_auto_commit=True,
    value_deserializer=lambda m: json.loads(m.decode('utf-8'))
)

try:
    topics = consumer.topics()
    logger.debug(f"available topics: {topics}")
    
    while True:
        logger.info(f"entering polling loop (cycle time is {CYCLE_TIME}s)")
        logger.debug("polling consumer..")
        topic_partition = consumer.poll(timeout_ms=2000)
        logger.debug("polling done")

        if topic_partition:
            logger.debug("found some new messages")
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
                logger.debug(f"added {len(values)} location entries")
            except Exception as ex:
                logger.error(ex)
            finally:
                db.close()
        else:
            logger.debug("no new messages found")

        sleep(CYCLE_TIME)

except Exception as ex:
    logger.error(ex)

finally:
    consumer.unsubscribe()
    consumer.close()