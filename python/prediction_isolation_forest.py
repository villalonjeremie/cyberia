import joblib
import numpy as np
import json
import pandas as pd
from pathlib import Path
from datetime import datetime, timedelta
import re


MODEL_PATH = "models/isolation_forest_latest.pkl"
NEW_FEATURES_FILE = "new_features.csv"
ACCESS_LOG = "access.log"

def prediction_risk_score() -> list[dict]:
    bundle = joblib.load(MODEL_PATH)
    print(f"{bundle} : Results")

    model = bundle["model"]
    scaler = bundle["scaler"]
    features = bundle["features"]

    df = pd.read_csv(NEW_FEATURES_FILE)
    
    missing = set(features) - set(df.columns)
    if missing:
        raise ValueError(f"Colonnes manquantes : {missing}")

    X = df[features].to_numpy()

    print(f"{X} X en df puis numpy")
    print(f"{len(X)} lignes chargées")

    X_scaled = scaler.transform(X)
    print(f"{X_scaled} X apres transform")

    scores = model.decision_function(X_scaled)
    print(f"{scores} : scores")
    preds = model.predict(X_scaled)
    print(f"{preds} : preds")

    normal_data = df[preds == 1].copy()

    features_dir = Path("features_to_train")
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
    path_features = features_dir / f"feature_to_train_{timestamp}.csv";
    normal_data.to_csv(path_features, index=False)
    print(f"CSV clean sauvegardé dans {path_features} avec {len(normal_data)} lignes (sans anomalies)")

    results = []
    for i, row in df.iterrows():
        if preds[i] == -1:
            results.append({
                **row.to_dict(),
                "anomaly_score": float(scores[i]),
                "prediction": int(preds[i]),
                "risk": "HIGH"
            })
    print(f"{results} : Results")

    return results

def transform_logs_to_feature():
    log_pattern = re.compile(
        r'(?P<ip>\S+) \S+ \S+ \[(?P<date>.+?)\] "(?P<method>\S+) (?P<url>\S+) \S+" (?P<status>\d{3}) (?P<size>\S+)'
    )

    rows = []

    with open(ACCESS_LOG) as f:
        for line in f:
            m = log_pattern.match(line)
            if m:
                data = m.groupdict()
                size = int(data['size']) if data['size'].isdigit() else 0
                dt = datetime.strptime(data['date'].split()[0], "%d/%b/%Y:%H:%M:%S")
                rows.append({
                    "timestamp": dt,
                    "method": data["method"],
                    "url": data["url"],
                    "status": int(data["status"]),
                    "size": size,
                    "is_night": 22 <= dt.hour or dt.hour < 6
                })

    df = pd.DataFrame(rows)

    df_metrics = pd.DataFrame({
        "requests_per_minute": df.groupby(df["timestamp"].dt.floor("min"))["url"].count(),
        "failed_requests": df[df["status"] >= 400].groupby(df["timestamp"].dt.floor("min"))["status"].count(),
        "unique_urls": df.groupby(df["timestamp"].dt.floor("min"))["url"].nunique(),
        "avg_response_size": df.groupby(df["timestamp"].dt.floor("min"))["size"].mean(),
        "method_get": df[df["method"] == "GET"].groupby(df["timestamp"].dt.floor("min"))["method"].count(),
        "method_post": df[df["method"] == "POST"].groupby(df["timestamp"].dt.floor("min"))["method"].count(),
        "is_night": df.groupby(df["timestamp"].dt.floor("min"))["is_night"].max()  # True si au moins une requête nuit
    }).fillna(0).reset_index()

    df_metrics.to_csv("new_features.csv", index=False)
    print("new_features.csv créé avec succès !")

def remove_new_features_csv():
    file_path = Path("new_features.csv")
    if file_path.exists():
        file_path.unlink()
        print(f"{file_path} supprimé avec succès !")
    else:
        print(f"{file_path} n'existe pas.")

def main():
    transform_logs_to_feature()
    results = prediction_risk_score()
    print(json.dumps(results))
    return results
    #remove_new_features_csv()

if __name__ == "__main__":
    main()