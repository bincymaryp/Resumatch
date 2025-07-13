import streamlit as st
import sqlite3
import pandas as pd


def load_data():
    try:
        conn = sqlite3.connect("resumatch.db")
        df = pd.read_sql_query("SELECT * FROM resumes", conn)
        conn.close()
        return df
    except Exception as e:
        st.error(f"Error loading database: {e}")
        return pd.DataFrame()


st.set_page_config(page_title="RESUMATCH - Admin View", layout="wide")

st.markdown(
    """
    <div style="text-align:center; padding: 20px;">
        <h1 style="color:#2c3e50;">📊 RESUMATCH Admin Dashboard</h1>
        <h4 style="color:#555;">View Resume Logs & Stats</h4>
    </div>
    """,
    unsafe_allow_html=True
)

df = load_data()

if df.empty:
    st.warning("No resume data found yet.")
else:
    st.dataframe(df, use_container_width=True)

    # ---------- Optional Filters ----------
    st.sidebar.header("📌 Filters")
    roles = df["role"].unique().tolist()
    selected_roles = st.sidebar.multiselect("Filter by Job Role", roles, default=roles)

    if selected_roles:
        filtered_df = df[df["role"].isin(selected_roles)]
        st.subheader(f"📄 Filtered Results for Roles: {', '.join(selected_roles)}")
        st.dataframe(filtered_df, use_container_width=True)

        st.markdown("### 📈 Score Distribution")
        st.bar_chart(filtered_df["score"])

        st.markdown("### 📌 Skill Match vs Gap (Preview of Top 5)")
        st.write(filtered_df[["name", "matched_skills", "missing_skills"]].head())

    if st.button("🔄 Refresh"):
        st.experimental_rerun()
