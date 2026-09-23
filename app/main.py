from fastapi import FastAPI, File, HTTPException, UploadFile

from app.services.data_analyzer import analyze_uploaded_file

app = FastAPI(
    title="Automated Reporting Platform",
    description="API for validating business datasets and generating analytical summaries.",
    version="0.1.0",
)


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/analyze")
async def analyze_file(file: UploadFile = File(...)) -> dict:
    try:
        return await analyze_uploaded_file(file)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
