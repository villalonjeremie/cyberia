from fastapi import FastAPI, UploadFile, File, Header, HTTPException
from prediction_isolation_forest import main
from pathlib import Path
import shutil
from pydantic import BaseModel

class LogData(BaseModel):
    log: str

app = FastAPI()

@app.get("/")
def root():
    return {"status": "ok", "service": "log worker"}

@app.post("/predict")
def predict(data: LogData, x_api_key: str = Header(None)):

    if x_api_key != "SECRET123":
        raise HTTPException(status_code=401, detail="Invalid API Key")



    with open("files/access.log", "w") as f:
        f.write(data.log)

    results = main()


    return {
        "status": "ok",
        "count": len(results),
        "data": results
    }

@app.get("/health")
def health():
    return {"status": "ok"}