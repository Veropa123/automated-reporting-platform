# Automated Reporting Platform

A portfolio-ready backend application for importing business data, validating datasets, calculating key performance indicators (KPIs), and generating structured analytical summaries.

## Project Goal

The project demonstrates practical skills in Python backend development, data processing, API design, testing, and documentation.

The first version focuses on a clean and testable API for analyzing CSV and Excel datasets. Future iterations will add persistent storage, charts, downloadable reports, authentication, and Docker-based deployment.

## Current Features

- FastAPI backend
- Health-check endpoint
- CSV and Excel upload support
- Dataset validation
- Missing-value analysis
- Numeric summary statistics
- Basic KPI calculation
- Sample business dataset
- Automated tests with Pytest

## Planned Features

- PostgreSQL persistence
- Configurable KPI rules
- Chart generation
- PDF and Excel report export
- Authentication
- Docker and Docker Compose
- CI workflow
- Expanded test coverage

## Tech Stack

- Python
- FastAPI
- Pandas
- Pytest
- OpenPyXL

## Project Structure

```text
automated-reporting-platform/
├── app/
│   ├── main.py
│   └── services/
│       └── data_analyzer.py
├── sample_data/
│   └── sales.csv
├── tests/
│   ├── test_analyzer.py
│   └── test_health.py
├── .env.example
├── .gitignore
├── README.md
└── requirements.txt
```

## Run Locally

```bash
git clone https://github.com/Veropa123/automated-reporting-platform.git
cd automated-reporting-platform

python -m venv .venv
```

Activate the virtual environment.

Windows:

```bash
.venv\Scripts\activate
```

macOS/Linux:

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Start the API:

```bash
uvicorn app.main:app --reload
```

Open the interactive API documentation at:

```text
http://127.0.0.1:8000/docs
```

## Run Tests

```bash
pytest
```

## Example Dataset

A sample sales dataset is included in `sample_data/sales.csv` so the project can be tested without external data.

## Portfolio Purpose

This project is being developed as a complete technical case study that demonstrates backend development, data analysis, clean project structure, documentation, and testing.

## License

MIT
