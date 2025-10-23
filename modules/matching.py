from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def compute_text_similarity(resume_text, job_desc_text):
    vectorizer = TfidfVectorizer()
    vectors = vectorizer.fit_transform([resume_text, job_desc_text])
    return cosine_similarity(vectors[0:1], vectors[1:2])[0][0]

def compute_weighted_score(resume_text, job_desc_text, skills_found, job_skills):
    # Skills match ratio
    skill_matches = len([skill for skill in skills_found if skill in job_skills])
    skill_ratio = skill_matches / len(job_skills) if job_skills else 0

    # Text similarity
    text_similarity = compute_text_similarity(resume_text, job_desc_text)

    # Weighted score
    final_score = 0.7 * skill_ratio + 0.3 * text_similarity
    return round(final_score, 2)
