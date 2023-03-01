## BigData

Follow the next commands in order to start projects:

***1. Project*** :
  - position yourself in folder [Projects](./Projects)
  - execute script [start_project1.sh](./Projects/scripts/start_project1.sh):
      - *./scripts/start_project1.sh*
  - execute script [execute_namenode.sh](./Projects/scripts/execute_namenode.sh)
      - *./scripts/execute_namenode.sh*
  - position yourself in folder [app](./Projects/app)
  - building application image:
      - *docker build --rm -t bde/spark-app .*
  - executing application as a container:
      - *docker run --name spark-python --net bde -p 4040:4040 -d bde/spark-app*
      
      
***2. Project -*** **SPARK** :
  - position yourself in folder [Projects](./Projects)
  - execute script [start_spark.sh](./Projects/scripts/start_spark.sh):
      - *./scripts/start_spark.sh*
  - execute script [start_project2.sh](./Projects/scripts/start_project2.sh):
      - *./scripts/start_project2.sh*
  - run file [producer_kafka.py](./Projects/producer_kafka.py):
      - *python producer_kafka.py*
      
***2. Project -*** **FLINK** :
  - position yourself in folder [FLINK](./Projects/FLINK)
  - execute script [start_flink.sh](./Projects/scripts/start_flink.sh):
      - *./scripts/start_flink.sh*
  - run file [producer.py](./Projects/FLINK/kafka-producer/producer.py):
      - *python kafka-producer/producer.py*
  - submit .jar file generated from [application](./Projects/FLINK/flink) on *job-manager*
  
  
***3. Project -*** **TRAINING** :
  - position yourself in folder [Projects](./Projects)
  - execute script [start_spark.sh](./Projects/scripts/start_spark.sh):
      - *./scripts/start_spark.sh*
  - execute script [start_project3a.sh](./Projects/scripts/start_project3a.sh):
      - *./scripts/start_project3a.sh*
  - run file [producer_kafka.py](./Projects/producer_kafka.py):
      - *python producer_kafka.py*\
      
 ***3. Project -*** **CLASSIFICATION** :
  - position yourself in folder [Projects](./Projects)
  - execute script [start_spark.sh](./Projects/scripts/start_spark.sh):
      - *./scripts/start_spark.sh*
  - execute script [start_project3b.sh](./Projects/scripts/start_project3b.sh):
      - *./scripts/start_project3a.sh*
  - run file [producer_kafka.py](./Projects/producer_kafka.py):
      - *python producer_kafka.py*
