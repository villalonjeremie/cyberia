from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel
import base64
from 

app = FastAPI()

class PredictRequest(BaseModel):
    filename: str
    content_base64: str  # on envoie le contenu du fichier encodé en base64


@app.post("/predict")
async def predict(x_api_key: str = Header(None), body: PredictRequest = None):
    if x_api_key != "SECRET123":
        raise HTTPException(status_code=401, detail="Invalid API Key")
    
    # Décodage du contenu
    file_bytes = base64.b64decode(body.content_base64)
    
    # Logging du fichier (taille, etc.)
    print(f"Received file: {body.filename}, size: {len(file_bytes)} bytes")
    
    # Sauvegarde sur le container (optionnel)
    with open(f"/files/{body.filename}", "wb") as f:
        f.write(file_bytes)

    results = main()

    return {"status": "ok", "filename": body.filename,  "count": len(results), "data": results}

@app.get("/health")
def health():
    return {"status": "ok"}