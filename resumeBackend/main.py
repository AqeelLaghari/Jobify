from utilz.job_api import fetch_jobs
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {
        "message": "ResumeBackend API is running",
        "available_endpoints": ["/test-jobs"]
    }

@app.get("/test-jobs")
def test_jobs():
    return fetch_jobs("data analyst")
