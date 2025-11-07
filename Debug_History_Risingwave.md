
# 🧩 Debug History — RisingWave + Kafka + Event Hubs Setup

This file documents **all technical issues encountered and their fixes**, without long explanations.

---

## 1️⃣ CNTLM / Bosch Proxy Setup (Python HTTPS_PROXY Issue)

**Error:**
```
HTTPSConnectionPool(host='pypi.org', port=443): Max retries exceeded
```
**Fix:**
```python
os.environ["HTTPS_PROXY"] = "http://127.0.0.1:3128"
os.environ["HTTP_PROXY"] = "http://127.0.0.1:3128"
```

---

## 2️⃣ Docker PATH Not Found

**Error:**
```
docker : The term 'docker' is not recognized as the name of a cmdlet
```
**Fix:**
Add Docker Desktop path to system PATH.
```
C:\Program Files\Docker\Docker
esourcesin
```
Restart PowerShell.

---

## 3️⃣ PostgreSQL `psql` Command Not Recognized

**Error:**
```
psql : The term 'psql' is not recognized
```
**Fix:**
Add PostgreSQL to PATH:
```
setx PATH "$env:PATH;C:\Program Files\PostgreSQL\18\bin"

```

---

## 4️⃣ WSL Memory Allocation (RisingWave low memory)

**Error (in container logs):**
```
total_memory: 2.87 GiB (too low)
```
**Fix (.wslconfig):**
```
[wsl2]
memory=16GB
processors=4
swap=8GB
localhostForwarding=true
```

---

## 5️⃣ Kafka Container Restarting

**Error:**
```
KAFKA_ZOOKEEPER_CONNECT is required
```
**Fix:** Added correct `KAFKA_ZOOKEEPER_CONNECT` in docker-compose.yml:
```yaml
KAFKA_ZOOKEEPER_CONNECT: zookeeper:2181
```

---

## 6️⃣ RisingWave SQL — Source Creation Error

**Error:**
```
function tumble(timestamp with time zone, interval) does not exist
```
**Fix:** Simplified query, removed unsupported TUMBLE window for timestamp with timezone.

---

## 7️⃣ RisingWave SQL — JSON Format Parsing Error

**Error:**
```
expected CANAL | PROTOBUF | DEBEZIUM | MAXWELL | PLAIN | NATIVE | NONE after FORMAT
```
**Fix:**
Changed from:
```
FORMAT JSON;
```
to:
```
FORMAT PLAIN ENCODE JSON;
```

---

## 8️⃣ RisingWave SQL — Timestamp Default Error

**Error:**
```
Unsupported function: cast(timestamp with time zone) -> timestamp without time zone
```
**Fix:** Removed `DEFAULT NOW()` from `ts` definition.

---

## 9️⃣ RisingWave Session Error

**Error:**
```
Failed to start a new session - database "root" does not exist
```
**Fix:**
Used `-d dev` in psql connection:
```
psql -h localhost -p 4566 -U root -d dev
```

---

## 🔟 Producer `NoBrokersAvailable`

**Error:**
```
kafka.errors.NoBrokersAvailable: NoBrokersAvailable
```
**Fixes:**
- Confirmed Kafka running: `docker ps`
- Verified mapped port `29092` for host access.
- Updated producer bootstrap:
```python
BOOTSTRAP = "localhost:29092"
```

---

## 11️⃣ RisingWave Meta Error

**Error:**
```
BrokerTransportFailure (Local: Broker transport failure)
```
**Fix:**
Updated `init.sql` with correct Kafka broker address:
```sql
properties.bootstrap.server = 'localhost:29092'
```

---

## 12️⃣ PowerShell SQL Execution Error

**Error:**
```
Select-Object : A positional parameter cannot be found that accepts argument 'FROM'
```
**Fix:**
Executed SQL *inside psql* instead of PowerShell:
```
psql -h localhost -p 4566 -U root -d dev
```
Then ran:
```sql
SELECT * FROM latest_user_state ORDER BY id;
```

---

## 13️⃣ Azure Event Hubs (Port 9093) Connection Failure

**Error:**
```
TcpTestSucceeded : False
```
**Fix:**
Allowed public IP in Event Hub → Networking → Firewall and Virtual Networks.
Then verified with:
```
Test-NetConnection Risingwave.servicebus.windows.net -Port 9093
```

---

## 14️⃣ Kafka Producer — Event Hubs SASL Connection

**Error:**
```
NoBrokersAvailable (Event Hubs)
```
**Fix:**
Added SASL_SSL + PLAIN config in producer:
```python
security_protocol="SASL_SSL",
sasl_mechanism="PLAIN",
sasl_plain_username="$ConnectionString",
sasl_plain_password="Endpoint=sb://Risingwave.servicebus.windows.net/;SharedAccessKeyName=RootManageSharedAccessKey;SharedAccessKey=<key>"
```

---

## 15️⃣ CNTLM Proxy Setup Validation

**Error:**
Requests blocked on corporate network.
**Fix:**
Validated CNTLM working via:
```
curl -v https://www.google.com --proxy http://127.0.0.1:3128
```
Confirmed success.

---

## ✅ Final System Working
✅ Docker containers running: Zookeeper, Kafka, RisingWave  
✅ Producer successfully sending data to Kafka  
✅ RisingWave reading source + updating materialized view  
✅ All data visible in `latest_user_state`  

---

📅 **Last Verified:** November 2025
