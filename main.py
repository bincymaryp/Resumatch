
import streamlit as st

st.set_page_config(page_title="Resume Analyzer", layout="centered")
st.markdown("""
    <style>
        .main-title {
            font-size: 3rem;
            font-weight: bold;
            color: #1f77b4;
        }
        .subtitle {
            font-size: 1.2rem;
            color: #444;
        }
        .role-box {
            background-color: #f1f1f1;
            padding: 1.5rem;
            border-radius: 12px;
            text-align: center;
            box-shadow: 0 0 10px rgba(0,0,0,0.05);
        }
        .stButton button {
            font-size: 1rem;
            border-radius: 8px;
            padding: 0.6rem 1.2rem;
        }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1 class='main-title'>Welcome to Resume Analyzer AI</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>Choose how you'd like to proceed:</p>", unsafe_allow_html=True)
st.markdown("")

col1, col2 = st.columns(2)

with col1:
    st.markdown("<div class='role-box'>", unsafe_allow_html=True)
    st.subheader("🧑‍💼 I'm an Employer")
    st.write("Analyze a single candidate's resume for skill gaps, course suggestions, and job readiness score.")
    if st.button("Go to Employer Dashboard"):
        st.switch_page("pages/1_Employer.py")
    st.markdown("</div>", unsafe_allow_html=True)

with col2:
    st.markdown("<div class='role-box'>", unsafe_allow_html=True)
    st.subheader("🧑‍💻 I'm a Recruiter")
    st.write("Upload multiple resumes, automatically rank candidates, and shortlist top fits.")
    if st.button("Go to Recruiter Dashboard"):
        st.switch_page("pages/2_Recruiter.py")
    st.markdown("</div>", unsafe_allow_html=True)
