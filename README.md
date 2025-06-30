
# Real-Time Fraud Detection Pipeline (Databricks / PySpark)

This personal project demonstrates how to build a real‑time fraud‑detection pipeline using open‑source
streaming components and Delta Lake.

**Tech stack**
- Apache Kafka (local via Docker Compose)
- PySpark 3.5 + Delta Lake 3.2
- scikit‑learn (Isolation Forest anomaly model)
- Databricks (optional deployment target)

## Architecture
1. **Data simulator** generates synthetic card‑transaction JSON.
2. **Kafka producer** streams JSON to a `transactions` topic.
3. **Spark Structured Streaming job** consumes the topic, scores each record with a pre‑trained model, and
   writes flagged transactions to a Delta table.
4. (Optional) Upload the Spark script to Databricks and write Delta output to S3.

## Quick start

```bash
# clone and create env
git clone https://github.com/<your-user>/fraud-detection-databricks.git
cd fraud-detection-databricks
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt

# start Kafka & Zookeeper
docker compose up -d

# in new terminal – generate + send transactions
python kafka_producer/send_transactions.py

# in another terminal – start Spark stream
spark-submit --packages io.delta:delta-spark_2.12:3.2.0 spark_job/fraud_detection_stream.py
```

## Folder overview
```
data_simulator/          # synthetic JSON generator
kafka_producer/          # sends JSON to Kafka topic
spark_job/               # PySpark Structured Streaming job
models/                  # trained anomaly model (.pkl)
requirements.txt         # pip deps
docker-compose.yml       # Confluent Kafka stack
```

## License
MIT
