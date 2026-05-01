from fastapi import FastAPI, UploadFile, File
from utilz.pdf_parser import extract_text
from utilz.job_api import fetch_jobs
from utilz.matcher import match_jobs
from sklearn.feature_extraction.text import TfidfVectorizer
from utilz.domain_detector import detect_resume_domains, get_search_query
from utilz.ats import calculate_ats_score

app = FastAPI()



@app.get("/")
def read_root():
    return {
        "message": "AI Resume Analyzer API Running"
    }


@app.post("/analyze-resume")
async def analyze_resume(file: UploadFile = File(...)):
    contents = await file.read()

    with open(file.filename, "wb") as f:
        f.write(contents)

    resume_text = extract_text(file.filename)

    



    top_domains = detect_resume_domains(resume_text)

    all_jobs = []
    search_queries = []

    for domain in top_domains:
        query = get_search_query(domain)
        search_queries.append(query)

        jobs = fetch_jobs(query)
        all_jobs.extend(jobs)


    unique_jobs = []
    seen_titles = set()

    for job in all_jobs:
        title = job.get("title", "").lower()

        if title not in seen_titles:
            seen_titles.add(title)
            unique_jobs.append(job)


    matched_jobs = match_jobs(resume_text, unique_jobs)
    ats_score, suggestions = calculate_ats_score(resume_text, matched_jobs)

    return {
    "filename": file.filename,
    "top_domains": top_domains,
    "search_queries": search_queries,
    "total_jobs_fetched": len(unique_jobs),
    "top_matches": matched_jobs,
    "ats_score": ats_score,
    "suggestions": suggestions
}


def extract_search_keyword(resume_text):
    documents = [resume_text]

    vectorizer = TfidfVectorizer(
        stop_words="english",
        max_features=10
    )



    tfidf_matrix = vectorizer.fit_transform(documents)

    keywords = vectorizer.get_feature_names_out()

    search_query = " ".join(keywords[:5])

    return search_query
