# Ultimate Resume Scanner - NLP [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)


A **live resume scanning and ranking tool** built using Python, Streamlit, and NLP. The app parses resumes (PDF/DOCX), extracts skills, experience, and education, ranks candidates against a job description, and generates highlighted resumes and full PDF reports.

---

## Features

* **Upload multiple resumes** (PDF / DOCX)
* **Job Description Input** with key skills
* **Live scoring** of candidates:

  * Weighted matching score
  * Semantic similarity score
* **Resume preview** with highlighted skills
* **Analytics Dashboard**:

  * Candidate skill distribution
  * Experience levels
  * Top skills
* **Skill Gap Heatmap**: Compare candidate skills vs job requirements
* **Export Options**:

  * Highlighted resumes in **HTML & PDF**
  * Full PDF report with all candidates and analytics
* Filters:

  * Minimum score
  * Years of experience
  * Education levels

---

## Project Structure

```
resume_scanner_nlp/
├── app.py                     # Main Streamlit app
├── config.py                  # Configuration (paths, API keys, etc.)
├── data/
│   ├── job_descriptions/      # Store sample or real job descriptions
│   ├── resumes/               # Upload raw resumes here
│   ├── highlighted_resumes/   # Generated highlighted resumes (HTML & PDF)
│   └── reports/               # Full reports PDFs
├── modules/                   # Core modules
│   ├── __init__.py
│   ├── dashboard.py
│   ├── experience_level.py
│   ├── highlight.py
│   ├── job_analysis.py
│   ├── matching.py
│   ├── ner_extraction.py
│   ├── parser.py
│   ├── preprocessing.py
│   ├── ranking.py
│   ├── report.py
│   ├── resume_scanner.py
│   ├── semantic.py
│   └── skill_extraction.py
├── README.md
├── requirements.txt
└── venv/                      # Virtual environment
```

---

## Installation

1. **Clone the repository**

```bash
git clone <your-repo-url>
cd resume_scanner_nlp
```

2. **Create a virtual environment**

```bash
python3 -m venv .venv
source .venv/bin/activate  # macOS/Linux
.venv\Scripts\activate     # Windows
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

4. **Install wkhtmltopdf** (required for PDF export)

* macOS (Homebrew):

```bash
brew install wkhtmltopdf
```

* Ubuntu/Debian:

```bash
sudo apt-get install wkhtmltopdf
```

---

## Usage

1. **Run Streamlit app**

```bash
streamlit run app.py
```

2. **Open in browser**

```
http://localhost:8502
```

3. **Steps in the app**:

* Paste the **job description**
* Enter **key skills** (comma-separated)
* Upload **resumes** (PDF or DOCX)
* Adjust filters in the sidebar (Score, Experience, Education)
* View candidate list, resume preview, analytics dashboard, and skill gap heatmap
* Export highlighted resumes and full PDF report

---

## Output Directories

* `data/highlighted_resumes/` → Highlighted HTML & PDF resumes
* `data/reports/` → Full PDF report with all candidates and analytics

---

## Example Data

* Place resumes in `data/resumes/`
* Place job descriptions in `data/job_descriptions/`

---

## Notes

* Make sure `wkhtmltopdf` is installed and path is correctly set in `app.py`:

```python
config = pdfkit.configuration(wkhtmltopdf="/usr/local/bin/wkhtmltopdf")
```

* Streamlit may give warnings about `use_container_width`. Use `width='stretch'` instead.
* HuggingFace tokenizers warning is normal when using multiprocessing; can be ignored.

---

## Dependencies

* Python ≥ 3.9
* Streamlit
* Pandas
* PDFKit
* PyPDF2
* python-docx
* spaCy (NER extraction)
* matplotlib / seaborn (for dashboards)
* HuggingFace Transformers (semantic similarity)
* scikit-learn

```bash
pip install -r requirements.txt
```

---

## License

MIT License – Open source
