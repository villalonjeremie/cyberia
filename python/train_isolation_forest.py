import pandas as pd
import joblib
from sklearn.ensemble import IsolationForest
from pathlib import Path
import shutil
import re
import numpy as np
from sklearn.preprocessing import StandardScaler
from datetime import datetime, timedelta

FEATURES_FILE = "features.csv"
INITIAL_FILE_CSV = "initial_feature_to_train.csv"
MODEL_PATH = "model/isolation_forest.pkl"
FEATURE_COLUMNS = [
    "requests_per_minute",
    "failed_requests",
    "unique_urls",
    "avg_response_size",
    "method_get",
    "method_post",
    "is_night"
]

CONTAMINATION = 0.01
N_ESTIMATORS = 200
RANDOM_STATE = 42

def load_features(path: str) -> np.ndarray:
    df = pd.read_csv(path)

    if df.isnull().any().any():
        raise ValueError("Données contenant des valeurs NULL")

    X = df[FEATURE_COLUMNS].to_numpy()
    return X

def train_save_model(X: np.ndarray) -> IsolationForest:
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    model = IsolationForest(
        n_estimators=N_ESTIMATORS,
        contamination=CONTAMINATION,
        random_state=RANDOM_STATE,
        n_jobs=-1
    )

    model.fit(X_scaled)

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")

    models_dir = Path("models")
    models_dir.mkdir(exist_ok=True)

    version_path = models_dir / f"isolation_forest_{timestamp}.pkl"
    latest_path = models_dir / "isolation_forest_latest.pkl"

    bundle = {
        "model": model,
        "scaler": scaler,
        "features": FEATURE_COLUMNS,
        "trained_at": timestamp,
        "n_samples": len(X)
    }

    joblib.dump(bundle, version_path)
    joblib.dump(bundle, latest_path)

    print(f"✅ Modèle versionné : {version_path}")
    print(f"🔄 Modèle latest mis à jour")

    return model

def initial_training_model():
    print(f"\n Entraînement initial")
    file_init_access_path = Path("files/init_access.log")

    if not file_init_access_path.exists():
        print("❌ Aucun fichier init_acces_log dans le repertoir file")
        return

    transform_logs_to_feature("files/init_access.log", True)
    X = load_features("files/new_init_features.csv")
    print(f"{X} X en df puis numpy")
    print(f"{len(X)} lignes chargées")
    print("Entraînement du modèle...")
    train_save_model(X)
    print("Modèle entrainé...")

def training_model():
    logs_dir = Path("files/features_to_train")
    logs_dir.mkdir(exist_ok=True)
    csv_files = list(logs_dir.glob("*.csv"))

    if not csv_files:
        print("❌ Aucun fichier à entraîner")
        return

    dfs = [pd.read_csv(file) for file in csv_files]
    merged = pd.concat(dfs, ignore_index=True)
    merged.to_csv("files/merged_features.csv", index=False)

    X = load_features("files/merged_features.csv")
    print(f"{X} X en df puis numpy")
    print(f"{len(X)} lignes chargées")
    print("Entraînement du modèle...")
    train_save_model(X)
    print("Modèle entrainé...")

    merged_file = Path("files/merged_features.csv")
    if merged_file.exists():
        merged_file.unlink()
        print("Fichier merged_features.csv supprimé")

def transform_logs_to_feature(access_log: str, is_initial: bool):
    log_pattern = re.compile(
        r'(?P<ip>\S+) \S+ \S+ \[(?P<date>.+?)\] "(?P<method>\S+) (?P<url>\S+) \S+" (?P<status>\d{3}) (?P<size>\S+)'
    )

    rows = []
    with open(access_log) as f:
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

    minute_index = df["timestamp"].dt.floor("min")
    df_metrics = pd.DataFrame({
        "requests_per_minute": df.groupby(minute_index)["url"].count(),
        "failed_requests": df[df["status"] >= 400].groupby(minute_index)["status"].count(),
        "unique_urls": df.groupby(minute_index)["url"].nunique(),
        "avg_response_size": df.groupby(minute_index)["size"].mean(),
        "method_get": df[df["method"] == "GET"].groupby(minute_index)["method"].count(),
        "method_post": df[df["method"] == "POST"].groupby(minute_index)["method"].count(),
        "is_night": df.groupby(minute_index)["is_night"].max()
    }).fillna(0).reset_index(drop=True)

    df_metrics = df_metrics[FEATURE_COLUMNS]
    output_file = "files/new_init_features.csv" if is_initial else "files/new_features.csv"
    df_metrics.to_csv(output_file, index=False)
    print(f"{output_file} créé avec succès !")

def main():
    training_model()
    
if __name__ == "__main__":
    main()
