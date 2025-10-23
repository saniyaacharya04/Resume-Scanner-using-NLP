import plotly.express as px
import pandas as pd
import streamlit as st

def show_dashboard(df):
    if df.empty:
        st.info("No data available for dashboard.")
        return

    # ----- Skills Distribution -----
    st.subheader("Skills Distribution")
    all_skills = []
    for s in df['Skills Found']:
        all_skills.extend([skill.strip() for skill in s.split(",") if skill])
    skill_counts = pd.Series(all_skills).value_counts().reset_index()
    skill_counts.columns = ['Skill', 'Count']
    fig1 = px.bar(skill_counts, x='Skill', y='Count', title="Skills Distribution Across Candidates")
    st.plotly_chart(fig1, use_container_width=True)

    # ----- Experience Distribution -----
    st.subheader("Experience Distribution")
    fig2 = px.histogram(df, x='experience', nbins=20, title="Experience Distribution")
    st.plotly_chart(fig2, use_container_width=True)

    # ----- Weighted Score Distribution -----
    st.subheader("Weighted Score Distribution")
    fig3 = px.histogram(df, x='Score', nbins=20, title="Weighted Score Distribution")
    st.plotly_chart(fig3, use_container_width=True)
