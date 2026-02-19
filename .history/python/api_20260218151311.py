INFO:     172.20.0.4:35456 - "POST /predict HTTP/1.1" 422 Unprocessable Entity

@app.get("/health")
def health():
    return {"status": "ok"}