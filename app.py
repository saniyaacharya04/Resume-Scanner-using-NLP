import os
import streamlit as st
import pandas as pd
import pdfkit
from modules import (
    parser, preprocessing, skill_extraction, ner_extraction, highlight,
    matching, ranking, dashboard, job_analysis, semantic, experience_level, report
)
from modules.report import generate_full_report

# ---------------- PDFKit Configuration ----------------
config = pdfkit.configuration(wkhtmltopdf="/usr/local/bin/wkhtmltopdf")

# ---------------- Page Config ----------------
st.set_page_config(page_title="Ultimate Resume Scanner - Live", layout="wide")
st.title("Ultimate Resume Scanner - Live Scoring")

# ---------------- Sidebar Filters ----------------
st.sidebar.header("Filters & Options")
min_score = st.sidebar.slider("Minimum Weighted Score", 0.0, 1.0, 0.0, 0.05)
experience_filter = st.sidebar.slider("Years of Experience", 0, 20, (0, 20))
education_options = ["B.Tech", "M.Tech", "PhD", "M.Sc", "B.Sc"]
selected_education = st.sidebar.multiselect("Education", education_options)

# ---------------- Job Description Inputs ----------------
job_desc = st.text_area("Paste Job Description Here", height=150)
job_skills_input = st.text_input("Enter key skills (comma-separated)")

uploaded_files = st.file_uploader(
    "Upload Resumes (PDF/DOCX)", accept_multiple_files=True, type=['pdf', 'docx'], key="resume_uploader"
)

# ---------------- Tabs ----------------
tabs = st.tabs(["Candidate List", "Resume Preview", "Analytics Dashboard", "Skill Gap Heatmap", "Export / Reports"])

# ---------------- Live Resume Processing ----------------
if uploaded_files and job_desc.strip() and job_skills_input.strip():
    job_desc_processed = preprocessing.preprocess_text(job_desc)
    job_skills_list = [skill.strip().lower() for skill in job_skills_input.split(",")]

    results = []

    for uploaded_file in uploaded_files:
        try:
            # Extract text
            resume_text = parser.extract_text(uploaded_file)
            resume_processed = preprocessing.preprocess_text(resume_text)

            # Extract details
            ner_info = ner_extraction.extract_ner_details(resume_text)
            skills_found = skill_extraction.extract_skills(resume_text)
            skills_dict = {skill.lower(): 1.0 if skill.lower() in job_skills_list else 0.5 for skill in skills_found}

            # Compute scores
            score = matching.compute_weighted_score(resume_processed, job_desc_processed, skills_found, job_skills_list)
            semantic_score = semantic.compute_semantic_score(resume_text, job_desc)
            final_score = round(0.7 * score + 0.3 * semantic_score, 2)

            # Experience
            experience = float(ner_info.get('experience') or 0)
            exp_level = experience_level.detect_experience_level(experience)

            # Highlighted resume
            highlighted_resume = highlight.highlight_skills_intensity(resume_text, skills_dict)

            # Append results
            results.append({
                "Filename": uploaded_file.name,
                "Score": final_score,
                "Skills Found": ", ".join(skills_found),
                "Highlighted Resume": highlighted_resume,
                "Experience Level": exp_level,
                **ner_info
            })

        except Exception as e:
            st.warning(f"Failed to process {uploaded_file.name}: {e}")

    # ---------------- DataFrame & Filtering ----------------
    df = pd.DataFrame(results)
    if not df.empty:
        df['experience'] = df['experience'].fillna(0).astype(float)
        df_filtered = df[
            (df['Score'] >= min_score) &
            (df['experience'] >= experience_filter[0]) &
            (df['experience'] <= experience_filter[1])
        ]
        if selected_education:
            df_filtered = df_filtered[
                df_filtered['education'].str.contains('|'.join(selected_education), case=False, na=False)
            ]

        df_ranked = df_filtered.sort_values(by='Score', ascending=False).reset_index(drop=True)

        # ---------------- Candidate List Tab ----------------
        with tabs[0]:
            st.subheader("Candidate List (Live Scoring)")
            st.dataframe(df_ranked.drop(columns=['Highlighted Resume']), width='stretch')

        # ---------------- Resume Preview Tab ----------------
        with tabs[1]:
            st.subheader("Resume Preview")
            if not df_ranked.empty:
                num_cols = min(len(df_ranked), 3)
                cols = st.columns(num_cols)
                for i, (idx, row) in enumerate(df_ranked.iterrows()):
                    with cols[i % num_cols]:
                        st.markdown(f"### {row['Filename']} (Score: {row['Score']})")
                        st.write(f"Skills: {row['Skills Found']}")
                        st.write(f"Education: {row['education']}, Experience: {row['experience']} yrs")
                        st.write(f"Level: {row['Experience Level']}")
                        st.write(f"Name: {row['name']}, Email: {row['email']}, Phone: {row['phone']}")
                        st.markdown(row['Highlighted Resume'], unsafe_allow_html=True)

        # ---------------- Analytics Dashboard Tab ----------------
        with tabs[2]:
            st.subheader("Analytics Dashboard")
            dashboard.show_dashboard(df_ranked)

        # ---------------- Skill Gap Heatmap Tab ----------------
        with tabs[3]:
            st.subheader("Candidate vs Job Skills Heatmap")
            job_analysis.show_skill_gap_heatmap(df_ranked, job_skills_list)

        # ---------------- Export / Reports Tab ----------------
        with tabs[4]:
            st.subheader("Export Results")

            # Create output directories
            highlight_dir = "data/highlighted_resumes"
            report_dir = "data/reports"
            os.makedirs(highlight_dir, exist_ok=True)
            os.makedirs(report_dir, exist_ok=True)

            # CSV export
            csv = df_ranked.drop(columns=['Highlighted Resume']).to_csv(index=False).encode('utf-8')
            st.download_button("Download Ranked Candidates as CSV", csv, "ranked_candidates.csv", "text/csv")

            # Export highlighted resumes
            for idx, row in df_ranked.iterrows():
                safe_name = row['Filename'].replace(" ", "_").replace(".pdf", "").replace(".docx", "")
                html_filename = os.path.join(highlight_dir, f"{safe_name}_highlighted.html")
                pdf_filename = os.path.join(highlight_dir, f"{safe_name}_highlighted.pdf")
                
                with open(html_filename, "w", encoding="utf-8") as f:
                    f.write(row['Highlighted Resume'])
                try:
                    pdfkit.from_file(html_filename, pdf_filename, configuration=config)
                except Exception:
                    st.warning(f"PDF export failed for {row['Filename']}. Ensure wkhtmltopdf is installed.")

            st.success("Highlighted resumes exported as HTML and PDF in 'data/highlighted_resumes/'")

            # Full PDF report
            if st.button("Generate Full Report"):
                try:
                    report_path = os.path.join(report_dir, "Full_Resume_Report.pdf")
                    generate_full_report(df_ranked, job_skills_list, report_name=report_path)
                    st.success(f"Full report generated: {report_path}")
                    st.download_button(
                        "Download Full Report PDF",
                        open(report_path, "rb").read(),
                        file_name="Full_Resume_Report.pdf"
                    )
                except Exception as e:
                    st.warning(f"Full report generation failed: {e}")

    else:
        st.warning("No resumes processed successfully yet.")
else:
    st.info("Upload resumes, enter job description & skills to see live scoring.")
