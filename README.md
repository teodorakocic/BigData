## BigData

Follow the next commands in order to start projects:

***1. Project*** :
  - position yourself in folder [Project](./Project)
  - execute script [start_project1.sh](./Project/scripts/start_project1.sh):
      - *./scripts/start_project1.sh*
  - execute script [execute_namenode.sh](./Project/scripts/execute_namenode.sh)
      - *./scripts/execute_namenode.sh*
  - position yourself in folder [app](./Project/app)
  - building application image:
      - *docker build --rm -t bde/spark-app .*
  - executing application as a container:
      - *docker run --name spark-python --net bde -p 4040:4040 -d bde/spark-app*
      
      
***2. Project -*** **SPARK** :
  - position yourself in folder [Project](./Project)
  - execute script [start_spark.sh](./Project/scripts/start_spark.sh):
      - *./scripts/start_spark.sh*
  - execute script [start_project2.sh](./Project/scripts/start_project2.sh):
      - *./scripts/start_project2.sh*
  - run file [producer_kafka.py](./Project/producer_kafka.py):
      - *python producer_kafka.py*
      
***2. Project -*** **FLINK** :
  - position yourself in folder [FLINK](./Project/FLINK)
  - execute script [start_flink.sh](./Project/scripts/start_flink.sh):
      - *./scripts/start_flink.sh*
  - run file [producer.py](./Project/FLINK/kafka-producer/producer.py):
      - *python kafka-producer/producer.py*
  - submit .jar file generated from [application](./Project/FLINK/flink) on *job-manager*
  
  
***3. Project -*** **TRAINING** :
  - position yourself in folder [Project](./Project)
  - execute script [start_spark.sh](./Project/scripts/start_spark.sh):
      - *./scripts/start_spark.sh*
  - execute script [start_project3a.sh](./Project/scripts/start_project3a.sh):
      - *./scripts/start_project3a.sh*
  - run file [producer_kafka.py](./Project/producer_kafka.py):
      - *python producer_kafka.py*
      
 ***3. Project -*** **CLASSIFICATION** :
  - position yourself in folder [Project](./Project)
  - execute script [start_spark.sh](./Project/scripts/start_spark.sh):
      - *./scripts/start_spark.sh*
  - execute script [start_project3b.sh](./Project/scripts/start_project3b.sh):
      - *./scripts/start_project3a.sh*
  - run file [producer_kafka.py](./Project/producer_kafka.py):
      - *python producer_kafka.py*
