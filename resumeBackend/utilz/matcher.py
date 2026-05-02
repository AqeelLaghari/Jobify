from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def match_jobs(resume_text, jobs):
    if not jobs:
        return []

    
    job_texts = [
        f"{job.get('title', '')} {job.get('location', '')}"
        for job in jobs
    ]

    
    documents = [resume_text] + job_texts

    
    vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = vectorizer.fit_transform(documents)

    
    resume_vector = tfidf_matrix[0]

    
    job_vectors = tfidf_matrix[1:]

    
    if job_vectors.shape[0] == 0:
        return []

   
    similarities = cosine_similarity(resume_vector, job_vectors)[0]

    
    for i, job in enumerate(jobs):
        job["match_percentage"] = round(similarities[i] * 100, 2)

    
    sorted_jobs = sorted(
        jobs,
        key=lambda x: x["match_percentage"],
        reverse=True
    )

    # ✅ Return top 10 (or whatever you want)
    return sorted_jobs[:10]