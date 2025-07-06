import os
import json

def extract_text_from_resume(filepath):
    ext = os.path.splitext(filepath)[1].lower()
    if ext == '.pdf':
        from pdfminer.high_level import extract_text as extract_pdf_text
        raw_text = extract_pdf_text(filepath)
    elif ext == '.docx':
        from docx import Document
        doc = Document(filepath)
        raw_text = '\n'.join([para.text for para in doc.paragraphs])
    else:
        return "Unsupported file format"

    # 🧼 Clean up: remove excessive newlines and join short lines
    lines = raw_text.splitlines()
    cleaned_lines = []
    buffer = ""

    for line in lines:
        line = line.strip()
        if len(line.split()) <= 2 and not line.endswith('.'):
            buffer += " " + line
        else:
            if buffer:
                cleaned_lines.append(buffer.strip())
                buffer = ""
            cleaned_lines.append(line)

    if buffer:
        cleaned_lines.append(buffer.strip())

    return '\n'.join(cleaned_lines)


def extract_skills(text):
    # Load skill list from JSON
    with open('app/skills.json', 'r') as f:
        skill_list = json.load(f)

    text_lower = text.lower()
    found_skills = [skill for skill in skill_list if skill in text_lower]
    return list(set(found_skills))

SKILL_CATEGORIES = {
    "Frontend": ["html", "css", "javascript", "react", "vue", "angular"],
    "Backend": ["python", "flask", "django", "node.js", "express", "java"],
    "Database": ["mysql", "postgresql", "mongodb", "sqlite"],
    "DevOps": ["docker", "kubernetes", "jenkins", "aws", "azure", "gcp"],
    "Tools": ["git", "postman", "jira", "figma", "vscode"]
}

def categorize_skills(skills):
    categorized = {category: [] for category in SKILL_CATEGORIES}
    for skill in skills:
        for category, keywords in SKILL_CATEGORIES.items():
            if skill.lower() in keywords:
                categorized[category].append(skill)
    return {k: v for k, v in categorized.items() if v}
