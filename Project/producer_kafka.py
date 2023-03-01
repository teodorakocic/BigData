from kafka import KafkaProducer
import csv
import json
import time


msgProducer = KafkaProducer(bootstrap_servers=['localhost:50023'], value_serializer = lambda x: x.encode('utf-8'))

with open('data//nyc_bike_rides.csv') as csvFile:  
    data = csv.DictReader(csvFile)
    for row in data:
        msgProducer.send('test', json.dumps(row))
        msgProducer.flush()

        print('Message sent with body: ' + json.dumps(row))
        time.sleep(0.1)

print('Kafka message producer done!')

