''' import streamlit as st
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
        st.write("None") '''

import streamlit as st
import requests

# 🔥 Page config (must be first)
st.set_page_config(page_title="AI Job Assistant", layout="centered")

# 🎯 Minimal Styling
st.markdown("""
    <style>
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 700px;
    }
    .section {
        margin-top: 2rem;
        margin-bottom: 1.5rem;
    }
    </style>
""", unsafe_allow_html=True)

# 🔥 HEADER
st.markdown("## 🤖 AI Job Assistant")
st.caption("Analyze your resume against job descriptions")

st.divider()

# 📂 Upload Section
st.markdown("### 📄 Upload Resume")
uploaded_file = st.file_uploader("", type=["pdf"])

# 📝 Job Description Section
st.markdown("### 🧾 Job Description")
job_description = st.text_area("", height=140, placeholder="Paste job description here...")

st.divider()

# 🚀 Analyze Button
if st.button("Analyze Resume"):

    if not uploaded_file or not job_description:
        st.warning("Please upload resume and enter job description")
        st.stop()

    with st.spinner("Analyzing your resume..."):

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

    # 🚨 Safety
    if isinstance(analysis, str):
        st.error("Backend returned invalid format")
        st.write(analysis)
        st.stop()

    st.divider()

    # 📊 MATCH SCORE
    st.markdown("### 📊 Match Score")
    score = int(analysis.get("match_score", 0))

    st.progress(score / 100)
    st.markdown(f"#### {score}%")

    # ❌ Missing Skills
    st.markdown('<div class="section">', unsafe_allow_html=True)
    st.markdown("### ❌ Missing Skills")

    missing = analysis.get("missing_skills", [])
    if missing:
        for skill in missing:
            st.markdown(f"- {skill}")
    else:
        st.markdown("No major missing skills")

    st.markdown('</div>', unsafe_allow_html=True)

    # ✅ Strengths
    st.markdown("### ✅ Strengths")

    strengths = analysis.get("strengths", [])
    if strengths:
        for skill in strengths:
            st.markdown(f"- {skill}")
    else:
        st.markdown("No strong strengths identified")

    st.divider()

    # 💡 Insight (clean + subtle)
    if score >= 80:
        st.success("Strong match for this role")
    elif score >= 60:
        st.info("Moderate match — improvement possible")
    else:
        st.warning("Low match — consider skill improvements")