from fastapi import FastAPI, Request, Header, HTTPException

app = FastAPI()

@app.post("/predict")
async def predict(
    request: Request,
    x_api_key: str = Header(None)
):

    if x_api_key != "SECRET123":
        raise HTTPException(status_code=401, detail="Bad API key")

    raw = await request.body()

    from fastapi import FastAPI, Request, Header, HTTPException

app = FastAPI()

@app.post("/predict")
async def predict(
    request: Request,
    x_api_key: str = Header(None)
):

    if x_api_key != "SECRET123":
        raise HTTPException(status_code=401, detail="Bad API key")

    raw = await request.body()

    print("==== LOG DATA ====")
    print(data)
    print("==== END LOG ====")

    if not raw:
        raise HTTPException(status_code=400, detail="Empty body")

    log_text = raw.decode("utf-8", errors="ignore")

    with open("files/access.log", "w") as f:
        f.write(log_text)

    return {
        "status": "ok",
        "size": len(raw),
        "lines": len(log_text.splitlines())
    }


    if not raw:
        raise HTTPException(status_code=400, detail="Empty body")

    log_text = raw.decode("utf-8", errors="ignore")

    with open("files/access.log", "w") as f:
        f.write(log_text)

    return {
        "status": "ok",
        "size": len(raw),
        "lines": len(log_text.splitlines())
    }


@app.get("/health")
def health():
    return {"status": "ok"}