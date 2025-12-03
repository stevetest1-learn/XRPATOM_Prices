# ATOM vs XRP Price Chart

Simple Flask app with:
- JSON API: `/api/prices?days=N`
- CSV: `/api/prices/csv?days=N`
- UI: `/` (Chart.js)

Run locally:
1. python -m venv venv
2. .\venv\Scripts\Activate.ps1
3. pip install -r requirements.txt
4. python web_app.py
Open http://127.0.0.1:5000

Deploy:
- With Docker: build and run using the provided Dockerfile.
- With Heroku: use the Procfile with `web: gunicorn --bind 0.0.0.0:$PORT web_app:app`