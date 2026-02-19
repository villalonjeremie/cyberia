from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel
import base64
import os
from prediction_isolation_forest import main

app = FastAPI()

FILES_DIR = "/files"
os.makedirs(FILES_DIR, exist_ok=True)

class PredictRequest(BaseModel):
    filename: str
    content_base64: str  # on envoie le contenu du fichier encodé en base64


@app.post("/predict")
async def predict(x_api_key: str = Header(None), body: PredictRequest = None):
    if x_api_key != "SECRET123":
        raise HTTPException(status_code=401, detail="Invalid API Key")
    
    # Décodage du contenu Base64
    file_bytes = base64.b64decode(body.content_base64)
    
    # Logging du fichier (taille, nom)
    print(f"Received file: {body.filename}, size: {len(file_bytes)} bytes")
    
    # Sauvegarde sécurisée
    file_path = os.path.join(FILES_DIR, "a")
    with open(file_path, "wb") as f:
        f.write(file_bytes)
    print(f"File saved at {file_path}")
    
    # Appel à ton module de prédiction
    results = main()

    return {
        "status": "ok",
        "filename": body.filename,
        "count": len(results),
        "data": results
    }

@app.get("/health")
def health():
    return {"status": "ok"}