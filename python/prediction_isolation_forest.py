import joblib
import numpy as np
import pandas as pd

MODEL_PATH = "model/isolation_forest.pkl"
NEW_FEATURES_FILE = "new_features.csv"

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
    X_scaled = scaler.transform(X)

    scores = model.decision_function(X_scaled)
    preds = model.predict(X_scaled)

    results = []
    for i, row in df.iterrows():
        results.append({
            **row.to_dict(),
            "anomaly_score": float(scores[i]),
            "prediction": int(preds[i]),
            "risk": "HIGH" if preds[i] == -1 else "LOW"
        })
    print(f"{results} : Results")

    return results

def main(): 
    prediction_risk_score()

if __name__ == "__main__":
    main()