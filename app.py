from flask import Flask, render_template, request, jsonify
import os

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

SKILLS = [
    "python", "java", "sql", "machine learning",
    "docker", "aws", "javascript", "react"
]

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/matcher")
def matcher():
    return render_template("index.html")

# 🔥 THIS ROUTE WAS MISSING
@app.route("/analyze", methods=["POST"])
def analyze():
    resume = request.files["resume"]
    job_desc = request.form["job"].lower()

    path = os.path.join(UPLOAD_FOLDER, resume.filename)
    resume.save(path)

    resume_text = open(path, encoding="utf-8", errors="ignore").read().lower()

    matched = []
    missing = []

    for skill in SKILLS:
        if skill in job_desc:
            if skill in resume_text:
                matched.append(skill)
            else:
                missing.append(skill)

    score = round(
        (len(matched) / max(len(matched) + len(missing), 1)) * 100,
        2
    )

    return jsonify({
        "score": score,
        "matched": matched,
        "missing": missing
    })

if __name__ == "__main__":
    app.run(debug=True)
