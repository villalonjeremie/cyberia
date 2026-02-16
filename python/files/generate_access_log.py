import random
from datetime import datetime, timedelta

log_file = "access.log"
start_time = datetime(2026, 1, 26, 12, 0, 0)
minutes = 10
total_lines = 1000
methods = ["GET", "POST", "PUT", "DELETE"]
urls = ["/index", "/about", "/contact", "/login", "/api/data", "/products", "/checkout"]
status_codes = [200]*100
lines = []
lines_per_minute = total_lines // minutes

for minute in range(minutes):
    if minute == 1:
        n_lines = lines_per_minute * 3
    else:
        n_lines = lines_per_minute

    for i in range(n_lines):
        ip = f"{random.randint(1,255)}.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(0,255)}"
        method = random.choice(methods)
        url = random.choice(urls)
        status = random.choice(status_codes)
        size = random.randint(200, 5000)
        timestamp = start_time + timedelta(minutes=minute, seconds=random.randint(0,59))
        timestamp_str = timestamp.strftime("%d/%b/%Y:%H:%M:%S -0700")
        line = f'{ip} - - [{timestamp_str}] "{method} {url} HTTP/1.1" {status} {size}'
        lines.append(line)

random.shuffle(lines)

with open(log_file, "w") as f:
    for line in lines:
        f.write(line + "\n")

print(f"{len(lines)} lignes générées dans {log_file} avec un pic sur la 2ᵉ minute.")
