# 🚀 Delta Writing with Kafka & RisingWave  

This project demonstrates a **real-time delta writing architecture**, where change events continuously update the latest dataset state using:

| Component | Role |
|----------|------|
| ✅ Python Producer | Publishes insert/update/delete events to Kafka |
| ✅ Apache Kafka | Event streaming backbone |
| ✅ RisingWave | Streaming SQL database computing the latest state |

---

## ✅ Result

RisingWave continuously merges delta changes to maintain a **correct and up-to-date state** of all records — including deletes ✅

---

## 🏗 Architecture & Workflow

```
Python Producer
        ↓
Kafka Topic: user-events
        ↓
RisingWave SOURCE (stream)
        ↓
Materialized View:
    latest_user_state
```

✔ Full change event history retained  
✔ Final snapshot always accurate  
✔ Deletes handled correctly

---

## 🔧 Requirements

| Software | Usage |
|---------|------|
| Docker + Docker Compose | Run Kafka + RisingWave |
| Python 3.10+ | Execute producer script |
| kafka-python | Kafka client library |
| psql CLI | Execute SQL scripts |

---

## ▶️ Setup & Execution Guide

### ✅ 1️⃣ Start Streaming Environment

```sh
docker-compose up -d
```

Verify services:

```sh
docker ps
```

---

### ✅ 2️⃣ Initialize RisingWave Source + Materialized View

```sh
psql -h localhost -p 4566 -U root -f init.sql
```

Creates:
- Kafka connector
- `user_events` source
- `latest_user_state` materialized view ✔

---

### ✅ 3️⃣ Run Event Producer

```sh
python producer.py
```

Random change events are streamed every second ✅

---

### ✅ 4️⃣ Query RisingWave

View event log:

```sql
SELECT * FROM user_events ORDER BY event_order DESC LIMIT 20;
```

View final latest merged record state:

```sql
SELECT * FROM latest_user_state ORDER BY id;
```

---

## 📂 Project Structure

| File | Description |
|------|-------------|
| `init.sql` | RisingWave Kafka source + delta view |
| `producer.py` | Random CRUD-like delta change stream |
| `docker-compose.yml` | Infrastructure for Kafka + RisingWave |

---

## 🛠 Debugging Notes

| Issue | Cause | Resolution |
|------|------|------------|
| `docker` not recognized | Missing PATH | Reinstall Docker Desktop |
| `psql` command not found | PATH not configured | Added PostgreSQL `bin` path |
| Kafka container failed | Missing Zookeeper env | Updated `docker-compose.yml` |
| `NoBrokersAvailable` | Broker not ready | Verified `localhost:9092` running |

✅ All setup issues resolved!

---

## 🚀 Future Enhancements

| Feature | Benefit |
|--------|---------|
| Debezium CDC | Real-world DB change capture |
| Iceberg / S3 Sink | Analytics + historical persistence |
| Real dashboards | Visual business insights |
| Schema Registry | Event format guarantees |

---

## ✅ Conclusion

This solution achieves:

✅ Real-time ingestion  
✅ Delta merge computing latest state  
✅ Durable event history  
✅ Robust for production use cases  
