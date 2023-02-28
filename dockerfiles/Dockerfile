FROM puckel/docker-airflow
# from jupyter/pyspark-notebook
# user root

RUN pip install requests
RUN pip install pandas
RUN pip install requests
RUN pip install cassandra-driver
# user jovyan
# RUN pip install com.datastax.spark:spark-cassandra-connector_2.11:2.4.2



COPY --from=openjdk:8-jre-slim /usr/local/openjdk-8 /usr/local/openjdk-8

ENV JAVA_HOME /usr/local/openjdk-8

USER root
# RUN pip install pyspark==2.3.1  
RUN pip install pyspark==3.3.1
# --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.0.1,com.datastax.spark:spark-cassandra-connector_2.12:3.0.0 

RUN update-alternatives --install /usr/bin/java java /usr/local/openjdk-8/bin/java 1


RUN apt-get update && \
	apt-get install -y wget


RUN 	mkdir spark-libs && \
	cd spark-libs && \
	wget https://repo1.maven.org/maven2/com/datastax/spark/spark-cassandra-connector_2.11/2.3.2/spark-cassandra-connector_2.11-2.3.2.jar -P spark-libs 
    # apt-get install spark-cassandra-connector_2.11-2.3.2.jar
	# com.datastax.spark:spark-cassandra-connector_2.12:3.0.0





# ENV PATH=$PATH:$SPARK_HOME/bin/
# ENV PYSPARK_PYTHON python


# CMD PYSPARK_PYTHON=python3 $SPARK_HOME/bin/spark-submit --packages com.datastax.spark:spark-cassandra-connector_2.12:3.0.0
# RUN 	mkdir spark-libs && \
# 	wget https://repo1.maven.org/maven2/com/datastax/spark/spark-cassandra-connector_2.11/2.3.2/spark-cassandra-connector_2.11-2.3.2.jar -P spark-libs && \
# 	mv spark-libs/*.jar usr/local/spark/jars && \
# 	rm -rf spark-libs && \
#   	cd usr/local/spark/jars

# ENV SPARK_HOME=spark-libs 



# RUN apt-get update && \
#     apt-get install com.datastax.spark:spark-cassandra-connector_2.11:2.4.2 && \
#     apt-get autoremove -yqq --purge && \
#     apt-get clean


# COPY spark-cassandra-connector_2.12-2.5.1.jar /usr/local/spark/spark-cassandra-connector_2.12-2.5.1.jar
# 
# ENV SPARK_HOME /usr/local/spark

# ARG JAR_FILE=target/*.jar
# COPY ${JAR_FILE} spark-cassandra-connector_2.12-2.5.1.jar
# ENTRYPOINT ["java","-jar","/spark-cassandra-connector_2.12-2.5.1.jar"]
# CMD /wait && /*.jar

# ADD ./spark-cassandra-connector_2.12-2.5.1.jar spark-cassandra-connector_2.12-2.5.1.jar 

# ENTRYPOINT ["java","-jar","/spark-cassandra-connector_2.12-2.5.1.jar"]



