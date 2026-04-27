def detect_resume_domains(resume_text):
    text = resume_text.lower()

    domains = {
        "Data & Analytics": [
            "sql", "power bi", "excel", "python", "r",
            "data analysis", "data analytics", "dashboard", "reporting",
            "tableau", "pandas", "numpy", "matplotlib", "seaborn",
            "business intelligence", "etl", "data visualization",
            "statistics"
        ],

        "Software Development": [
            "flutter", "dart", "java", "c++", "c#", "python",
            "javascript", "typescript", "react", "angular", "vue",
            "node", "express", "backend", "frontend", "full stack",
            "firebase", "rest api", "android", "ios", "kotlin", "swift"
        ],

        "Machine Learning & AI": [
            "machine learning", "deep learning", "ai", "artificial intelligence",
            "tensorflow", "pytorch", "keras", "scikit-learn",
            "nlp", "computer vision", "data science", "llm"
        ],

        "QA / SQA": [
            "qa", "sqa", "testing", "software testing",
            "selenium", "jira", "postman", "automation testing",
            "manual testing", "test cases", "cypress"
        ],

        "DevOps & Cloud": [
            "aws", "azure", "gcp", "google cloud",
            "docker", "kubernetes", "jenkins", "ci/cd",
            "devops", "cloud computing", "terraform", "linux"
        ],

        "Cyber Security": [
            "cyber security", "ethical hacking", "penetration testing",
            "security analyst", "firewall", "network security",
            "vulnerability assessment"
        ],

        "Database Engineering": [
            "database", "mysql", "postgresql", "mongodb",
            "sql server", "oracle", "dbms", "nosql"
        ],

        # 🎨 GRAPHIC DESIGN
        "Graphic Design": [
            "graphic design", "logo design", "branding",
            "photoshop", "illustrator", "coreldraw",
            "poster design", "flyer design", "banner design",
            "social media posts", "typography", "visual design"
        ],

        # 🎬 VIDEO EDITING
        "Video Editing & Production": [
            "video editing", "adobe premiere pro", "after effects",
            "davinci resolve", "filmora", "capcut",
            "motion graphics", "youtube editing",
            "reels editing", "shorts editing"
        ],

        # 🎞 ANIMATION
        "Animation & Motion Graphics": [
            "animation", "motion graphics", "2d animation",
            "3d animation", "blender", "maya",
            "cinema 4d", "after effects animation"
        ],

        # ✍ CONTENT WRITING
        "Content Writing": [
            "content writing", "copywriting", "blog writing",
            "seo writing", "article writing",
            "technical writing", "script writing"
        ],

        # 🎨 UI/UX
        "UI/UX Design": [
            "ui", "ux", "ui/ux", "figma", "adobe xd",
            "wireframing", "prototyping", "user research",
            "canva", "product design"
        ],

        # 💼 BUSINESS
        "Business & Administration": [
            "business analyst", "project management",
            "operations", "administration",
            "office assistant", "management"
        ],

        # 📈 MARKETING
        "Marketing": [
            "digital marketing", "seo", "sem",
            "social media marketing", "google ads",
            "facebook ads", "email marketing",
            "content marketing"
        ],

        # 💰 FINANCE
        "Finance": [
            "finance", "accounting", "bookkeeping",
            "financial analysis", "budgeting",
            "tax", "investment", "quickbooks"
        ],

        # 👥 HR
        "Human Resources": [
            "hr", "human resources", "recruitment",
            "talent acquisition", "payroll",
            "employee relations"
        ],

        # 🌐 FREELANCING
        "Freelancing / Virtual Assistant": [
            "freelancer", "upwork", "fiverr",
            "virtual assistant", "data entry",
            "customer support", "email handling",
            "online work"
        ],

        # 📡 NETWORKING
        "Network Engineering": [
            "network engineer", "ccna", "routing",
            "switching", "tcp/ip", "dns", "vpn"
        ],

        # 🔧 EMBEDDED / IOT
        "Embedded Systems / IoT": [
            "embedded", "iot", "arduino",
            "raspberry pi", "microcontroller",
            "firmware"
        ],

        # 🎮 GAME DEV
        "Game Development": [
            "unity", "unreal engine",
            "game development", "game design",
            "blender", "c#"
        ]
    }

    scores = {}

    for domain, keywords in domains.items():
        score = 0
        for keyword in keywords:
            if keyword in text:
                score += 1
        scores[domain] = score

    sorted_domains = sorted(scores.items(), key=lambda x: x[1], reverse=True)

    top_domains = [
        domain for domain, score in sorted_domains if score > 0
    ][:3]

    return top_domains


def get_search_query(domain):
    mapping = {
        "Data & Analytics": "data analyst",
        "Software Development": "software engineer",
        "Machine Learning & AI": "machine learning engineer",
        "QA / SQA": "qa engineer",
        "DevOps & Cloud": "devops engineer",
        "Cyber Security": "cyber security analyst",
        "Database Engineering": "database engineer",
        "Graphic Design": "graphic designer",
        "Video Editing & Production": "video editor",
        "Animation & Motion Graphics": "motion graphics designer",
        "Content Writing": "content writer",
        "UI/UX Design": "ui ux designer",
        "Business & Administration": "business analyst",
        "Marketing": "digital marketing specialist",
        "Finance": "financial analyst",
        "Human Resources": "hr specialist",
        "Freelancing / Virtual Assistant": "virtual assistant",
        "Network Engineering": "network engineer",
        "Embedded Systems / IoT": "embedded engineer",
        "Game Development": "game developer"
    }

    return mapping.get(domain, "graduate trainee, senior, junior, fresher")