import psycopg2
import json
import time
from datetime import datetime

conn = psycopg2.connect(
    dbname="app",
    user="app",
    password="!ChangeMe!",
    host="database"
)

cur = conn.cursor()

cur.execute("""
    SELECT logs_json, security_type, created_at
    FROM logs
    LIMIT 100
""")

rows = cur.fetchall()

for logs_json, security_type, created_at in rows:
    ip = logs_json.get("ip")
    event = logs_json.get("event")

    print(f"[{created_at}] {ip} {event}")

conn.close()

while True:
    print("Waiting for logs...")
    time.sleep(5)