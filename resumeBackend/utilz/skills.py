skills_db = [
    "python",
    "sql",
    "machine learning",
    "data analysis",
    "flutter",
    "java"
]

def extract_skills(text):
    found = []

    for skill in skills_db:
        if skill in text:
            found.append(skill)

    return found