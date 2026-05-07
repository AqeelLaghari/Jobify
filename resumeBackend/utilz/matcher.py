from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def match_jobs(resume_text, jobs):

    if not jobs:
        return []

    # =========================
    # REMOVE DUPLICATE JOBS
    # =========================
    unique_jobs = []
    seen_titles = set()

    for job in jobs:

        title = job.get("title", "")

        # Clean title properly
        cleaned_title = " ".join(title.split()).strip().lower()

        if cleaned_title == "":
            continue

        if cleaned_title not in seen_titles:
            seen_titles.add(cleaned_title)
            unique_jobs.append(job)

    jobs = unique_jobs

    # =========================
    # CREATE JOB TEXTS
    # =========================
    job_texts = [
        f"{job.get('title', '')} "
        f"{job.get('location', '')} "
        f"{job.get('salary', '')}"
        for job in jobs
    ]

    # =========================
    # TF-IDF DOCUMENTS
    # =========================
    documents = [resume_text] + job_texts

    vectorizer = TfidfVectorizer(stop_words='english')

    tfidf_matrix = vectorizer.fit_transform(documents)

    # =========================
    # RESUME VECTOR
    # =========================
    resume_vector = tfidf_matrix[0]

    # =========================
    # JOB VECTORS
    # =========================
    job_vectors = tfidf_matrix[1:]

    if job_vectors.shape[0] == 0:
        return []

    # =========================
    # COSINE SIMILARITY
    # =========================
    similarities = cosine_similarity(
        resume_vector,
        job_vectors
    )[0]

    # =========================
    # ADD MATCH %
    # =========================
    matched_jobs = []

    for i, job in enumerate(jobs):

        job["match_percentage"] = round(
            similarities[i] * 100,
            2
        )

        matched_jobs.append(job)

    # =========================
    # SORT JOBS
    # =========================
    sorted_jobs = sorted(
        matched_jobs,
        key=lambda x: x["match_percentage"],
        reverse=True
    )

    # =========================
    # RETURN TOP 10
    # =========================
    return sorted_jobs[:10]