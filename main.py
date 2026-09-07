import os
import docx
from dotenv import load_dotenv
import google.generativeai as genai
import PyPDF2
import streamlit as st

# =========================================================
# CONFIG & INITIALIZATION
# =========================================================
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-3.6-flash")

st.set_page_config(
    page_title="AI Study & Assignment Planner",
    layout="centered"
)

# Custom CSS for Header, Cards, and Layout without overriding input internals
st.markdown(
    """
<style>
/* Clean Background for App */
.stApp {
    background-color: #FFFFFF;
}

/* Custom Header */
.main-header {
    text-align: center;
    padding: 30px 20px;
    background: linear-gradient(135deg, #6C5CE7 0%, #A29BFE 100%);
    border-radius: 16px;
    margin-bottom: 25px;
    color: #FFFFFF;
}

.main-header h1 {
    color: #FFFFFF !important;
    margin-bottom: 8px;
}

.main-header p {
    color: #F0EDFF !important;
    font-size: 1.05rem;
}

/* Card Section Containers */
.card-header {
    display: flex;
    align-items: center;
    gap: 12px;
    margin-bottom: 15px;
}

.card-header h3 {
    margin: 0;
    color: #6C5CE7;
}

/* Generate Button Styling */
div.stButton > button {
    background: linear-gradient(90deg, #6C5CE7, #A29BFE) !important;
    color: #FFFFFF !important;
    font-weight: 700;
    font-size: 1.1rem;
    border-radius: 10px;
    padding: 12px 24px;
    border: none;
    width: 100%;
    margin-top: 10px;
}

div.stButton > button:hover {
    background: linear-gradient(90deg, #5B4BD6, #8E86F5) !important;
}
</style>
""",
    unsafe_allow_html=True,
)

# =========================================================
# HEADER
# =========================================================
st.markdown(
    """
<div class="main-header">
    <img src="https://cdn-icons-png.flaticon.com/512/2436/2436874.png" width="80" style="margin-bottom: 10px;" />
    <h1>AI Study & Assignment Planner</h1>
    <p>Upload your syllabus or assignment and let AI create a personalized study plan for you.</p>
</div>
""",
    unsafe_allow_html=True,
)

if "extracted_text" not in st.session_state:
    st.session_state.extracted_text = ""

# =========================================================
# BASIC DETAILS SECTION
# =========================================================
st.markdown(
    """
<div class="card-header">
    <img src="https://cdn-icons-png.flaticon.com/512/2921/2921222.png" width="32" />
    <h3>Basic Details</h3>
</div>
""",
    unsafe_allow_html=True,
)

col1, col2 = st.columns(2)

with col1:
    subject = st.text_input("Subject Name")
    study_hours = st.number_input(
        "Study Hours per Day", min_value=1, max_value=16, value=2
    )

with col2:
    deadline = st.date_input("Exam / Assignment Deadline")
    level = st.selectbox(
        "Current Level", ["Beginner", "Intermediate", "Advanced"]
    )

goal = st.text_area(
    "Goal (e.g., Pass the exam, Score above 80%, Finish assignment)"
)

st.divider()

# =========================================================
# SYLLABUS / ASSIGNMENT MATERIAL SECTION
# =========================================================
st.markdown(
    """
<div class="card-header">
    <img src="https://cdn-icons-png.flaticon.com/512/3143/3143460.png" width="32" />
    <h3>Syllabus / Assignment Material</h3>
</div>
""",
    unsafe_allow_html=True,
)

input_method = st.radio(
    "Select Input Method:", ["Upload File (PDF/DOCX/TXT)", "Paste Text"]
)

if input_method == "Upload File (PDF/DOCX/TXT)":
    uploaded_file = st.file_uploader(
        "Upload a PDF, DOCX, or TXT file", type=["pdf", "docx", "txt"]
    )

    if uploaded_file is not None:
        text = ""

        if uploaded_file.name.endswith(".pdf"):
            reader = PyPDF2.PdfReader(uploaded_file)
            for page in reader.pages:
                text += page.extract_text() or ""

        elif uploaded_file.name.endswith(".docx"):
            doc = docx.Document(uploaded_file)
            for para in doc.paragraphs:
                text += para.text + "\n"
            for table in doc.tables:
                for row in table.rows:
                    for cell in row.cells:
                        text += cell.text + " "
                    text += "\n"

        elif uploaded_file.name.endswith(".txt"):
            text = uploaded_file.read().decode("utf-8")

        st.session_state.extracted_text = text

        if text.strip():
            st.success("File processed successfully.")
            with st.expander("View Extracted Text"):
                st.write(
                    text[:2000] + ("..." if len(text) > 2000 else "")
                )
        else:
            st.warning(
                "No text could be extracted from this file. Try another file."
            )
else:
    pasted = st.text_area(
        "Paste your syllabus/assignment text here", height=200
    )
    st.session_state.extracted_text = pasted

st.divider()

# =========================================================
# GENERATE PLAN
# =========================================================
if st.button("Generate Study Plan"):
    if not st.session_state.extracted_text.strip():
        st.error("Please upload a file or paste text first.")
    else:
        with st.spinner("Gemini is analyzing your material..."):
            prompt = f"""
You are a study planner AI.

Based on the details and material below, respond using EXACTLY this format with markdown headers:

## Important Topics
(bullet list)

## High-Priority Topics
(bullet list)

## Study Plan / Timetable
(day-by-day breakdown as a bullet list or table)

## What to Focus On
(2-3 sentences)

Subject: {subject}
Deadline: {deadline}
Study Hours per Day: {study_hours}
Current Level: {level}
Goal: {goal}

Material:
{st.session_state.extracted_text[:5000]}
"""
            response = model.generate_content(prompt)

        st.subheader("Your Study Plan")
        st.markdown(response.text)
