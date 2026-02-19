from fastapi import FastAPI, UploadFile, File, Header, HTTPException
from prediction_isolation_forest import main
from pathlib import Path
import shutil


app = FastAPI()

@app.get("/")
def root():
    return {"status": "ok", "service": "log worker"}

@app.post("/predict")
def predict(
    file: UploadFile = File(...),
    x_api_key: str = Header(None)
):
    upload_dir = Path("files")
    upload_dir.mkdir(exist_ok=True)
    
    if x_api_key != "SECRET123":
        raise HTTPException(status_code=401, detail="Invalid API Key")

    if not file.filename.endswith(".log"):
        raise HTTPException(400, "Only .log files allowed")

    log_path = upload_dir / "access.log"

    with open(log_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    results = main()

    return {
        "status": "ok",
        "count": len(results),
        "data": results
    }

@app.get("/health")
def health():
    return {"status": "ok"}