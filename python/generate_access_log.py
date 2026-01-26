import random
from datetime import datetime, timedelta

# Fichier de sortie
log_file = "access.log"

# Paramètres
start_time = datetime(2026, 1, 26, 12, 0, 0)  # début du log
minutes = 10  # durée totale en minutes
total_lines = 1000  # nombre total de lignes

# Méthodes HTTP possibles
methods = ["GET", "POST", "PUT", "DELETE"]

# URLs fictives
urls = ["/index", "/about", "/contact", "/login", "/api/data", "/products", "/checkout"]

# Codes HTTP possibles
status_codes = [200]*85 + [404]*5 + [500]*10  # majorité 200, quelques erreurs

# Générer les lignes
lines = []

# Calculer lignes par minute
lines_per_minute = total_lines // minutes

for minute in range(minutes):
    # Pic sur la 2e minute (minute = 1)
    if minute == 1:
        n_lines = lines_per_minute * 3  # 3 fois plus de requêtes
    else:
        n_lines = lines_per_minute

    for i in range(n_lines):
        # Random IP
        ip = f"{random.randint(1,255)}.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(0,255)}"
        
        # Random method, URL et status
        method = random.choice(methods)
        url = random.choice(urls)
        status = random.choice(status_codes)
        size = random.randint(200, 5000)  # taille réponse en bytes

        # Timestamp avec secondes aléatoires
        timestamp = start_time + timedelta(minutes=minute, seconds=random.randint(0,59))
        timestamp_str = timestamp.strftime("%d/%b/%Y:%H:%M:%S -0700")  # format Apache

        # Ligne log Apache Combined Format simplifié
        line = f'{ip} - - [{timestamp_str}] "{method} {url} HTTP/1.1" {status} {size}'
        lines.append(line)

# Mélanger les lignes pour simuler un ordre réaliste
random.shuffle(lines)

# Écrire dans le fichier
with open(log_file, "w") as f:
    for line in lines:
        f.write(line + "\n")

print(f"{len(lines)} lignes générées dans {log_file} avec un pic sur la 2ᵉ minute.")
