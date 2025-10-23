# resume_scanner.py

import os
import glob
import fitz  # PyMuPDF for PDF text extraction
import docx2txt  # For DOCX
from sentence_transformers import SentenceTransformer, util
from config import (
    RAW_RESUME_DIR,
    EXTRACTED_TEXT_DIR,
    EMBEDDINGS_DIR,
    TRANSFORMER_MODEL,
    SIMILARITY_THRESHOLD,
    TOP_N_MATCHES,
    ensure_dirs
)
import pickle

# Ensure directories exist
ensure_dirs()

# Load embedding model
print("[INFO] Loading embedding model...")
model = SentenceTransformer(TRANSFORMER_MODEL)

# ---------------------------
# 1. Resume Text Extraction
# ---------------------------
def extract_text_from_pdf(pdf_path):
    text = ""
    doc = fitz.open(pdf_path)
    for page in doc:
        text += page.get_text()
    return text

def extract_text_from_docx(docx_path):
    return docx2txt.process(docx_path)

def extract_resume_text(resume_path):
    ext = resume_path.split('.')[-1].lower()
    if ext == "pdf":
        return extract_text_from_pdf(resume_path)
    elif ext == "docx":
        return extract_text_from_docx(resume_path)
    else:
        print(f"[WARN] Unsupported file type: {resume_path}")
        return ""

def process_all_resumes():
    extracted_texts = {}
    resume_files = glob.glob(os.path.join(RAW_RESUME_DIR, "*"))
    for resume_file in resume_files:
        text = extract_resume_text(resume_file)
        if text.strip():
            fname = os.path.basename(resume_file)
            extracted_texts[fname] = text
            # Save extracted text
            out_file = os.path.join(EXTRACTED_TEXT_DIR, fname + ".txt")
            with open(out_file, "w", encoding="utf-8") as f:
                f.write(text)
    return extracted_texts

# ---------------------------
# 2. Generate Resume Embeddings
# ---------------------------
def embed_resumes(extracted_texts):
    embeddings = {}
    for fname, text in extracted_texts.items():
        embeddings[fname] = model.encode(text, convert_to_tensor=True)
        # Save individual embeddings
        emb_file = os.path.join(EMBEDDINGS_DIR, fname + ".pkl")
        with open(emb_file, "wb") as f:
            pickle.dump(embeddings[fname], f)
    return embeddings

# ---------------------------
# 3. Match Resumes to Job Description
# ---------------------------
def match_resumes(job_description, resume_embeddings):
    job_emb = model.encode(job_description, convert_to_tensor=True)
    similarities = {}
    for fname, emb in resume_embeddings.items():
        sim_score = util.cos_sim(job_emb, emb).item()
        if sim_score >= SIMILARITY_THRESHOLD:
            similarities[fname] = sim_score
    # Sort by similarity descending
    sorted_matches = sorted(similarities.items(), key=lambda x: x[1], reverse=True)
    return sorted_matches[:TOP_N_MATCHES]

# ---------------------------
# 4. Main Pipeline
# ---------------------------
if __name__ == "__main__":
    print("[INFO] Extracting resumes...")
    extracted_texts = process_all_resumes()
    
    print(f"[INFO] Extracted {len(extracted_texts)} resumes. Generating embeddings...")
    resume_embeddings = embed_resumes(extracted_texts)
    
    # Example job description
    job_desc = """
    We are looking for a Python developer with experience in Machine Learning,
    NLP, and cloud deployment (AWS, Docker, Kubernetes). Excellent communication skills required.
    """
    
    print("[INFO] Matching resumes to job description...")
    top_matches = match_resumes(job_desc, resume_embeddings)
    
    print("[RESULT] Top Resume Matches:")
    for fname, score in top_matches:
        print(f"{fname} --> Similarity: {score:.2f}")
