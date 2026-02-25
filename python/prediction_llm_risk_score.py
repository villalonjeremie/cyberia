import os
import pandas as pd
import requests
import json
from dotenv import load_dotenv
from huggingface_hub import InferenceClient

load_dotenv()
HF_API_KEY = os.getenv("HUGGINGFACE_API_KEY")
MODEL = "meta-llama/Llama-3-8B-Instruct"
NEW_FEATURES_FILE = "files/new_features.csv"

def call_hf(prompt):
    client = InferenceClient(token=HF_API_KEY)
    response = client.text_generation(
        model="tiiuae/falcon-7b-instruct",
        prompt=prompt,
        max_new_tokens=500,
        temperature=0.7
    )

    response.raise_for_status()
    result = response.json()
    
    if isinstance(result, list) and "generated_text" in result[0]:
        return result[0]["generated_text"]
    return str(result)

def make_global_prompt(df):
    """
    Build a prompt to detect anomalies in server logs.
    """
    prompt = "You are an expert in server log analysis.\n"
    prompt += "Here are server log entries. Identify all anomalies.\n\n"
    
    for idx, row in df.iterrows():
        prompt += (
            f"Line {idx}:\n"
            f"- Requests per minute: {row['requests_per_minute']}\n"
            f"- Failed requests: {row['failed_requests']}\n"
            f"- Unique URLs: {row['unique_urls']}\n"
            f"- Avg response size: {row['avg_response_size']}\n"
            f"- GET count: {row['method_get']}\n"
            f"- POST count: {row['method_post']}\n"
            f"- Is night: {row['is_night']}\n\n"
        )
    
    prompt += (
        "Analyze all lines and return only the anomalies.\n"
        "For each anomaly, provide:\n"
        "1) The corresponding line number\n"
        "2) Anomaly score (0-1)\n"
        "3) Risk level (LOW/MEDIUM/HIGH)\n"
        "4) A brief explanation\n\n"
        "Return the results in JSON format: "
        "[{\"line\":0,\"anomaly_score\":0.85,\"risk\":\"HIGH\",\"explanation\":\"...\"}, ...]"
    )
    
    return prompt

def prediction_llm_risk_score():
    df = pd.read_csv(NEW_FEATURES_FILE)
    prompt = make_global_prompt(df)
    llm_output = call_hf(prompt)

    try:
        results = json.loads(llm_output)
    except json.JSONDecodeError:
        print("Erreur JSON, sortie brute :")
        print(llm_output)
        results = []

    print(f"{len(results)} anomalies détectées")
    for r in results:
        print(r)

    return results

def main():
    prediction_llm_risk_score()

if __name__ == "__main__":
    main()