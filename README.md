# SaaS Hiring & Layoff Signal Tracker

This project pulls tech news from Hacker News, uses Gemini to find which companies are hiring or doing layoffs, saves it to a CSV, and shows it on a Streamlit dashboard. It runs in Docker and GitHub Actions runs it every day.

## Files

- `fetch_data.py` gets headlines from Hacker News
- `analyze_trends.py` sends them to Gemini and gets the signals back
- `save_trends.py` runs everything and saves to `trends_log.csv`
- `dashboard.py` is the dashboard
- `tests/` has the tests

## How to run

```
bash setup.sh
source venv/bin/activate
python save_trends.py
streamlit run dashboard.py
```

## With Docker

```
docker build -t signal-tracker .
docker run -p 8501:8501 signal-tracker
```

Then go to http://localhost:8501

## Built with

Python, Gemini API, Pandas, Streamlit, Docker, GitHub Actions, Pytest
