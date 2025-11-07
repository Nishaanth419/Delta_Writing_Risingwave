# producer.py
import json
import time
import random
from datetime import datetime, timezone
from kafka import KafkaProducer

MODE = "host"  
BOOTSTRAP = "localhost:29092" if MODE == "host" else "kafka:9092"
TOPIC = "user-events"


producer = KafkaProducer(
    bootstrap_servers=BOOTSTRAP,
    value_serializer=lambda v: json.dumps(v).encode("utf-8"),
    retries=5,
    linger_ms=5
)

users = [
    {"id": 1, "name": "Alice", "age": 25},
    {"id": 2, "name": "Bob", "age": 30},
    {"id": 3, "name": "Charlie", "age": 36},
]


event_order = 1
print(f"📡 Sending events to Kafka topic '{TOPIC}' via {BOOTSTRAP}...\n")

try:
    while True:
        user = random.choice(users)
        op = random.choice(["insert", "update", "delete"])

        event = {
            "id": user["id"],
            "name": user["name"] if op != "delete" else None,
            "age": user["age"] + random.randint(-2, 2) if op == "update" else user["age"],
            "op": op,
            "event_order": event_order,
            "ts": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
        }

        producer.send(TOPIC, value=event)
        print(f"✅ Sent: {event}")

        event_order += 1
        time.sleep(1)

except KeyboardInterrupt:
    print("\n🛑 Stopped by user.")

except Exception as e:
    print(f"❌ Send error: {e}")

finally:
    producer.flush()
    producer.close()
    print("🚀 All messages sent and producer closed.")
