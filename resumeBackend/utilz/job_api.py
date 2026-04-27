import requests

APP_ID = "b69c4db0"
APP_KEY = "ee33a282619590bf3364c48e494ad164"

def fetch_jobs(keyword):
    url = "https://api.adzuna.com/v1/api/jobs/gb/search/1"

    params = {
        "app_id": APP_ID,
        "app_key": APP_KEY,
        "what": keyword,
        "results_per_page": 20
    }

    response = requests.get(url, params=params)
    data = response.json()

    jobs = []

    for job in data.get("results", []):
        jobs.append({
            "title": job.get("title"),
            "description": job.get("description"),
            "link": job.get("redirect_url")
        })

    return jobs



