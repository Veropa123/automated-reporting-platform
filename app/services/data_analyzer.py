from __future__ import annotations

from io import BytesIO

import pandas as pd
from fastapi import UploadFile


SUPPORTED_EXTENSIONS = {".csv", ".xlsx"}


def _extension(filename: str) -> str:
    name = (filename or "").lower()
    if name.endswith(".csv"):
        return ".csv"
    if name.endswith(".xlsx"):
        return ".xlsx"
    return ""


async def analyze_uploaded_file(file: UploadFile) -> dict:
    extension = _extension(file.filename or "")
    if extension not in SUPPORTED_EXTENSIONS:
        raise ValueError("Unsupported file type. Upload a CSV or XLSX file.")

    content = await file.read()
    if not content:
        raise ValueError("The uploaded file is empty.")

    buffer = BytesIO(content)

    try:
        if extension == ".csv":
            dataframe = pd.read_csv(buffer)
        else:
            dataframe = pd.read_excel(buffer)
    except Exception as exc:
        raise ValueError("The dataset could not be read.") from exc

    return analyze_dataframe(dataframe)


def analyze_dataframe(dataframe: pd.DataFrame) -> dict:
    if dataframe.empty:
        raise ValueError("The dataset contains no rows.")

    numeric = dataframe.select_dtypes(include="number")
    missing_values = {
        column: int(value)
        for column, value in dataframe.isna().sum().items()
        if int(value) > 0
    }

    numeric_summary = {}
    for column in numeric.columns:
        series = numeric[column].dropna()
        if series.empty:
            continue
        numeric_summary[column] = {
            "count": int(series.count()),
            "mean": round(float(series.mean()), 2),
            "min": round(float(series.min()), 2),
            "max": round(float(series.max()), 2),
            "sum": round(float(series.sum()), 2),
        }

    return {
        "rows": int(len(dataframe)),
        "columns": int(len(dataframe.columns)),
        "column_names": [str(column) for column in dataframe.columns],
        "missing_values": missing_values,
        "numeric_summary": numeric_summary,
        "kpis": calculate_basic_kpis(dataframe),
    }


def calculate_basic_kpis(dataframe: pd.DataFrame) -> dict:
    kpis: dict[str, float | int] = {
        "total_rows": int(len(dataframe)),
        "complete_rows": int(dataframe.dropna().shape[0]),
    }

    normalized_columns = {str(column).strip().lower(): column for column in dataframe.columns}

    for candidate in ("sales", "revenue", "amount", "total"):
        if candidate in normalized_columns:
            column = normalized_columns[candidate]
            values = pd.to_numeric(dataframe[column], errors="coerce").dropna()
            if not values.empty:
                kpis[f"total_{candidate}"] = round(float(values.sum()), 2)
                kpis[f"average_{candidate}"] = round(float(values.mean()), 2)
            break

    return kpis
