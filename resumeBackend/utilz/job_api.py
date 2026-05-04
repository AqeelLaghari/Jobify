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
        response = requests.get(
            url,
            params=params,
            timeout=5   # ✅ CRITICAL FIX
        )

        if response.status_code != 200:
            print("❌ Adzuna error:", response.status_code)
            return []

        data = response.json()
        jobs = []

        for job in data.get("results", []):
            jobs.append({
                "title": job.get("title"),
                "location": job.get("location", {}).get("display_name", "N/A"),
                "salary": job.get("salary_max") or job.get("salary_min") or "Not disclosed",
                "link": job.get("redirect_url")
            })

        return jobs

    except requests.exceptions.Timeout:
        print("❌ Adzuna TIMEOUT")
        return []

    except Exception as e:
        print("❌ Adzuna ERROR:", e)
        return []