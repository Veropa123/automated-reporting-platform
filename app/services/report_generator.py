from __future__ import annotations

from io import BytesIO

import pandas as pd


def build_excel_report(dataframe: pd.DataFrame, analysis: dict) -> bytes:
    output = BytesIO()

    summary_rows = [
        {"metric": "Rows", "value": analysis["rows"]},
        {"metric": "Columns", "value": analysis["columns"]},
        {
            "metric": "Complete rows",
            "value": analysis["kpis"].get("complete_rows", 0),
        },
    ]

    for key, value in analysis["kpis"].items():
        if key in {"total_rows", "complete_rows"}:
            continue
        summary_rows.append(
            {
                "metric": key.replace("_", " ").title(),
                "value": value,
            }
        )

    missing_rows = [
        {"column": column, "missing_values": value}
        for column, value in analysis["missing_values"].items()
    ]

    numeric_rows = []
    for column, metrics in analysis["numeric_summary"].items():
        numeric_rows.append({"column": column, **metrics})

    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        pd.DataFrame(summary_rows).to_excel(writer, sheet_name="Summary", index=False)

        pd.DataFrame(
            missing_rows or [{"column": "No missing values", "missing_values": 0}]
        ).to_excel(writer, sheet_name="Missing Values", index=False)

        pd.DataFrame(
            numeric_rows
            or [
                {
                    "column": "No numeric columns",
                    "count": 0,
                    "mean": 0,
                    "min": 0,
                    "max": 0,
                    "sum": 0,
                }
            ]
        ).to_excel(writer, sheet_name="Numeric Summary", index=False)

        dataframe.head(200).to_excel(writer, sheet_name="Data Preview", index=False)

        for worksheet in writer.book.worksheets:
            worksheet.freeze_panes = "A2"
            for column_cells in worksheet.columns:
                max_length = max(
                    len(str(cell.value)) if cell.value is not None else 0
                    for cell in column_cells
                )
                worksheet.column_dimensions[column_cells[0].column_letter].width = min(
                    max(max_length + 2, 12), 40
                )

    output.seek(0)
    return output.getvalue()
