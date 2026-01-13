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
        raise ValueError("❌ Données contenant des valeurs NULL")

    X = df[FEATURE_COLUMNS].to_numpy()
    return X

# =========================
# TRAIN MODEL
# =========================
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
    return model


# =========================
# SAVE MODEL
# =========================
def save_model(model, path: str):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, path)
    print(f"✅ Modèle sauvegardé dans {path}")


# =========================
# MAIN
# =========================
def main():
    print("🔄 Chargement des features...")
    X = load_features(FEATURES_FILE)



    print(f"{X} 1er debug")



    print(f"📊 {len(X)} lignes chargées")

    print("🤖 Entraînement du modèle...")
    model = train_model(X)
    print(f"{model} 2e debug")

    print("💾 Sauvegarde du modèle...")
    save_model(model, MODEL_PATH)

    # Test rapide
    scores = model.decision_function(X)
    print(f"{scores} 3e debug")
    print(f"{model.predict(X)} 4e debug")

    anomalies = (model.predict(X) == -1).sum()

    print(f"🚨 Anomalies détectées dans le train set : {anomalies}")
    print(f"📉 Score moyen : {scores.mean():.4f}")


if __name__ == "__main__":
    main()
