from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_analyze_csv_file() -> None:
    response = client.post(
        "/analyze",
        files={
            "file": (
                "sales.csv",
                b"product,sales\nA,100\nB,250\nC,150\n",
                "text/csv",
            )
        },
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["rows"] == 3
    assert payload["kpis"]["total_sales"] == 500.0


def test_excel_report_download() -> None:
    response = client.post(
        "/report/excel",
        files={
            "file": (
                "sales.csv",
                b"product,sales\nA,100\nB,250\n",
                "text/csv",
            )
        },
    )

    assert response.status_code == 200
    assert response.headers["content-type"].startswith(
        "application/vnd.openxmlformats-officedocument"
    )
    assert response.content.startswith(b"PK")


def test_dashboard_is_available() -> None:
    response = client.get("/")

    assert response.status_code == 200
    assert "Automated Reporting Platform" in response.text
