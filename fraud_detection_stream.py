
from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col
from pyspark.sql.types import *
from delta import *
import joblib, pandas as pd

spark = (SparkSession.builder
         .appName("FraudStream")
         .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension")
         .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog")
         .getOrCreate())

schema = StructType([
    StructField("txn_id", StringType()),
    StructField("ts_utc", StringType()),
    StructField("merchant", StringType()),
    StructField("amount", DoubleType()),
    StructField("card_id", StringType())
])

df = (spark.readStream
          .format("kafka")
          .option("kafka.bootstrap.servers", "localhost:9092")
          .option("subscribe", "transactions")
          .load()
          .selectExpr("CAST(value AS STRING) as json"))

parsed = df.select(from_json(col("json"), schema).alias("data")).select("data.*")

model = joblib.load("models/anomaly_model.pkl")

from pyspark.sql.functions import pandas_udf
@pandas_udf("boolean")
def is_fraud(amount: pd.Series) -> pd.Series:
    return pd.Series(model.predict(amount.values.reshape(-1,1)) == -1)

scored = parsed.withColumn("flag_fraud", is_fraud(col("amount")))

(scored.writeStream
       .format("delta")
       .outputMode("append")
       .option("checkpointLocation", "./chk")
       .start("./delta_fraud_output"))

spark.streams.awaitAnyTermination()
