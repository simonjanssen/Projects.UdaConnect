
from kafka import KafkaConsumer

TOPIC_NAME = "locations"


consumer = KafkaConsumer(TOPIC_NAME, auto_offset_reset="earlierst", enable_auto_commit=False)
for message in consumer:
    print(message)