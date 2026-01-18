import pandas as pd
import joblib
from sklearn.ensemble import IsolationForest
from pathlib import Path
import numpy as np
from sklearn.preprocessing import StandardScaler

# =========================
# CONFIG
# =========================
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

CONTAMINATION = 0.01   # % estimé d'anomalies
N_ESTIMATORS = 200
RANDOM_STATE = 42

# =========================
# LOAD DATA
# =========================
def load_features(path: str) -> np.ndarray:
    df = pd.read_csv(path)

    if df.isnull().any().any():
        raise ValueError("Données contenant des valeurs NULL")

    X = df[FEATURE_COLUMNS].to_numpy()
    return X

def train_model(X: np.ndarray) -> IsolationForest:
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    model = IsolationForest(
        n_estimators=N_ESTIMATORS,
        contamination=CONTAMINATION,
        random_state=RANDOM_STATE,
        n_jobs=-1
    )

    model.fit(X_scaled)

    print("Sauvegarde du modèle...")
    Path(MODEL_PATH).parent.mkdir(parents=True, exist_ok=True)
    bundle = {
        "model": model,
        "scaler": scaler,
        "features": FEATURE_COLUMNS
    }

    joblib.dump(bundle, MODEL_PATH)
    print(f"Modèle sauvegardé dans {MODEL_PATH}")

    return model

def save_model(model, path: str):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    bundle = {
    "model": model,
    "scaler": scaler,
    "features": FEATURE_COLUMNS
}
    joblib.dump(bundle, path)
    print(f"✅ Modèle sauvegardé dans {path}")

def main():
    print("🔄 Chargement des features...")
    X = load_features(FEATURES_FILE)

    print(f"{X} X en df puis numpy")
    print(f"{len(X)} lignes chargées")

    print("Entraînement du modèle...")
    model = train_model(X)

    #print("Sauvegarde du modèle...")
    #save_model(model, MODEL_PATH)

if __name__ == "__main__":
    main()
