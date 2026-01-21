import csv
import random
from pathlib import Path
from datetime import datetime, timedelta

LINES_PER_DAY = 10_000

FIELDNAMES = [
    "requests_per_minute",
    "failed_requests",
    "unique_urls",
    "avg_response_size",
    "method_get",
    "method_post",
    "is_night"
]

def is_night(hour: int) -> int:
    return 1 if hour < 7 or hour > 22 else 0

def generate_normal_row(hour: int) -> dict:
    night = is_night(hour)
    requests = random.randint(1, 6) if night else random.randint(3, 15)
    failed = random.choices([0, 1], weights=[0.9, 0.1])[0]
    urls = random.randint(1, 5) if night else random.randint(2, 12)
    size = random.randint(400, 1500)
    get = 1
    post = 1 if random.random() < 0.1 else 0

    return {
        "requests_per_minute": requests,
        "failed_requests": failed,
        "unique_urls": urls,
        "avg_response_size": size,
        "method_get": get,
        "method_post": post,
        "is_night": night
    }

def main():
    now = datetime.now()
    timestamp = now.strftime("%Y%m%d_%H%M%S")
    logs_dir = Path("daily_logs")
    logs_dir.mkdir(parents=True, exist_ok=True)

    output_file = logs_dir / f"features_{timestamp}.csv"

    with open(output_file, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        writer.writeheader()

        for i in range(LINES_PER_DAY):
            hour = (now + timedelta(minutes=i)).hour
            row = generate_normal_row(hour)
            writer.writerow(row)

    print(f"{LINES_PER_DAY} lignes normales générées dans {output_file}")

if __name__ == "__main__":
    main()
