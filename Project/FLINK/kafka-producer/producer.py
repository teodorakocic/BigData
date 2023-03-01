from confluent_kafka import Producer
import csv
import json
import sys
import time

def receipt(err, msg):
    if err is not None:
        print('Error: {}', format(err))
    else:
        message = 'Produces message on topic {}:{}'.format(msg.topic(), msg.value().decode('utf-8'))
        print(message) 

if __name__ == '__main__':
    producer = Producer({'bootstrap.servers': 'localhost:29092'})
    topic = 'bikenyc'
    print('Kafka Producer has been initiated')

    with open('kafka-producer//nyc_bike_rides.csv') as csvFile:  
        data = csv.DictReader(csvFile)
        for row in data:
            row['tripduration'] = int(row['tripduration'])
            row['start_station_id'] = int(row['start_station_id']) 
            row['start_station_latitude'] = float(row['start_station_latitude'])
            row['start_station_longitude'] = float(row['start_station_longitude'])
            row['end_station_id'] = int(row['end_station_id']) 
            row['end_station_latitude'] = float(row['end_station_latitude'])
            row['end_station_longitude'] = float(row['end_station_longitude'])
            row['bikeid'] = int(row['bikeid'])
            row['birth_year'] = int(row['birth_year']) if row['birth_year'] != "\\N" else -1
            row['gender'] = int(row['gender'])

            producer.produce(topic, key = 'nyc', value = json.dumps(row), callback = receipt)
            producer.flush()
            
            time.sleep(0.1)

    print('Kafka message producer done!')