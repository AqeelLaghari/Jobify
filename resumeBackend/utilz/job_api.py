import requests

APP_ID = "REMOVED"
APP_KEY = "REMOVED"

def fetch_jobs(keyword):
    url = "https://api.adzuna.com/v1/api/jobs/gb/search/1"

    params = {
        "app_id": APP_ID,
        "app_key": APP_KEY,
        "what": keyword,
        "results_per_page": 10
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        print(f"Adzuna URL: {response.url}")
        print(f"Adzuna Status: {response.status_code}")
        response.raise_for_status()
        data = response.json()
        print(f"Adzuna Response: {data}")
    except requests.exceptions.RequestException as e:
        print(f"Adzuna API request failed: {e}")
        return []

    if "error" in data:
        print(f"Adzuna API error: {data['error']}")
        return []

    jobs = []

    for job in data.get("results", []):
        jobs.append({
            "title": job.get("title"),
            "description": job.get("description"),
            "link": job.get("redirect_url")
        })

    return jobs
