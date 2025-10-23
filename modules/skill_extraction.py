import spacy

nlp = spacy.load("en_core_web_sm")

# Example skill list
SKILLS_DB = ["python", "java", "c++", "nlp", "machine learning", "data analysis", "deep learning"]

def extract_skills(text):
    text = text.lower()
    skills_found = [skill for skill in SKILLS_DB if skill in text]
    return skills_found
