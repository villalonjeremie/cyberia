#Timestamps réguliers
#Méthodes HTTP variées (GET / POST / éventuellement PUT)
#URLs réalistes
#Codes de statut réalistes (200, 302, 404, 500)
#Taille de réponse cohérente

from datetime import datetime, timedelta
import random
from pathlib import Path

num_lines = 1000
output_file = Path("init_access.log")

ips = [f"192.168.1.{i}" for i in range(1, 101)]

urls = [
    "/index.html",
    "/about.html",
    "/contact.html",
    "/dashboard",
    "/blog",
    "/blog/article-1",
    "/blog/article-2",
    "/blog/article-3",
    "/faq",
    "/static/style.css",
    "/static/script.js",
    "/login",
    "/signup",
]

methods = ["GET", "POST"]

status_codes = [200, 200, 200, 302, 404, 500]  # plus de 200 pour simuler normalité

sizes = list(range(200, 15000))

current_time = datetime(2026, 2, 16, 8, 0, 0)

with output_file.open("w") as f:
    for i in range(num_lines):
        ip = random.choice(ips)
        method = random.choice(methods)
        url = random.choice(urls)
        status = random.choice(status_codes)
        size = random.choice(sizes)
        timestamp = current_time.strftime("%d/%b/%Y:%H:%M:%S +0000")
        
        log_line = f'{ip} - - [{timestamp}] "{method} {url} HTTP/1.1" {status} {size}\n'
        f.write(log_line)
        
        current_time += timedelta(seconds=random.randint(1, 5))

print(f"✅ init_access.log généré avec {num_lines} lignes")
