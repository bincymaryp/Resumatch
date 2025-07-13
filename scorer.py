

def calculate_resume_score(matched, total_expected, grammar_score=7):
    if total_expected == 0:
        return 0

    skill_score = (len(matched) / total_expected) * 70  
    grammar_score = grammar_score * 3 
    final_score = skill_score + grammar_score
    return round(final_score)
