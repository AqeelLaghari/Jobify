from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def match_jobs(resume_text, jobs):
    if not jobs:
        return []

    job_descriptions = []

    for job in jobs:
        if job.get("description"):
            job_descriptions.append(job["description"])

    if not job_descriptions:
        return []

    documents = [resume_text] + job_descriptions

    vectorizer = TfidfVectorizer(stop_words="english")
    tfidf_matrix = vectorizer.fit_transform(documents)

    similarity_scores = cosine_similarity(
        tfidf_matrix[0:1],
        tfidf_matrix[1:]
    )[0]

    matched_jobs = []

    for i, score in enumerate(similarity_scores):
        matched_jobs.append({
            "title": jobs[i]["title"],
            "link": jobs[i]["link"],
            "match_percentage": round(score * 100, 2)
        })

    matched_jobs.sort(
        key=lambda x: x["match_percentage"],
        reverse=True
    )

    return matched_jobs[:10]