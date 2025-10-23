# modules/experience_level.py
def detect_experience_level(experience_years):
    """
    Categorize candidate as Junior (<3 yrs), Mid (3-7 yrs), Senior (>7 yrs)
    """
    if experience_years < 3:
        return "Junior"
    elif experience_years <= 7:
        return "Mid-Level"
    else:
        return "Senior"
