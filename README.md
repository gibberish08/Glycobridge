# Glycobridge
🧬 Diabetes Data API

A FastAPI + Streamlit-based platform to upload patient health data in CSV or Excel format and instantly receive a secure API endpoint and API key to access structured, cleaned tabular data.

Perfect for medical data apps, dashboards, and AI/ML pipelines that require easy integration of custom patient data.

🚀 Features

📁 Upload .csv or .xlsx patient datasets via a simple UI
🔑 Get a unique API key and endpoint per upload
🧹 Automatic data cleaning and standardization
🔒 Secure access to data via API key authentication
🧪 Designed for use in platforms like NexFlow or custom Python pipelines
🧰 Tech Stack

Frontend: Streamlit for simple upload and results display
Backend: FastAPI with file handling and secure API access
Data Processing: pandas for CSV/Excel parsing and normalization
Storage: Local file-based JSON storage (can be swapped for a database)
🖥️ Usage

1. Run the Backend
uvicorn main:app --reload
2. Run the Frontend
streamlit run app.py
🔄 API Workflow

Upload your file in the frontend.
Receive:
✅ API Key
🌐 Endpoint: /api/v1/data
Make GET requests like this:
import requests

headers = {
    "Authorization": "Bearer <your-api-key>"
}

response = requests.get("http://localhost:8000/api/v1/data", headers=headers)
print(response.json())
📋 Expected File Format

Column	Description
glucose (mg/dL)	Blood glucose level
insulin (uU/mL)	Insulin concentration
A1C (%)	Hemoglobin A1C percentage
...	Additional patient metrics
Column names will be normalized (lowercased, spaces to underscores). Missing values like "N/A" are handled automatically.
📦 Future Improvements

Rate limiting / API key expiration
JWT-based auth or OAuth integration
Persistent database (PostgreSQL, MongoDB)
File preview, validations, and visualization
