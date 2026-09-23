import pandas as pd

from app.services.data_analyzer import analyze_dataframe


def test_analyze_dataframe_returns_summary_and_kpis() -> None:
    dataframe = pd.DataFrame(
        {
            "product": ["A", "B", "C"],
            "sales": [100, 250, 150],
            "region": ["North", "South", None],
        }
    )

    result = analyze_dataframe(dataframe)

    assert result["rows"] == 3
    assert result["columns"] == 3
    assert result["missing_values"] == {"region": 1}
    assert result["numeric_summary"]["sales"]["sum"] == 500.0
    assert result["kpis"]["total_sales"] == 500.0
    assert result["kpis"]["average_sales"] == 166.67
