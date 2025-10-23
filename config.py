# config.py

import os

# --------------------------
# General Project Settings
# --------------------------
PROJECT_NAME = "Resume Scanner NLP"
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# --------------------------
# Data Paths
# --------------------------
DATA_DIR = os.path.join(BASE_DIR, "data")
RAW_RESUME_DIR = os.path.join(DATA_DIR, "resumes_raw")  # folder containing input resumes (pdf/docx)
PROCESSED_RESUME_DIR = os.path.join(DATA_DIR, "resumes_processed")
EXTRACTED_TEXT_DIR = os.path.join(DATA_DIR, "text_extracted")
EMBEDDINGS_DIR = os.path.join(DATA_DIR, "embeddings")  # store vectorized resume embeddings

# --------------------------
# NLP / Model Settings
# --------------------------
# spaCy pre-trained model for NLP tasks
SPACY_MODEL = "en_core_web_sm"

# Transformer-based model (optional, for semantic embeddings)
TRANSFORMER_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

# Keywords for skill extraction / parsing
SKILLS_KEYWORDS = [
    "Python", "Java", "C++", "Machine Learning", "Deep Learning",
    "NLP", "Data Analysis", "SQL", "Excel", "Communication",
    "Leadership", "Project Management", "AWS", "Docker", "Kubernetes"
]

# Minimum confidence threshold for entity recognition
ENTITY_CONFIDENCE_THRESHOLD = 0.85

# --------------------------
# Resume Parsing Config
# --------------------------
ALLOWED_EXTENSIONS = ["pdf", "docx"]  # allowed file formats
MAX_RESUME_FILE_SIZE_MB = 10  # max allowed file size

# --------------------------
# Embedding / Vectorization Config
# --------------------------
EMBEDDING_DIM = 384  # dimension for MiniLM embeddings
SIMILARITY_THRESHOLD = 0.75  # cosine similarity threshold for matching resumes to jobs

# --------------------------
# Evaluation / Metrics
# --------------------------
EVAL_METRICS = ["precision", "recall", "f1-score"]  # evaluation metrics for matching or classification
TOP_N_MATCHES = 5  # number of top resumes to return per job description

# --------------------------
# Logging Settings
# --------------------------
LOG_DIR = os.path.join(BASE_DIR, "logs")
LOG_FILE = os.path.join(LOG_DIR, "app.log")
LOG_LEVEL = "INFO"

# --------------------------
# Database / Storage Config (Optional)
# --------------------------
DB_DIR = os.path.join(BASE_DIR, "database")
DB_URI = "sqlite:///" + os.path.join(DB_DIR, "resumes.db")

# --------------------------
# Utility Functions
# --------------------------
def ensure_dirs():
    """Ensure all necessary directories exist."""
    for folder in [
        DATA_DIR, RAW_RESUME_DIR, PROCESSED_RESUME_DIR,
        EXTRACTED_TEXT_DIR, EMBEDDINGS_DIR, LOG_DIR, DB_DIR
    ]:
        if not os.path.exists(folder):
            os.makedirs(folder)

# Call at import to auto-create folders
ensure_dirs()
