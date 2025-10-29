# 🚀 Delta Writing with Kafka & RisingWave  
### Real-Time Streaming State Management

This project demonstrates a **real-time delta writing architecture**, where change events continuously update the latest dataset state using:

| Component | Role |
|----------|------|
| ✅ Python Producer | Publishes insert/update/delete events to Kafka |
| ✅ Apache Kafka | Event streaming backbone |
| ✅ RisingWave | Streaming SQL database maintaining the latest state |

---

## ✅ Result

RisingWave continuously merges all delta changes to maintain a **correct and up-to-date** state — including deletes ✔

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

| Software | Version | Usage |
|---------|---------|------|
| Docker + Docker Compose | Latest | Run Kafka & RisingWave |
| Python | 3.10+ | Kafka event producer |
| Kafka Client Library | kafka-python | Send messages to Kafka |
| PostgreSQL CLI | psql | Setup SQL pipelines |

---

## 🧰 Tools Installation Guide

### ✅ Install Docker & Docker Compose

#### Windows / Mac  
Download Docker Desktop from docker.com

#### Linux (Ubuntu Example)

```sh
sudo apt update
sudo apt install docker.io docker-compose -y
sudo systemctl enable --now docker
```

Verify:

```sh
docker --version
docker-compose --version
```

---

### ✅ Install PostgreSQL CLI

Ubuntu:

```sh
sudo apt install postgresql-client -y
```

Mac:

```sh
brew install libpq
brew link --force libpq
```

Verify:

```sh
psql --version
```

---

### ✅ Install Python Dependencies

```sh
pip install kafka-python
```

---

## ▶️ Setup & Execution Guide

### ✅ 1️⃣ Start Streaming Environment

```sh
docker-compose up -d
```

Check containers:

```sh
docker ps
```

---

### ✅ 2️⃣ Initialize RisingWave SQL

```sh
psql -h localhost -p 4566 -U root -f init.sql
```

---

### ✅ 3️⃣ Run Delta Change Producer

```sh
python producer.py
```

---

### ✅ 4️⃣ Query RisingWave

Event log:
```sql
SELECT * FROM user_events ORDER BY event_order DESC LIMIT 20;
```

Latest state:
```sql
SELECT * FROM latest_user_state ORDER BY id;
```

---

## 📂 Project Structure

| File | Purpose |
|------|---------|
| `docker-compose.yml` | Runs Kafka & RisingWave |
| `init.sql` | Creates streaming tables/views |
| `producer.py` | Generates streaming CRUD events |

---

## 🛠 Troubleshooting & Fixes

| Issue | Fix |
|------|-----|
| `psql not recognized` | Add PostgreSQL bin folder to PATH |
| Kafka connection failed | Restart docker-compose |
| Permission denied | Run PowerShell as Admin |

---

## 🚀 Future Enhancements

- Debezium CDC streaming
- S3/Iceberg historical warehouse
- Real-time dashboards

---

## ✅ Conclusion

✔ Real-time ingestion  
✔ Delta merge correctness  
✔ Production-ready streaming foundation  
