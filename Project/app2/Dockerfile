FROM bde2020/spark-python-template:2.4.3-hadoop2.7

ENV SPARK_MASTER spark://spark-master:7077
ENV SPARK_APPLICATION_PYTHON_LOCATION app/consumer_kafka.py
ENV KAFKA_URL kafka-server:9092
ENV KAFKA_TOPIC test
ENV END_STATION Avenue
ENV HDFS_DATA hdfs://namenode:9000
ENV DATASET_LOCATION /data/nyc_bike_rides.csv
ENV CASSANDRA_HOSTNAME cassandra
ENV CASSANDRA_PORT 9042

ADD start.sh /

RUN chmod +x /start.sh

CMD ["/bin/bash", "/start.sh"]