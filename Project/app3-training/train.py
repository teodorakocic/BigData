from pyspark.sql import SparkSession
from pyspark import SparkContext
from pyspark.ml.classification import LogisticRegression, DecisionTreeClassifier, NaiveBayes
from pyspark.ml import Pipeline, PipelineModel
from pyspark.ml.feature import VectorIndexer, VectorAssembler, StringIndexer
from pyspark.sql.types import FloatType
import pyspark.sql.functions as F
from pyspark.ml.evaluation import BinaryClassificationEvaluator
import os


if __name__ == '__main__':
    
    spark = SparkSession.builder.appName('Big Data 3 - Training').getOrCreate()
    spark.sparkContext.setLogLevel("ERROR")

    HDFS_DATA = os.getenv('HDFS_URL')
    DATASET = os.getenv('DATASET_LOCATION')
    MODEL = os.getenv('MODEL_LOCATION')

    dataFrame = spark.read.csv(HDFS_DATA + DATASET, header=True)

    columns = ['start station latitude', 'start station longitude']

    for column in columns:
        dataFrame = dataFrame.withColumn(column, F.col(column).cast(FloatType()))

    vectorAssembler = VectorAssembler().setInputCols(columns).setOutputCol('features').setHandleInvalid('skip')

    assembled = vectorAssembler.transform(dataFrame)
    
    stringIndexer = StringIndexer().setInputCol('usertype').setOutputCol('label')
    indexedDataFrame = stringIndexer.fit(assembled).transform(assembled)

    train_split, test_split = indexedDataFrame.randomSplit([0.8, 0.2], seed=1337)

    regressionModel = LogisticRegression(maxIter=100, regParam=0.02, elasticNetParam=0.8)

    pipeline = Pipeline(stages=[regressionModel])
    regressionModelPipe = pipeline.fit(train_split)

    prediction = regressionModelPipe.transform(test_split)

    evaluator = BinaryClassificationEvaluator(labelCol='label', rawPredictionCol='prediction', metricName='areaUnderROC')
    accuracy = evaluator.evaluate(prediction)

    print('Accuracy\'s value for logistic regression model is ' + str(accuracy) + '!')

    regressionModelPipe.write().overwrite().save(HDFS_DATA + MODEL)