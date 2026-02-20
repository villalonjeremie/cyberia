import os
import pandas as pd
import requests
from dotenv import load_dotenv

load_dotenv() 
NEW_FEATURES_FILE = "files/new_features.csv"
HF_API_KEY = os.getenv("HUGGINGFACE_API_KEY")
MODEL = "bigscience/bloomz-560m"

df = pd.read_csv(NEW_FEATURES_FILE)

def make_prompt(row):
    return (
        f"Analyse ces metrics de serveur :\n"
        f"Requests per minute: {row['requests_per_minute']}\n"
        f"Failed requests: {row['failed_requests']}\n"
        f"Unique URLs: {row['unique_urls']}\n"
        f"Avg response size: {row['avg_response_size']}\n"
        f"GET method count: {row['method_get']}\n"
        f"POST method count: {row['method_post']}\n"
        f"Is night: {row['is_night']}\n"
        f"Donne un résumé ou des insights."
    )

def call_hf(prompt):
    url = f"https://api-inference.huggingface.co/models/{MODEL}"
    headers = {"Authorization": f"Bearer {HF_API_KEY}"}
    payload = {"inputs": prompt, "parameters": {"max_new_tokens": 150}}
    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()
    result = response.json()
    if isinstance(result, list) and "generated_text" in result[0]:
        return result[0]["generated_text"]
    return str(result)

# 🔹 5️⃣ Boucle sur chaque ligne du CSV
for idx, row in df.iterrows():
    prompt = make_prompt(row)
    output = call_hf(prompt)
    print(f"\n--- Ligne {idx} ---")
    print(output)
