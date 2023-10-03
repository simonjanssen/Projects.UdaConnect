FROM ubuntu:22.04

RUN apt update \
    && apt install --no-install-recommends -y wget ca-certificates default-jre \
    && rm -rf /var/lib/apt/lists/* \
    && apt clean

RUN wget https://dlcdn.apache.org/kafka/3.5.0/kafka_2.13-3.5.0.tgz \
    && tar -xzf kafka_2.13-3.5.0.tgz \
    && rm -f *.tgz

WORKDIR kafka_2.13-3.5.0

RUN KAFKA_CLUSTER_ID="$(bin/kafka-storage.sh random-uuid)" \ 
    && bin/kafka-storage.sh format -t $KAFKA_CLUSTER_ID -c config/kraft/server.properties

EXPOSE 9092 

CMD ["bin/kafka-server-start.sh", "config/kraft/server.properties"]