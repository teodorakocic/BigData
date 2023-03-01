from pyspark import SparkContext
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils
import json
import os
from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider

def structured_streaming(hadoop, end_station):
    data = hadoop.map(lambda hdfs:json.loads(hdfs[1]))
    data.cache()

    filtered = data.filter(lambda x: (end_station in x['end station name']))

    if (filtered.isEmpty()):
        print('Not a single ride ended on any of the Avenues!')
    else:
        tripduration_max = filtered.map(lambda x: float(x['tripduration'])).max()
        tripduration_min = filtered.map(lambda x: float(x['tripduration'])).min()
        tripduration_cnt = filtered.map(lambda x: float(x['tripduration'])).count()
        tripduration_std = filtered.map(lambda x: float(x['tripduration'])).stdev()

        job1 = 'Trip duration parameters: max=' + str(tripduration_max) + '\t min=' + str(tripduration_min) + '\t standard deviation=' + str(tripduration_std)\
            + '\t count=' + str(tripduration_cnt)

        print(job1)
        
        cassandra_session.execute(f"""
        INSERT INTO project2_streaming_keyspace.tripduration(time, end_station, max, min, cnt, std)
        VALUES (toTimeStamp(now()), '{end_station}', {tripduration_max}, {tripduration_min}, {tripduration_cnt}, {tripduration_std})
        """)

    popular_streets = data.map(lambda x: (x['end station name'], 1)).reduceByKey(lambda x,y : x+y).sortBy(lambda x: x[1],ascending=False).take(3)
    
    N = len(popular_streets)
    if N==0:
        popular_streets = [('',0),('',0),('',0)]
    elif N==1:
        popular_streets.append(('',0))
        popular_streets.append(('',0))
    elif N==2:
        popular_streets.append(('',0))
    
    print(popular_streets)
    print('-'*100)

    cassandra_session.execute(f"""
        INSERT INTO project2_streaming_keyspace.popular_streets(time, street1, name1, street2, name2, street3, name3)
        VALUES (toTimeStamp(now()), '{popular_streets[0][0]}', {popular_streets[0][1]}, '{popular_streets[1][0]}', {popular_streets[1][1]}, '{popular_streets[2][0]}', {popular_streets[2][1]})
        """)


def build_database(cassandra_session):
    keyspace = 'project2_streaming_keyspace'
    cassandra_session.execute("""
        CREATE KEYSPACE IF NOT EXISTS %s
        WITH replication = { 'class': 'SimpleStrategy', 'replication_factor': '1' }
        """ % keyspace)

    cassandra_session.set_keyspace(keyspace)

    cassandra_session.execute("""
        CREATE TABLE IF NOT EXISTS tripduration (
            time TIMESTAMP,
            end_station text,
            max float,
            min float,
            cnt float,
            std float,
            PRIMARY KEY (time)
        )
        """)
    
    cassandra_session.execute("""
        CREATE TABLE IF NOT EXISTS popular_streets (
            time TIMESTAMP,
            street1 text,
            name1 int,
            street2 text,
            name2 int,
            street3 text,
            name3 int,
            PRIMARY KEY (time)
        )
        """)

if __name__ == '__main__':

    kafka_url = os.getenv('KAFKA_URL')
    topic = os.getenv('KAFKA_TOPIC')
    end_station= os.getenv('END_STATION')
    spark_master = os.getenv('SPARK_MASTER')
    cassandra_host = os.getenv('CASSANDRA_HOSTNAME')
    window_duration = os.getenv('WINDOW_DURATION_IN_SECONDS')

    cassandra_cluster = Cluster([cassandra_host],port=9042)
    cassandra_session = cassandra_cluster.connect()
    build_database(cassandra_session)
    print('Connected to Cassandra!')

    sc = SparkContext(appName='Big Data 2')
    streaming = StreamingContext(sc, int(window_duration))
    
    stream = KafkaUtils.createDirectStream(streaming, [topic], {'metadata.broker.list':kafka_url})
    print('Connected to Kafka!')

    stream.foreachRDD(lambda input: structured_streaming(input, end_station))
    
    streaming.start()
    streaming.awaitTermination()