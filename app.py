import streamlit as st
from parser import extract_text_from_pdf
from skill_analysis import analyze_skills
from courses import get_courses_for_skills
from scorer import calculate_resume_score
from tips import get_resume_tips
import sqlite3
import json
import pandas as pd

# ------------------- Load Roles ----------------------
@st.cache_data
def load_roles():
    try:
        with open("assets/skills.json", "r", encoding="utf-8") as f:
            skills_data = json.load(f)
        return list(skills_data.keys())
    except:
        st.error("❌ Could not load roles.")
        return []

# ------------------- Database Setup ----------------------

def init_db():
    conn = sqlite3.connect("resumatch.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS resumes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            role TEXT,
            score INTEGER,
            matched_skills TEXT,
            missing_skills TEXT
        )
    """)
    conn.commit()
    conn.close()

def save_resume_to_db(name, role, score, matched, missing):
    conn = sqlite3.connect("resumatch.db")
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO resumes (name, role, score, matched_skills, missing_skills)
        VALUES (?, ?, ?, ?, ?)
    """, (name, role, score, ', '.join(matched), ', '.join(missing)))
    conn.commit()
    conn.close()

def show_database_table():
    conn = sqlite3.connect("resumatch.db")
    df = pd.read_sql_query("SELECT * FROM resumes", conn)
    conn.close()

    st.subheader("📋 All Resume Entries in Database")
    st.dataframe(df)

# ------------------- UI Components ----------------------

def show_resume_tips(resume_text):
    tips = get_resume_tips(resume_text)
    st.subheader("💡 Resume Tips")
    if tips:
        for tip in tips:
            st.info(f"👉 {tip}")
    else:
        st.success("Your resume looks solid! 💪")

def show_courses(missing):
    st.subheader("📚 Recommended Courses")
    courses = get_courses_for_skills(missing)
    cols = st.columns(2)
    i = 0
    for skill, link in courses.items():
        with cols[i % 2]:
            if link:
                st.markdown(f"**{skill.title()}**")
                st.video(link)
            else:
                st.info(f"No video available for **{skill}**")
        i += 1

def show_score(score):
    st.subheader("📈 Resume Score")
    st.success(f"Score: **{score}/100**")

    st.subheader("🎯 Job Readiness Meter")
    if score >= 80:
        label, color, emoji = "Excellent", "#28a745", "🚀"
    elif score >= 60:
        label, color, emoji = "Good", "#007bff", "👍"
    else:
        label, color, emoji = "Needs Improvement", "#ffc107", "⚠️"

    st.markdown(
        f"""
        <div style='padding: 1rem; border-radius: 10px; background-color: {color}; color: white; font-size: 18px;'>
            <strong>{emoji} {label}</strong><br>Resume Score: {score}/100
        </div>
        """,
        unsafe_allow_html=True
    )
    st.progress(score)

# ------------------- Job Seeker Section ----------------------

def job_seeker_section():
    roles = load_roles()
    selected_role = st.sidebar.selectbox("🎯 Select Job Role", roles)
    uploaded_file = st.sidebar.file_uploader("📤 Upload Your Resume", type=["pdf"])

    if uploaded_file and selected_role:
        resume_text = extract_text_from_pdf(uploaded_file)

        if resume_text.strip() == "":
            st.error("❌ Resume text could not be extracted.")
            return

        st.success("✅ Resume uploaded and processed!")
        st.subheader("📊 Skill Gap Analysis")
        matched, missing = analyze_skills(resume_text, selected_role)

        st.markdown(f"✅ **Matched Skills ({len(matched)})**")
        for skill in matched:
            st.success(f"✔️ {skill.title()}")

        st.markdown(f"❌ **Missing Skills ({len(missing)})**")
        for skill in missing:
            st.warning(f"⚠️ {skill.title()}")

        score = calculate_resume_score(matched, len(matched) + len(missing))
        show_score(score)
        show_resume_tips(resume_text)
        if missing:
            show_courses(missing)

        # Save to DB
        name = uploaded_file.name.replace(".pdf", "")
        save_resume_to_db(name, selected_role, score, matched, missing)

# ------------------- Recruiter Section ----------------------

def recruiter_section():
    roles = load_roles()
    selected_role = st.sidebar.selectbox("🎯 Target Job Role", roles)
    uploaded_files = st.sidebar.file_uploader("📤 Upload Multiple Resumes", type=["pdf"], accept_multiple_files=True)

    if uploaded_files and selected_role:
        for file in uploaded_files:
            st.divider()
            st.markdown(f"### 📄 {file.name}")
            resume_text = extract_text_from_pdf(file)

            if resume_text.strip() == "":
                st.error("❌ Could not extract text.")
                continue

            matched, missing = analyze_skills(resume_text, selected_role)

            st.markdown(f"✅ **Matched Skills ({len(matched)})**")
            st.success(", ".join(matched) if matched else "None")

            st.markdown(f"❌ **Missing Skills ({len(missing)})**")
            st.warning(", ".join(missing) if missing else "None")

            score = calculate_resume_score(matched, len(matched) + len(missing))
            show_score(score)

            # Save to DB
            name = file.name.replace(".pdf", "")
            save_resume_to_db(name, selected_role, score, matched, missing)

# ------------------- Main App ----------------------

def main():
    init_db()
    st.set_page_config(page_title="RESUMATCH", layout="wide")

    st.markdown(
        """
        <div style="text-align:center; padding: 20px;">
            <h1 style="color:#2c3e50;">🎯 RESUMATCH</h1>
            <h4 style="color:#555;">Analyze Resumes Instantly for Job Roles</h4>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.sidebar.title("User Type")
    user_type = st.sidebar.radio("Who are you?", ["👤 Job Seeker", "🏢 Recruiter", "🛠️ Admin"])

    if user_type == "👤 Job Seeker":
        job_seeker_section()
    elif user_type == "🏢 Recruiter":
        recruiter_section()
    else:
        if st.sidebar.checkbox("👀 View Resume Database"):
            show_database_table()

if __name__ == "__main__":
    main()
