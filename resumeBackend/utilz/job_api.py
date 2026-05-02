import requests

APP_ID = "REMOVED"
APP_KEY = "REMOVED"

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
        
        
        location = job.get("location", {}).get("display_name", "Not specified")

        
        salary_min = job.get("salary_min")
        salary_max = job.get("salary_max")

        if salary_min and salary_max:
            salary = f"{int(salary_min)} - {int(salary_max)}"
        else:
            salary = "Not disclosed"

        jobs.append({
            "title": job.get("title", "No Title"),
            "location": location,
            "salary": salary,
            "link": job.get("redirect_url", "")
        })

    return jobs