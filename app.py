'''import streamlit as st
import requests

st.set_page_config(page_title="AI Job Assistant", layout="centered")

st.title("📄 AI Job Assistant")

# Upload resume
uploaded_file = st.file_uploader("Upload your Resume (PDF)", type=["pdf"])

# Job description input
job_description = st.text_area("Paste Job Description")

# Analyze button
if st.button("Analyze"):
    if uploaded_file and job_description:

        with st.spinner("Analyzing..."):

            files = {"file": uploaded_file}
            data = {"job_description": job_description}

            response = requests.post(
                "http://127.0.0.1:8001/match-job",
                files=files,
                data=data
            )

        result = response.json()

        if "result" in result:
            analysis = result["result"]

            st.subheader("📊 Match Score")
            st.write(analysis.get("match_score", "N/A"))

            st.subheader("❌ Missing Skills")
            for skill in analysis.get("missing_skills", []):
                st.write(f"- {skill}")

            st.subheader("✅ Strengths")
            for skill in analysis.get("strengths", []):
                st.write(f"- {skill}")

        else:
            st.error(result)

    else:
        st.warning("Please upload resume and enter job description") '''

import streamlit as st
import requests

st.set_page_config(page_title="AI Job Assistant", layout="centered")

st.title("📄 AI Job Assistant")

# Upload Resume
uploaded_file = st.file_uploader("Upload Resume (PDF)", type=["pdf"])

# Job Description
job_description = st.text_area("Job Description")

# Analyze Button
if st.button("Analyze"):

    if not uploaded_file or not job_description:
        st.warning("Please upload resume and enter job description")
        st.stop()

    with st.spinner("Analyzing..."):

        try:
            response = requests.post(
                "https://ai-jobassistant.onrender.com/match-job",
                files={"file": uploaded_file},
                data={"job_description": job_description}
            )
            result = response.json()

        except Exception as e:
            st.error(f"Connection error: {e}")
            st.stop()

    # 🧠 SAFE HANDLING
    if "result" not in result:
        st.error("Invalid response from backend")
        st.write(result)
        st.stop()

    analysis = result["result"]
    
    # st.write("🔍 DEBUG BACKEND RESPONSE:", analysis)

    # 🚨 If still string → show raw (no crash)
    if isinstance(analysis, str):
        st.error("Backend returned invalid format")
        st.write(analysis)
        st.stop()

    # ✅ CLEAN DISPLAY
    st.subheader("📊 Match Score")
    st.write(analysis.get("match_score", "N/A"))

    st.subheader("❌ Missing Skills")
    missing = analysis.get("missing_skills", [])
    if missing:
        for skill in missing:
            st.write(f"- {skill}")
    else:
        st.write("None")

    st.subheader("✅ Strengths")
    strengths = analysis.get("strengths", [])
    if strengths:
        for skill in strengths:
            st.write(f"- {skill}")
    else:
        st.write("None") 

