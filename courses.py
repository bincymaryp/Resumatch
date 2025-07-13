import json

def get_courses_for_skills(missing_skills):
    try:
        with open("assets/courses.json", "r", encoding="utf-8") as file:
            course_data = json.load(file)
    except FileNotFoundError:
        return {}

    recommendations = {}
    for skill in missing_skills:
        recommendations[skill] = course_data.get(skill.lower(), None)

    return recommendations
