import spacy
import re

nlp = spacy.load("en_core_web_sm")

EDUCATION_KEYWORDS = [
    'bachelor', 'master', 'b.tech', 'm.tech', 'phd', 'b.sc', 'm.sc', 'btech', 'msc'
]

def extract_email(text):
    emails = re.findall(r'\S+@\S+', text)
    return emails[0] if emails else None

def extract_phone(text):
    phones = re.findall(r'\+?\d[\d -]{8,12}\d', text)
    return phones[0] if phones else None

def extract_name(text):
    doc = nlp(text)
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            return ent.text
    return None

def extract_education(text):
    text_lower = text.lower()
    edu = [word.upper() if '.' not in word else word.title() for word in EDUCATION_KEYWORDS if word in text_lower]
    return edu

def extract_experience(text):
    """
    Returns experience as float (years) if found, else 0.
    """
    exp = re.findall(r'(\d+)\+?\s+years?', text.lower())
    if exp:
        try:
            return float(exp[0])
        except ValueError:
            return 0.0
    return 0.0

def extract_ner_details(text):
    return {
        "name": extract_name(text),
        "email": extract_email(text),
        "phone": extract_phone(text),
        "education": ", ".join(extract_education(text)),
        "experience": extract_experience(text)
    }
