from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import os
import uuid
import time

from utilz.pdf_parser import extract_text
from utilz.job_api import fetch_jobs
from utilz.matcher import match_jobs
from utilz.domain_detector import detect_resume_domains, get_search_query
from utilz.ats import calculate_ats_score

app = FastAPI()

# =========================
# CORS
# =========================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =========================
# Upload folder
# =========================
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


# =========================
# Root Route
# =========================
@app.get("/")
def read_root():
    return {
        "message": "AI Resume Analyzer API Running"
    }


# =========================
# Health Route
# =========================
@app.get("/health")
def health():
    return {"status": "healthy"}


# =========================
# Analyze Resume
# =========================
@app.post("/analyze-resume")
async def analyze_resume(file: UploadFile = File(...)):

    start_time = time.time()
    file_path = None

    try:

        print("📥 Resume received")

        # =========================
        # Save PDF
        # =========================
        unique_filename = f"{uuid.uuid4()}_{file.filename}"
        file_path = os.path.join(UPLOAD_DIR, unique_filename)

        contents = await file.read()

        with open(file_path, "wb") as f:
            f.write(contents)

        print("✅ PDF saved")

        # =========================
        # Extract Resume Text
        # =========================
        print("⏳ Extracting text from PDF...")

        resume_text = extract_text(file_path)

        if not resume_text or len(resume_text.strip()) == 0:
            return {
                "error": "Could not extract text from PDF"
            }

        print("✅ Resume text extracted")

        # =========================
        # Detect Domains
        # =========================
        print("⏳ Detecting resume domains...")

        top_domains = detect_resume_domains(resume_text)

        print("✅ Domains detected:", top_domains)

        # =========================
        # Fetch Jobs
        # =========================
        all_jobs = []
        search_queries = []

        for domain in top_domains:

            query = get_search_query(domain)

            search_queries.append(query)

            print(f"⏳ Fetching jobs for: {query}")

            jobs = fetch_jobs(query)

            print(f"✅ Jobs fetched: {len(jobs)}")

            if jobs:
                all_jobs.extend(jobs)

        print("✅ Total jobs before cleaning:", len(all_jobs))

        # =========================
        # Remove Duplicate Jobs
        # =========================
        unique_jobs = []
        seen_titles = set()

        for job in all_jobs:

            title = job.get("title", "")

            # Clean title properly
            cleaned_title = " ".join(title.split()).strip().lower()

            # Skip empty titles
            if cleaned_title == "":
                continue

            if cleaned_title not in seen_titles:
                seen_titles.add(cleaned_title)
                unique_jobs.append(job)

        print("✅ Unique jobs after cleaning:", len(unique_jobs))

        # =========================
        # Limit jobs for speed
        # =========================
        unique_jobs = unique_jobs[:20]

        # =========================
        # Match Jobs
        # =========================
        print("⏳ Matching jobs with resume...")

        matched_jobs = match_jobs(resume_text, unique_jobs)

        print("✅ Job matching completed")

        # =========================
        # ATS Score
        # =========================
        print("⏳ Calculating ATS score...")

        ats_score, suggestions = calculate_ats_score(
            resume_text,
            matched_jobs
        )

        print("✅ ATS calculation completed")

        # =========================
        # Total Time
        # =========================
        total_time = round(time.time() - start_time, 2)

        print(f"⏱ Completed in {total_time} seconds")

        # =========================
        # Response
        # =========================
        return {
            "filename": file.filename,
            "top_domains": top_domains,
            "search_queries": search_queries,
            "total_jobs_fetched": len(unique_jobs),
            "top_matches": matched_jobs,
            "ats_score": ats_score,
            "suggestions": suggestions,
            "processing_time": total_time
        }

    except Exception as e:

        print("❌ ERROR:", str(e))

        return {
            "error": str(e)
        }

    finally:

        # =========================
        # Delete uploaded file
        # =========================
        try:
            if file_path and os.path.exists(file_path):
                os.remove(file_path)
                print("🗑 Uploaded PDF deleted")
        except Exception as delete_error:
            print("❌ File delete error:", delete_error)