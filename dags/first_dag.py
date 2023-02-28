try:

    from datetime import timedelta
    from airflow import DAG
    from airflow.operators.python_operator import PythonOperator
    from datetime import datetime
    import requests
    import json
    from pyspark.sql import SparkSession
    import pyspark.sql.functions as F
    
    from pyspark.sql.types import StructType,StructField, StringType, IntegerType
    from pyspark.sql.functions import *
    from pyspark.sql.types import *
    import os
    from pyspark.sql import DataFrame
    import time
    import logging
    
    # import org.apache.spark.sql.cassandra._
    
    # from datetime import datetime

    print("All Dag modules are ok ......")

except Exception as e:
    print("Error  {} ".format(e))


def first_function():
    print("Hello world this works ")
    # # url = 'https://api.cricapi.com/v1/currentMatches?apikey=8990f916-8107-4f70-9e8e-dcbd9639b687&offset=0'

    # # download  = requests.get(url).text
    # # json_data = json.loads(download)
    # # return json_data
    # spark = SparkSession.builder.appName('SparkByExamples.com').getOrCreate()

    
    # data2 = [("James","","Smith","36636","M",3000),
    # ("Michael","Rose","","40288","M",4000),
    # ("Robert","","Williams","42114","M",4000),
    # ("Maria","Anne","Jones","39192","F",4000),
    # ("Jen","Mary","Brown","","F",-1)
    # ]

    # schema = StructType([ \
    #     StructField("firstname",StringType(),True), \
    #     StructField("middlename",StringType(),True), \
    #     StructField("lastname",StringType(),True), \
    #     StructField("id", StringType(), True), \
    #     StructField("gender", StringType(), True), \
    #     StructField("salary", IntegerType(), True) \
    # ])
    
    # df = spark.createDataFrame(data=data2,schema=schema)
    # df.printSchema()
    # df.show(truncate=False)


def json_api_data_import():
    url = 'https://api.cricapi.com/v1/currentMatches?apikey=8990f916-8107-4f70-9e8e-dcbd9639b687&offset=0'

    download  = requests.get(url)
    
    data = download.json()['data']
    
    data2 = json.dumps(data)
    
    records = json.loads(data2)
    
    file = open('./ip_files/imported_json_data.json','a')


    json.dump(records,file,indent=6)
    file.close()
    
def writeToCassandrafunc():
    spark = (SparkSession.builder
                 .config("spark.cassandra.connection.host","cassandra")
                 .config("spark.cassandra.auth.username","cassandra")
                 .config("spark.cassandra.auth.password","cassandra")
                 .config("com.datastax.spark.connector.datasource.CassandraCatalog")
                #  .config("spark.sql.catalog.myCatalog", "com.datastax.spark.connector.datasource.CassandraCatalog")
                 .appName("demo").getOrCreate()
                 )
    # spark.conf.set(f"spark.sql.catalog.myCatalog", "com.datastax.spark.connector.datasource.CassandraCatalog")

    # spark.sql(f"use cricket")
    # dept = [(10,"Finance"),(20,"Marketing"),(30,"Sales"),(40,"IT") ,(50,"HR")]
    # dept = [(11,"Finance"),(22,"Marketing"),(33,"Sales"),(44,"IT") ,(55,"HR")]
    # deptColumns = ["dept_id","dept_name"]
    

    # df = spark.createDataFrame(data=dept, schema = deptColumns)
    
    df = spark.read.json('./ip_files/imported_json_data.json',multiLine=True)
    df = df.drop('teamInfo').drop('score')
    df = df.withColumnRenamed('date','date_')



    df = df.select('date_','hasSquad','id','matchEnded','matchStarted','matchType','name','series_id','status','venue')
    
    df.show(truncate  = False)
    
    # df.rdd.saveToCassandra("cricket", "cricket_data3")
    

    
    
    
    #create spark session with cassandar configuration
    # sparkSesison = (SparkSession.builder
    #     .config("spark.cassandra.connection.host","cassandra")
    #     .config("spark.cassandra.auth.username","cassandra")
    #     .config("spark.cassandra.auth.password","cassandra")
    #     .appName("demo").getOrCreate()
    # )


    # write data to cassandra database
    try:
        print('writing part is skipped')
        # (df.write.format("org.apache.spark.sql.cassandra").mode('append').options(table='cricket_data', keyspace='cricket').save())
        # df.write \
        # .format("org.apache.spark.sql.cassandra") \
        # .options(table="cricket_data", keyspace="cricket") \
        # .mode("append") \
        # .save()
        
    except Exception :
        print("exception occured")

    df_cassandra = (spark.read
        .format("org.apache.spark.sql.cassandra")
        .options(table="cricket_data",keyspace="cricket")
        .load())  

    df_cassandra.show(truncate  = False)
    #Print the schema 
    df.printSchema()
    
    
    

with DAG(dag_id="first_dag",
         schedule_interval="@daily",
         default_args={
             "owner": "airflow",
             "start_date": datetime(2023, 1, 27),
             "retries": 1,
             "retry_delay": timedelta(minutes=1)
         },
         catchup=False) as dag:

    first_function = PythonOperator(
        task_id="first_function",
        python_callable=first_function
    )
    json_api_data_import = PythonOperator(
        task_id="json_api_data_import",
        python_callable=json_api_data_import
    )
    writeToCassandrafunc = PythonOperator(
        task_id="writeToCassandrafunc",
        python_callable=writeToCassandrafunc
    )


first_function >> json_api_data_import >> writeToCassandrafunc





















# ====================================Notes====================================

# all_success           -> triggers when all tasks arecomplete
# one_success           -> trigger when one task is complete
# all_done              -> Trigger when all Tasks are Done
# all_failed            -> Trigger when all task Failed
# one_failed            -> one task is failed
# none_failed           -> No Task Failed

# ==============================================================================



# ============================== Executor====================================

# There are Three main  types of executor
# -> Sequential Executor  run single task in linear fashion wih no parllelism default Dev
# -> Local Exector  run each task in seperate process
# -> Celery Executor Run each worker node within multi node architecture Most scalable

# ===========================================================================