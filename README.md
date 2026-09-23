# Automated Reporting Platform

[![Live Demo](https://img.shields.io/badge/Live_Demo-Open_App-4C6EF5?style=for-the-badge)](https://automated-reporting-platform.onrender.com/)
[![API Docs](https://img.shields.io/badge/API_Docs-Swagger-009688?style=for-the-badge)](https://automated-reporting-platform.onrender.com/docs)
[![GitHub](https://img.shields.io/badge/Source_Code-GitHub-181717?style=for-the-badge&logo=github)](https://github.com/Veropa123/automated-reporting-platform)

A portfolio-ready application for importing business data, validating datasets, calculating key performance indicators (KPIs), visualizing analytical summaries, and exporting structured Excel reports.

> **Live application:** https://automated-reporting-platform.onrender.com/

## Project Goal

This project demonstrates practical skills in Python backend development, data processing, API design, dashboard development, automated testing, CI, Docker, and technical documentation.

The application is intentionally built around a real business workflow: upload a dataset, inspect its quality, calculate key metrics, visualize the result, and export a reusable report.

## Current Features

- FastAPI backend
- Interactive web dashboard
- Drag-and-drop CSV and Excel upload
- Sample dataset for instant demo
- Dataset validation
- Missing-value analysis
- Numeric summary statistics
- Basic KPI calculation
- Responsive in-browser visualizations
- JSON analysis download
- Excel report generation
- Interactive Swagger/OpenAPI documentation
- Automated tests with Pytest
- Docker support
- Docker Compose configuration
- GitHub Actions CI workflow
- Public deployment on Render

## Planned Features

- PostgreSQL persistence
- Configurable KPI rules
- Historical analyses
- Authentication and user accounts
- PDF report export
- Expanded visualizations
- Broader test coverage

## Tech Stack

- Python
- FastAPI
- Pandas
- OpenPyXL
- JavaScript
- HTML/CSS
- Pytest
- Docker
- GitHub Actions
- Render

## Architecture

```text
Browser Dashboard
      |
      | CSV / XLSX
      v
   FastAPI
      |
      +----> Pandas data validation and analysis
      |
      +----> KPI generation
      |
      +----> JSON analytical response
      |
      +----> Excel report generator
```

## Project Structure

```text
automated-reporting-platform/
├── .github/
│   └── workflows/
│       └── ci.yml
├── app/
│   ├── main.py
│   ├── services/
│   │   ├── data_analyzer.py
│   │   └── report_generator.py
│   └── static/
│       ├── app.js
│       ├── index.html
│       └── styles.css
├── sample_data/
│   └── sales.csv
├── tests/
│   ├── test_analyzer.py
│   ├── test_api_analysis.py
│   └── test_health.py
├── .env.example
├── .gitignore
├── Dockerfile
├── docker-compose.yml
├── LICENSE
├── README.md
├── render.yaml
└── requirements.txt
```

## Live Demo

Open the deployed application:

https://automated-reporting-platform.onrender.com/

Interactive API documentation:

https://automated-reporting-platform.onrender.com/docs

Health check:

https://automated-reporting-platform.onrender.com/health

> The free Render instance may take a short time to wake up after periods of inactivity.

## Run Locally

Clone the repository:

```bash
git clone https://github.com/Veropa123/automated-reporting-platform.git
cd automated-reporting-platform
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it on Windows:

```bash
.venv\Scripts\activate
```

Activate it on macOS/Linux:

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Start the application:

```bash
uvicorn app.main:app --reload
```

Open:

```text
Dashboard: http://127.0.0.1:8000
API docs:  http://127.0.0.1:8000/docs
```

## Run with Docker

```bash
docker compose up --build
```

Then open:

```text
http://127.0.0.1:8000
```

## Run Tests

```bash
pytest
```

GitHub Actions also runs the test suite automatically on pushes to `main` and on pull requests.

## Demo Workflow

1. Open the dashboard.
2. Click **Use sample data** or upload a CSV/XLSX file.
3. Review row/column counts, completeness, numeric summaries, and missing values.
4. Download the analysis as JSON.
5. Generate a structured Excel report.

A sample dataset is included in `sample_data/sales.csv` so the project can be demonstrated without external files.

## API Endpoints

| Method | Endpoint | Purpose |
| --- | --- | --- |
| GET | `/` | Interactive dashboard |
| GET | `/health` | Health check |
| GET | `/sample-data` | Download sample CSV |
| POST | `/analyze` | Analyze CSV/XLSX data |
| POST | `/report/excel` | Generate Excel report |
| GET | `/docs` | Interactive API documentation |

## Portfolio Purpose

This project is developed as a complete technical case study rather than a code exercise. It demonstrates backend development, data analysis, frontend integration, API design, automated testing, containerization, CI, deployment, and documentation in one practical workflow.

## License

MIT
