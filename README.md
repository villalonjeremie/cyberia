# 🚨 Anomaly Detection Logs with Isolation Forest (Python + ML)

## Description
This project detects suspicious behaviors (brute force, abnormal traffic)
from web access logs using **Isolation Forest**.

The model is trained on aggregated features per IP and identifies anomalies
without labeled data.

## Features used
- requests_per_minute
- failed_requests
- unique_urls
- avg_response_size
- method_get
- method_post
- is_night

## Tech stack
- PHP
- Symfony
- API Platform
- PostgreSQL
- Python
- Pandas / NumPy
- Scikit-learn
- Isolation Forest

## How to run
```bash
git clone https://github.com/villalonjeremie/cyberia.git
cd cyberia
docker-compose build
go to http://localhost:8000/
