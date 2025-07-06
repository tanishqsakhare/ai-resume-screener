import os
import re
import pdfkit
from flask import Blueprint, render_template, request, make_response
from .nlp_utils import (
    extract_text_from_resume,
    extract_skills,
    categorize_skills
)

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

def highlight_skills(text, matched_skills):
    """
    Highlights matched skills in the resume text using <mark> tags.
    """
    for skill in matched_skills:
        pattern = re.compile(rf'\b({re.escape(skill)})\b', re.IGNORECASE)
        text = pattern.sub(r'<mark>\1</mark>', text)
    return text

@main.route('/upload', methods=['POST'])
def upload_resume():
    file = request.files.get('resume')
    jobdesc = request.form.get('jobdesc')

    if file and jobdesc:
        # Save uploaded file
        upload_folder = 'app/uploads'
        os.makedirs(upload_folder, exist_ok=True)
        filepath = os.path.join(upload_folder, file.filename)
        file.save(filepath)

        # Extract and clean resume text
        resume_text = extract_text_from_resume(filepath)

        # Extract skills
        resume_skills = extract_skills(resume_text)
        jd_skills = extract_skills(jobdesc)

        # Match skills
        matched_skills = list(set(resume_skills) & set(jd_skills))
        match_score = int((len(matched_skills) / len(jd_skills)) * 100) if jd_skills else 0

        # Highlight matched skills in resume text
        highlighted_text = highlight_skills(resume_text, matched_skills)

        # Categorize matched skills
        categorized_skills = {
          "Frontend": [skill for skill in matched_skills if skill.lower() in ["html", "css", "javascript", "react", "vue", "angular"]],
          "Backend": [skill for skill in matched_skills if skill.lower() in ["flask", "django", "node.js", "express", "java"]],
          "Tools": [skill for skill in matched_skills if skill.lower() in ["git", "postman", "jira", "figma", "vscode"]]
        }

        # Categorize matched skills
        categorized_skills = categorize_skills(matched_skills)
        category_labels = list(categorized_skills.keys())
        category_counts = [len(skills) for skills in categorized_skills.values()]
        matched_count = len(matched_skills)
        resume_only_count = len(resume_skills) - matched_count
        jd_only_count = len(jd_skills) - matched_count



        return render_template(
            'result.html',
            text=highlighted_text,
            jd=jobdesc,
            resume_skills=resume_skills,
            jd_skills=jd_skills,
            matched_skills=matched_skills,
            categorized_skills=categorized_skills,
            category_labels=category_labels,
            category_counts=category_counts,
            matched_count=matched_count,
            resume_only_count=resume_only_count,
            jd_only_count=jd_only_count,
            score=match_score
        )

    return "Missing file or job description"

@main.route('/download', methods=['POST'])
def download_pdf():
    resume_text = request.form.get('text')
    jd = request.form.get('jd')
    matched_skills = request.form.getlist('matched_skills')
    score = request.form.get('score')

    rendered = render_template(
        'report.html',
        text=resume_text,
        jd=jd,
        matched_skills=matched_skills,
        score=score
    )

    pdf = pdfkit.from_string(rendered, False)
    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'attachment; filename=resume_match_report.pdf'
    return response
