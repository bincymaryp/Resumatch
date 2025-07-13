import json
import re

def clean_and_tokenize(text):
    
    text = text.lower()
    tokens = re.findall(r'\b[a-zA-Z]+\b', text)
    return set(tokens)

def load_role_skills(role):
    with open("assets/skills.json", "r", encoding="utf-8") as file:
        skills_data = json.load(file)
    return set(skills_data.get(role.lower(), []))

def analyze_skills(resume_text, selected_role):
    resume_tokens = clean_and_tokenize(resume_text)
    expected_skills = load_role_skills(selected_role)

    matched_skills = sorted(list(expected_skills.intersection(resume_tokens)))
    missing_skills = sorted(list(expected_skills.difference(resume_tokens)))

    return matched_skills, missing_skills
