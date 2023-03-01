docker exec -it namenode hdfs dfs -test -e /big-data
if [ $? -eq 1 ]
then
  echo "[INFO]: Creating /data folder on HDFS"
  docker exec -it namenode hdfs dfs -mkdir /data
fi

docker exec -it namenode hdfs dfs -test -e /data/nyc_bike_rides.csv
if [ $? -eq 1 ]
then
  echo "[INFO]: Adding csv file in the /big-data folder on the HDFS"
  docker exec -it namenode hdfs dfs -put /data/nyc_bike_rides.csv /data/nyc_bike_rides.csv
fi

data/nyc_bike_rides.csv