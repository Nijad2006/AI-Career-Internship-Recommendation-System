import pandas as pd

# Load LinkedIn dataset
df = pd.read_csv("dataset/cleaned_postings.csv")


def recommend_jobs(course, skills, interest, job_type, cgpa):

    jobs = df.copy()

    # -----------------------------
    # Filter Job / Internship
    # -----------------------------
    if job_type == "Internship":
        jobs = jobs[
            jobs["title"].astype(str).str.contains(
                "intern",
                case=False,
                na=False
            )
        ]
    else:
        jobs = jobs[
            ~jobs["title"].astype(str).str.contains(
                "intern",
                case=False,
                na=False
            )
        ]

    # -----------------------------
    # Course Keywords
    # -----------------------------
    course_map = {

        "Computer Science": [
            "software",
            "developer",
            "engineer",
            "programmer",
            "web"
        ],

        "AI & ML": [
            "artificial intelligence",
            "machine learning",
            "ai",
            "data scientist"
        ],

        "Data Science": [
            "data scientist",
            "data analyst",
            "analytics"
        ],

        "Cyber Security": [
            "cyber",
            "security",
            "soc"
        ],

        "Cloud Computing": [
            "cloud",
            "aws",
            "azure",
            "devops"
        ],

        "Information Technology": [
            "it",
            "system",
            "network"
        ]

    }

    keywords = course_map.get(course, [interest.lower()])

    scores = []

    for _, row in jobs.iterrows():

        score = 0

        title = str(row["title"]).lower()
        description = str(row["description"]).lower()
        skill_text = str(row["skills_desc"]).lower()

        # -----------------------------
        # Course Match (40)
        # -----------------------------
        for word in keywords:

            if word in title:
                score += 40
                break

        # -----------------------------
        # Interest Match (20)
        # -----------------------------
        if interest.lower() in title or interest.lower() in description:
            score += 20

        # -----------------------------
        # Skills Match (20)
        # -----------------------------
        student_skills = skills.lower().split(",")

        for skill in student_skills:

            if skill.strip() in skill_text:
                score += 5

        # -----------------------------
        # CGPA Score (20)
        # -----------------------------
        try:

            cg = float(cgpa)

            if cg >= 9:
                score += 20

            elif cg >= 8:
                score += 15

            elif cg >= 7:
                score += 10

            elif cg >= 6:
                score += 5

            else:
                score -= 10

        except:
            pass

        scores.append(score)

    jobs["match_score"] = scores

    jobs = jobs.sort_values(
        by="match_score",
        ascending=False
    )

    return jobs.head(5).to_dict("records")