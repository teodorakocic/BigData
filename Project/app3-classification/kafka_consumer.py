from pyspark import SparkContext
from pyspark.sql import SparkSession
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils
from pyspark.sql.types import *
import json
from pyspark.ml.classification import DecisionTreeClassificationModel
from pyspark.ml import Pipeline, PipelineModel
from pyspark.ml.feature import VectorIndexer, VectorAssembler, StringIndexer
from pyspark.sql.types import FloatType
import pyspark.sql.functions as F
from pyspark.ml.evaluation import BinaryClassificationEvaluator
import os
from influxdb import InfluxDBClient
from datetime import datetime

dbhost = os.getenv('INFLUXDB_HOST', '127.0.0.1')
dbport = int(os.getenv('INFLUXDB_PORT'))
dbuser = os.getenv('INFLUXDB_USERNAME')
dbpassword = os.getenv('INFLUXDB_PASSWORD')
dbname = os.getenv('INFLUXDB_DATABASE')
topic = os.getenv('KAFKA_TOPIC')

def influxDBconnect():
    return InfluxDBClient(dbhost, dbport, dbuser, dbpassword, dbname)

def influxDBwrite(count, accuracy, topic, data):
    timestamp = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
    measurementData = [
        {
            "measurement": topic,
            "time": timestamp,
            "fields": {
                "start station latitude": data[0],
                "start station longitude": data[1],
                "end station latitude": data[2],
                "end station longitude": data[3],
                "trip duration": data[4],
                "predictions": count,
                "accuracy": accuracy
            }
        }
    ]
    print(measurementData)
    influxDBConnection.write_points(measurementData, time_precision='ms')

def structured_streaming(hadoop, model):
    data = hadoop.map(lambda x:json.loads(x[1]))
    data.cache()

    forBucket = list()

    if(data.isEmpty()):
        print('No data available')
        return
    else:
        sample = data.toDF().count() // 2
        forBucket.append(float(data.toDF().collect()[sample][3]))
        forBucket.append(float(data.toDF().collect()[sample][4]))
        forBucket.append(float(data.toDF().collect()[sample][8]))
        forBucket.append(float(data.toDF().collect()[sample][9]))
        forBucket.append(int(data.toDF().collect()[sample][13]))

    dataFrame = data.toDF()
    
    columns = ['start station latitude', 'start station longitude']

    for column in columns:
        dataFrame = dataFrame.withColumn(column, F.col(column).cast(FloatType()))

    vectorAssembler = VectorAssembler().setInputCols(columns).setOutputCol('features').setHandleInvalid('skip')

    assembled = vectorAssembler.transform(dataFrame)
    
    stringIndexer = StringIndexer().setInputCol('usertype').setOutputCol('label')
    indexedDataFrame = stringIndexer.fit(assembled).transform(assembled)

    prediction = model.transform(indexedDataFrame)

    prediction.select('prediction', 'label')

    predictionsMade = prediction.count()

    correctNumber = float(prediction.filter(prediction['label'] == prediction['prediction']).count())

    influxDBwrite(predictionsMade, correctNumber, topic, forBucket)


if __name__ == '__main__':

    HDFS_DATA = os.getenv('HDFS_URL')
    MODEL = os.getenv('MODEL_LOCATION')
    kafka_url = os.getenv('KAFKA_URL')
    window_duration = os.getenv('WINDOW_DURATION_IN_SECONDS')

    influxDBConnection = influxDBconnect()

    spark = SparkSession.builder.appName('Big Data 3 - Classification').getOrCreate()
    
    sc = spark.sparkContext
    streaming = StreamingContext(sc, int(window_duration))

    model = PipelineModel.load(HDFS_DATA + MODEL)

    stream = KafkaUtils.createDirectStream(streaming,[topic], {'metadata.broker.list':kafka_url})
    result = stream.foreachRDD(lambda input: structured_streaming(input, model))

    streaming.start()
    streaming.awaitTermination()