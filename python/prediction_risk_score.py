import joblib
import numpy as np
import json
import pandas as pd
from pathlib import Path
from datetime import datetime, timedelta
import re
from train_isolation_forest import transform_logs_to_feature
from train_isolation_forest import initial_training_model, training_model
from prediction_llm_risk_score import prediction_llm_risk_score
from prediction_isolation_forest_risk_score import prediction_isolation_forest_risk_score

MODEL_PATH = "models/isolation_forest_latest.pkl"
NEW_FEATURES_FILE = "files/new_features.csv"
NEW_INIT_FEATURES_FILE = "files/new_init_features.csv"
ACCESS_LOG = "files/access.log"

def remove_new_features_csv():
    file = Path(NEW_FEATURES_FILE)
    if file.exists():
        file.unlink()
        print(f"{file} removed !")
    else:
        print(f"{file} does not exist.")

    init_file = Path("files/new_init_features.csv")
    if init_file.exists():
        init_file.unlink()
        print(f"{init_file} removed !")
    else:
        print(f"{init_file} does not exist.")

def main():
    transform_logs_to_feature(ACCESS_LOG, False)
    results_llm = prediction_llm_risk_score()
    results_isolation_forest = prediction_isolation_forest_risk_score()
    #remove_new_features_csv()
    return results_isolation_forest

if __name__ == "__main__":
    main()