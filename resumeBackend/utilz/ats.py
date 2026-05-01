from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def calculate_ats_score(resume_text, jobs):
    if not jobs:
        return 0, ["No jobs found to compare."]

    job_texts = []

    for job in jobs:
        text = f"{job.get('title', '')} {job.get('description', '')}"
        job_texts.append(text)

    documents = [resume_text] + job_texts

    vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = vectorizer.fit_transform(documents)

    resume_vector = tfidf_matrix[0]
    job_vectors = tfidf_matrix[1:]

    similarities = cosine_similarity(resume_vector, job_vectors)

    avg_score = similarities.mean() * 100

    # 🔍 Suggestions logic
    feature_names = vectorizer.get_feature_names_out()
    resume_words = set(resume_text.lower().split())

    missing_keywords = []

    for i, word in enumerate(feature_names):
        if word not in resume_words:
            missing_keywords.append(word)

    suggestions = []

    if avg_score < 40:
        suggestions.append("Your resume is poorly aligned with job descriptions. Consider adding more relevant skills.")

    if avg_score < 60:
        suggestions.append("Try improving your resume with more job-specific keywords.")

    if missing_keywords:
        suggestions.append(
            f"Consider adding keywords like: {', '.join(missing_keywords[:10])}"
        )

    return round(avg_score, 2), suggestions