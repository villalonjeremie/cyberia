import pandas as pd
import joblib
from sklearn.ensemble import IsolationForest
from pathlib import Path
import shutil
import numpy as np
from sklearn.preprocessing import StandardScaler
from datetime import datetime, timedelta

FEATURES_FILE = "features.csv"
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

def main():
    logs_dir = Path("features_to_train")
    trained_dir = Path("features_trained")
    trained_dir.mkdir(exist_ok=True)
    csv_files = list(logs_dir.glob("*.csv"))

    if not csv_files:
        print("❌ Aucun fichier à entraîner")
        return

    for csv_file in csv_files:
        print(f"\n Entraînement avec {csv_file.name}")
        output_file = logs_dir / csv_file.name
        X = load_features(output_file)
        print(f"{X} X en df puis numpy")
        print(f"{len(X)} lignes chargées")
        print("Entraînement du modèle...")
        train_save_model(X)
        new_csv_name = csv_file.name.replace("feature_to_train", "features_trained", 1)
        dest = trained_dir / new_csv_name
        shutil.move(csv_file, dest)
        print(f" Déplacé vers {dest}")

if __name__ == "__main__":
    main()
