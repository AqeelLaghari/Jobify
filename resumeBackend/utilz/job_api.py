import requests

APP_ID = "b69c4db0"
APP_KEY = "ee33a282619590bf3364c48e494ad164"

def fetch_jobs(keyword):
    url = "https://api.adzuna.com/v1/api/jobs/us/search/1"

    params = {
        "app_id": APP_ID,
        "app_key": APP_KEY,
        "what": keyword,
        "results_per_page": 20
    }

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    try:
        response = requests.get(
            url,
            params=params,
            headers=headers,
            timeout=5   # ✅ CRITICAL FIX (prevents hanging)
        )

        print("STATUS:", response.status_code)

        if response.status_code != 200:
            print("API ERROR:", response.text)
            return []

        data = response.json()

        jobs = []
        for job in data.get("results", []):
            jobs.append({
                "title": job.get("title"),
                "link": job.get("redirect_url"),
                "location": job.get("location", {}).get("display_name", "Unknown"),
                "salary": str(job.get("salary_min", "N/A")) + " - " + str(job.get("salary_max", "N/A"))
            })

        return jobs

    except requests.exceptions.Timeout:
        print("❌ API Timeout")
        return []

    except Exception as e:
        print("❌ API Error:", e)
        return []