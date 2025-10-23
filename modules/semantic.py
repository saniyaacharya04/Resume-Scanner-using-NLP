# modules/semantic.py
from sentence_transformers import SentenceTransformer, util

model = SentenceTransformer('all-MiniLM-L6-v2')

def compute_semantic_score(resume_text, job_desc_text):
    """
    Returns a semantic similarity score between 0 and 1
    """
    embeddings_resume = model.encode(resume_text, convert_to_tensor=True)
    embeddings_job = model.encode(job_desc_text, convert_to_tensor=True)
    
    cosine_score = util.cos_sim(embeddings_resume, embeddings_job)
    return float(cosine_score)
