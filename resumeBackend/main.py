from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import os
import uuid
import time

from utilz.pdf_parser import extract_text
from utilz.job_api import fetch_jobs
from utilz.matcher import match_jobs
from sklearn.feature_extraction.text import TfidfVectorizer
from utilz.domain_detector import detect_resume_domains, get_search_query
from utilz.ats import calculate_ats_score

app = FastAPI()

# ✅ CORS (important for Flutter)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Upload directory
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@app.get("/")
def read_root():
    return {"message": "AI Resume Analyzer API Running"}


@app.post("/analyze-resume")
async def analyze_resume(file: UploadFile = File(...)):
    import time
    start_time = time.time()

    try:
        print("📥 File received")

        unique_filename = f"{uuid.uuid4()}_{file.filename}"
        file_path = os.path.join(UPLOAD_DIR, unique_filename)

        contents = await file.read()
        with open(file_path, "wb") as f:
            f.write(contents)

        print("✅ File saved")

        # 🔴 STEP 1: PDF extraction
        print("⏳ Extracting text...")
        resume_text = extract_text(file_path)
        print("✅ Text extracted")

        # 🔴 STEP 2: Domains
        print("⏳ Detecting domains...")
        top_domains = detect_resume_domains(resume_text)
        print("✅ Domains:", top_domains)

        all_jobs = []
        search_queries = []

        # 🔴 STEP 3: Fetch jobs
        for domain in top_domains:
            print(f"⏳ Fetching jobs for {domain}")
            query = get_search_query(domain)
            search_queries.append(query)

            jobs = fetch_jobs(query)

            print(f"✅ Jobs fetched: {len(jobs)}")

            if jobs:
                all_jobs.extend(jobs)

        print("✅ Total jobs collected:", len(all_jobs))

        # 🔴 STEP 4: Matching
        print("⏳ Matching jobs...")
        matched_jobs = match_jobs(resume_text, all_jobs)
        print("✅ Matching done")

        # 🔴 STEP 5: ATS
        print("⏳ Calculating ATS...")
        ats_score, suggestions = calculate_ats_score(resume_text, matched_jobs)
        print("✅ ATS done")

        os.remove(file_path)

        print("⏱ Total time:", time.time() - start_time)

        return {
            "top_domains": top_domains,
            "top_matches": matched_jobs,
            "ats_score": ats_score,
            "suggestions": suggestions
        }

    except Exception as e:
        print("❌ ERROR:", e)
        return {"error": str(e)}


# Optional helper (unchanged)
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