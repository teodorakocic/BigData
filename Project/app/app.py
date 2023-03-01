import pyspark 
from pyspark.sql import SparkSession
from pyspark.conf import SparkConf
from pyspark import SparkContext
from pyspark.sql.types import StructType, FloatType
from pyspark.sql.functions import *
import sys
import os
from dotenv import load_dotenv
from datetime import datetime
# from geopy.distance import geodesic

# @udf(returnType=FloatType())
# def geodesic_udf(a, b):
#     return geodesic(a, b).m

if __name__ == "__main__":

    load_dotenv()

    START_LOCATION = float(os.getenv('START_LOCATION'))
    END_LOCATION = float(os.getenv('END_LOCATION'))
    TIME_START = int(os.getenv('TIME_START'))
    FILE_DATA = os.getenv('FILE_DATA')
    HDFS_DATA = os.getenv('HDFS_DATA')

    lines = list()

    # spark = SparkSession.builder.master('local[*]').appName('Big Data 1').getOrCreate()
    # tStart = datetime.now()
    spark = SparkSession.builder.appName('Big Data 1').getOrCreate()

    rideSchema = StructType().add('tripduration', 'integer').add('starttime', 'string').add('stoptime', 'string').add('start_station_id', 'integer')\
                        .add('start_station_name', 'string').add('start_station_latitude', 'float').add('start_station_longitude', 'float')\
                        .add('end_station_id', 'integer').add('end_station_name', 'string').add('end_station_latitude', 'float')\
                        .add('end_station_longitude', 'float').add('bikeid', 'integer').add('usertype', 'string')\
                        .add('birthyear', 'string').add('gender', 'integer')

    # dataFrame = spark.read.csv(FILE_DATA, schema=rideSchema)       # For local execution
    dataFrame = spark.read.csv(HDFS_DATA, schema=rideSchema)

    datetimeArg = datetime(2013, 8, 15, 00, TIME_START, 00)

    dataFrame = dataFrame.withColumn('starttimeFormat', to_timestamp(dataFrame.starttime, 'yyyy-MM-dd HH:mm:ss'))
    dataFrame = dataFrame.withColumn('start_location', array(array(dataFrame.start_station_latitude, dataFrame.start_station_longitude)))
    dataFrame = dataFrame.withColumn('end_location', array(array(dataFrame.end_station_latitude, dataFrame.end_station_longitude)))

    # This part for spark-local
    # dataFrame = dataFrame.withColumn('distance', geodesic_udf(col('start_location'), col('end_location')))          
    # dataFrame = dataFrame.withColumn('Vsr', col('distance')/col('tripduration'))
    # dataFrame = dataFrame.withColumn('Vsr', col('Vsr').cast('float'))
    # dataFrame_filtered = dataFrame_filtered.select('start_station_name', 'end_station_name', 'distance', 'tripduration', 'Vsr', 'usertype', 'birthyear', 'gender')
    # dataFrame_filtered_mean_time = dataFrame_filtered.groupBy('birthyear').agg(avg('Vsr').alias('average_Vsr'), mean('tripduration').alias('mean_trip_time')).show(truncate=False)
    # dataFrame_filtered_trip_data = dataFrame_filtered.groupBy('usertype').agg(max('tripduration').alias('max_trip_duration'), min('tripduration').alias('min_trip_duration'), sum('distance').alias('total_distance')).show(truncate=False)

    dataFrame_filtered = dataFrame.filter((dataFrame.start_station_latitude > START_LOCATION) & (dataFrame.end_station_longitude < END_LOCATION) & \
        (dataFrame.starttimeFormat > datetimeArg))

    task1 = 'First 50 rows of filtered data are:'
    print(task1, '\n')
    dataFrame_filtered.show(n=50, truncate=False)

    dataFrame_filtered_location_start_stop = dataFrame_filtered.groupBy('start_station_name', 'end_station_name').agg(stddev('tripduration')\
        .alias('standard_deviation_time_spent_between_stations')).sort(col('standard_deviation_time_spent_between_stations').asc()).collect()
    task2 = 'The lowest standard deviation for the trip duration is for the route ' + str(dataFrame_filtered_location_start_stop[0].asDict()['start_station_name']) \
        + '-' + str(dataFrame_filtered_location_start_stop[0].asDict()['end_station_name']) + '.'
    print(task2, '\n')
    lines.append(task2)
    
    dataFrame_filtered_longer_10_min = dataFrame_filtered.groupBy('usertype').agg(avg('tripduration').alias('average_trip_time')).filter(col('average_trip_time') > 600).collect()
    task3 = str(dataFrame_filtered_longer_10_min[0].asDict()['usertype']) + 's have average trip duration time of ' + \
        str(dataFrame_filtered_longer_10_min[0].asDict()['average_trip_time'] / 60)+ ' minutes, while the same parametes is '\
             + str(dataFrame_filtered_longer_10_min[1].asDict()['average_trip_time'] / 60) + ' minutes for the ' + str(dataFrame_filtered_longer_10_min[1].asDict()['usertype']) + 's.'
    print(task3, '\n')
    lines.append(task3)

    dataFrame_filtered_years = dataFrame_filtered.groupBy('birthyear').agg(count('*').alias('count'), avg('tripduration').alias('avg_riding_time'))\
        .filter(col('birthyear').startswith('199')).sort(col('avg_riding_time').desc()).collect()
    for row in dataFrame_filtered_years:
        task4 = 'Number of riders who are ' + str(2013 - int(row.asDict()['birthyear'])) + ' years old is ' + str(row.asDict()['count']) \
            + ' and average riding time for those riders is ' + str(row.asDict()['avg_riding_time']) + ' seconds.'
        print(task4, '\n')
        lines.append(task4)
    
    dataFrame_filtered_end_location = dataFrame_filtered.groupBy('end_station_name').agg(count('bikeid').alias('count_rides'), mean('tripduration')\
        .alias('mean_trip_time')).filter(col('end_station_name').like('%Avenue%')).sort(col('mean_trip_time').asc()).collect()
    for row in dataFrame_filtered_end_location:
        task5 = 'Number of bike rides that ended on the Avenue \'' + str(row.asDict()['end_station_name']) + '\' is ' + str(row.asDict()['count_rides']) \
            + ' with mean time of ' + str(row.asDict()['mean_trip_time']) + ' seconds.'
        print(task5, '\n')
        lines.append(task5)

    dataFrame_filtered_trip_data = dataFrame_filtered.groupBy('bikeId', 'gender').agg(max('tripduration').alias('max_trip_duration'), min('tripduration')\
        .alias('min_trip_duration'), sum('tripduration').alias('total_time'))\
        .filter(col('gender') == 2).sort(col('max_trip_duration').desc())
    task6 = 'Woman who spent the most time driving, rode a bicycle overall ' + str(dataFrame_filtered_trip_data.collect()[0].asDict()['total_time'] / 3600) + ' hours.'
    print(task6, '\n')
    lines.append(task6)

    with open("app/output.txt", "w") as fileOutput:
        for line in lines:
            fileOutput.write(line)
            fileOutput.write("\n")

    # tEnd = datetime.now()
    # delta = tEnd - tStart

    # print('Spark execution was ' + str(delta) + ' long.')