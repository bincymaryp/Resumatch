

def get_resume_tips(resume_text):
    tips = []
    text = resume_text.lower()

    
    if "objective" not in text and "summary" not in text:
        tips.append("Add a short and strong Objective or Summary at the top.")

    
    if "project" not in text:
        tips.append("Mention academic or personal projects to show practical skills.")

    
    if "internship" not in text:
        tips.append("Include any internship experience to boost credibility.")

    
    if "certification" not in text and "certified" not in text:
        tips.append("Add any certifications relevant to your target role.")

    
    if "%" not in resume_text and any(word in text for word in ["achieved", "increased", "reduced", "improved"]):
        tips.append("Include numbers or percentages to highlight impact (e.g., 'Increased efficiency by 20%').")

  
    word_count = len(resume_text.split())
    if word_count < 150:
        tips.append("Your resume is too short. Add more experience, skills, or projects.")
    elif word_count > 1000:
        tips.append("Your resume seems too long. Try to keep it concise and under 1 page for freshers.")

   
    if "team" not in text:
        tips.append("Mention any experiences working in a team.")
    if "lead" not in text and "managed" not in text:
        tips.append("Highlight any leadership or management experiences.")

 
    if "linkedin.com" not in text:
        tips.append("Include a link to your LinkedIn profile.")
    if "github.com" not in text and "portfolio" not in text:
        tips.append("Include your GitHub or personal portfolio link.")

   
    if "education" not in text:
        tips.append("Make sure your academic background is clearly listed.")

   
    if "i am" in text or "i have" in text:
        tips.append("Avoid using first-person language like 'I am' or 'I have' in resumes.")

    return tips
