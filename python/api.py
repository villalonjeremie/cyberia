from fastapi import FastAPI, HTTPException, Header
from prediction_isolation_forest import main

app = FastAPI()

@app.get("/")
def root():
    return {"status": "ok", "service": "log worker"}

@app.post("/predict")
def predict(x_api_key: str = Header(None)):

    if x_api_key != "SECRET123":
        raise HTTPException(401)

    results = main()
    return {
        "status": "ok",
        "data": results
    }

@app.get("/health")
def health():
    return {"status": "ok"}