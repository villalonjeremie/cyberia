import joblib
import numpy as np
import json
import pandas as pd
from pathlib import Path
from datetime import datetime, timedelta
import re
from train_isolation_forest import transform_logs_to_feature
from train_isolation_forest import initial_training_model, training_model

MODEL_PATH = "models/isolation_forest_latest.pkl"
NEW_FEATURES_FILE = "files/new_features.csv"
ACCESS_LOG = "files/access.log"

def prediction_risk_score() -> list[dict]:
    file_path = Path(MODEL_PATH)
    if not file_path.exists():
        initial_training_model()

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

    features_dir = Path("files/features_to_train")
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
    path_features = features_dir / f"feature_to_train_{timestamp}.csv"
    normal_data.to_csv(path_features, index=False)
    print(f"CSV cleaned and saved in {path_features} with {len(normal_data)} lines (without errors")

    training_model()
    print("Model trained")

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

def remove_new_features_csv():
    file_path = Path("files/new_features.csv")
    if file_path.exists():
        file_path.unlink()
        print(f"{file_path} supprimé avec succès !")
    else:
        print(f"{file_path} n'existe pas.")

def main():
    transform_logs_to_feature("files/access.log", False)
    results = prediction_risk_score()
    print(json.dumps(results))
    remove_new_features_csv()
    return results

if __name__ == "__main__":
    main()