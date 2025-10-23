import pandas as pd
import streamlit as st
import plotly.express as px

def generate_skill_gap_matrix(df, job_skills_list):
    """
    Generates a candidate vs job-skills matrix for skill matches (1=present, 0=absent)
    """
    if df.empty:
        st.info("No data available for skill gap analysis.")
        return

    candidates = df['Filename'].tolist()
    skills = [skill.lower() for skill in job_skills_list]
    matrix = pd.DataFrame(0, index=candidates, columns=skills)

    for idx, row in df.iterrows():
        candidate_skills = [s.strip().lower() for s in row['Skills Found'].split(",")]
        for skill in skills:
            if skill in candidate_skills:
                matrix.at[row['Filename'], skill] = 1

    return matrix

def show_skill_gap_heatmap(df, job_skills_list):
    """
    Displays an interactive heatmap of skill matches
    """
    skill_matrix = generate_skill_gap_matrix(df, job_skills_list)
    if skill_matrix is None or skill_matrix.empty:
        return

    fig = px.imshow(
        skill_matrix,
        text_auto=True,
        color_continuous_scale='Blues',
        labels=dict(x="Job Skills", y="Candidates", color="Match")
    )
    st.subheader("Candidate vs Job Skills Heatmap")
    st.plotly_chart(fig, use_container_width=True)
