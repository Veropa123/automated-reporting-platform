from pathlib import Path

from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.responses import FileResponse, Response
from fastapi.staticfiles import StaticFiles

from app.services.data_analyzer import (
    analyze_dataframe,
    analyze_uploaded_file,
    read_uploaded_dataframe,
)
from app.services.report_generator import build_excel_report

BASE_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = BASE_DIR.parent

app = FastAPI(
    title="Automated Reporting Platform",
    description="API for validating business datasets and generating analytical summaries.",
    version="0.2.0",
)

app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")


@app.get("/", include_in_schema=False)
def dashboard() -> FileResponse:
    return FileResponse(BASE_DIR / "static" / "index.html")


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/sample-data", include_in_schema=False)
def sample_data() -> FileResponse:
    return FileResponse(
        PROJECT_ROOT / "sample_data" / "sales.csv",
        media_type="text/csv",
        filename="sales.csv",
    )


@app.post("/analyze")
async def analyze_file(file: UploadFile = File(...)) -> dict:
    try:
        return await analyze_uploaded_file(file)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.post("/report/excel")
async def generate_excel_report(file: UploadFile = File(...)) -> Response:
    try:
        dataframe = await read_uploaded_dataframe(file)
        analysis = analyze_dataframe(dataframe)
        report = build_excel_report(dataframe, analysis)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    headers = {
        "Content-Disposition": 'attachment; filename="automated-analysis-report.xlsx"'
    }

    return Response(
        content=report,
        media_type=(
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        ),
        headers=headers,
    )
