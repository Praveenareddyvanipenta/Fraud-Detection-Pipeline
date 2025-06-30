
from kafka import KafkaProducer
import json, subprocess

producer = KafkaProducer(
    bootstrap_servers="localhost:9092",
    value_serializer=lambda v: json.dumps(v).encode()
)

# Stream generator output
proc = subprocess.Popen(["python", "-u", "data_simulator/generate_transactions.py"], stdout=subprocess.PIPE)

for line in proc.stdout:
    if line:
        producer.send("transactions", value=json.loads(line))
        producer.flush()
