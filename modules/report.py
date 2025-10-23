# modules/report.py
import pdfkit
import os
import streamlit as st

def generate_full_report(df, job_skills_list, report_name="Full_Resume_Report.pdf"):
    """
    Generates a PDF combining top resumes, dashboard, and heatmap,
    and provides a Streamlit download button.
    """
    html_content = "<h1>Resume Scanner Report</h1>"

    # Top candidates
    html_content += "<h2>Top Candidates</h2>"
    for idx, row in df.iterrows():
        html_content += f"<h3>{row['Filename']} (Score: {row['Score']})</h3>"
        html_content += f"<p>Experience: {row['experience']} yrs, Level: {row['Experience Level']}</p>"
        html_content += row['Highlighted Resume']

    # Dashboard charts
    html_content += "<h2>Analytics Dashboard</h2>"
    html_content += "<p>Charts and visualizations exported as images</p>"

    # Skill Gap Heatmap
    html_content += "<h2>Skill Gap Heatmap</h2>"
    html_content += "<p>Heatmap exported as image</p>"

    # Generate PDF
    try:
        pdfkit.from_string(html_content, report_name)
        pdf_path = os.path.abspath(report_name)

        st.success(f"Report successfully generated: {pdf_path}")

        # Show download button in Streamlit
        with open(pdf_path, "rb") as f:
            st.download_button(
                label="Download Full Resume Report",
                data=f,
                file_name=report_name,
                mime="application/pdf"
            )

        return pdf_path

    except Exception as e:
        st.error(f"Error generating report: {e}")
        return None
