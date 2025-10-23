import re

def highlight_keywords(text, keywords):
    """
    Highlights all occurrences of keywords in the text using <mark>.
    """
    def replace(match):
        return f"<mark>{match.group(0)}</mark>"

    for kw in keywords:
        pattern = re.compile(rf'\b{re.escape(kw)}\b', flags=re.IGNORECASE)
        text = pattern.sub(replace, text)
    return text

def highlight_skills_intensity(text, skills_dict):
    """
    Highlights skills in text with intensity based on relevance.
    skills_dict: {"python": 1.0, "nlp": 0.7}  # 1.0 = high relevance
    """
    def replace(match):
        skill = match.group(0).lower()
        intensity = int(skills_dict.get(skill, 0.5) * 255)
        return f"<span style='background-color: rgba(255, {255-intensity}, 0, 0.5)'>{match.group(0)}</span>"

    for skill in skills_dict.keys():
        pattern = re.compile(rf'\b{re.escape(skill)}\b', flags=re.IGNORECASE)
        text = pattern.sub(replace, text)
    return text
