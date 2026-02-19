from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel
import base64
import os
from prediction_isolation_forest import main

app = FastAPI()

FILES_DIR = "files"
os.makedirs(FILES_DIR, exist_ok=True)

class PredictRequest(BaseModel):
    filename: str
    content_base64: str  # on envoie le contenu du fichier encodé en base64


@app.post("/predict")
async def predict(x_api_key: str = Header(None), body: PredictRequest = None):
    if x_api_key != "SECRET123":
        raise HTTPException(status_code=401, detail="Invalid API Key")
    
    file_bytes = base64.b64decode(body.content_base64)
    file_path = os.path.join(FILES_DIR, "access.log")

    print(f"Received file: {file_path}, size: {len(file_bytes)} bytes")

    with open(file_path, "wb") as f:
        f.write(file_bytes)
    print(f"File saved at {file_path}")
    
    results = main()

    return {
        "status": "ok",
        "filename": FILES_DIR,
        "count": len(results),
        "data": results
    }

@app.get("/health")
def health():
    return {"status": "ok"}