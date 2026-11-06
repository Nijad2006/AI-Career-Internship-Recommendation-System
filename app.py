from flask import Flask, render_template, request
from recommendation import recommend_jobs

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/assessment")
def assessment():
    return render_template("assessment.html")


@app.route("/result", methods=["GET", "POST"])
def result():

    if request.method == "POST":

        # Student Details
        name = request.form.get("name")
        college = request.form.get("college")
        degree = request.form.get("degree")
        course = request.form.get("course")
        year = request.form.get("year")
        cgpa = request.form.get("cgpa")
        skills = request.form.get("skills")
        interest = request.form.get("interest")
        job_type = request.form.get("job_type")

        # Get recommendations
        jobs = recommend_jobs(
            course,
            skills,
            interest,
            job_type,
            cgpa
        )

        return render_template(
            "result.html",
            name=name,
            college=college,
            degree=degree,
            course=course,
            year=year,
            cgpa=cgpa,
            skills=skills,
            interest=interest,
            job_type=job_type,
            jobs=jobs
        )

    return render_template("result.html")


@app.route("/about")
def about():
    return render_template("about.html")


if __name__ == "__main__":
    app.run(debug=True)