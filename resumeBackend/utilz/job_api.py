import requests

APP_ID = "REMOVED"
APP_KEY = "REMOVED"


def fetch_jobs(keyword):
    url = "https://api.adzuna.com/v1/api/jobs/us/search/1"

    params = {
        "app_id": APP_ID,
        "app_key": APP_KEY,
        "what": keyword,
        "results_per_page": 10
    }

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    try:
        response = requests.get(
            url,
            params=params,
            headers=headers,
            timeout=4  # ⚠️ VERY IMPORTANT for Azure stability
        )

        if response.status_code != 200:
            return []

        data = response.json()

        jobs = []

        for job in data.get("results", []):
            jobs.append({
                "title": job.get("title", "No title"),
                "link": job.get("redirect_url", ""),
                "location": job.get("location", {}).get("display_name", "Unknown"),
                "salary": f"{job.get('salary_min', 'N/A')} - {job.get('salary_max', 'N/A')}"
            })

        return jobs

    except Exception:
        return []