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

# =========================================================
# CUSTOM LIGHT-THEME STYLING
# =========================================================
st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700;800&display=swap');

/* Force font across application */
html, body, [class*="css"], p, span, label, div, h1, h2, h3, h4 {
    font-family: 'Poppins', sans-serif !important;
}

[data-testid="stAppViewContainer"],
[data-testid="stHeader"],
.main, body, .stApp {
    background-color: #FFFFFF !important;
    color: #1E1E2F !important;
}

label, .stMarkdown, p, span {
    color: #1E1E2F !important;
}

/* Universal Light Input Backgrounds */
div[data-baseweb="input"],
div[data-baseweb="base-input"],
div[data-baseweb="textarea"],
div[data-baseweb="select"],
div[data-baseweb="select"] > div {
    background-color: #FFFFFF !important;
    border: 1px solid #D8D2F5 !important;
    border-radius: 8px !important;
    color: #1E1E2F !important;
}

/* Force Text Fill Colors */
input, textarea {
    background-color: #FFFFFF !important;
    color: #1E1E2F !important;
    -webkit-text-fill-color: #1E1E2F !important;
}

/* Focus States */
div[data-baseweb="input"]:focus-within,
div[data-baseweb="textarea"]:focus-within,
div[data-baseweb="select"] > div:focus-within {
    border-color: #6C5CE7 !important;
    box-shadow: 0 0 0 1px #6C5CE7 !important;
}

input::placeholder, textarea::placeholder {
    color: #8E8A9F !important;
    -webkit-text-fill-color: #8E8A9F !important;
}

/* =========================================================
   FIX: DATE INPUT FIELD (DEADLINE)
   ========================================================= */
[data-testid="stDateInput"] {
    color-scheme: light !important;
}

[data-testid="stDateInput"] div[data-baseweb="input"] {
    background-color: #FFFFFF !important;
}

[data-testid="stDateInput"] input {
    background-color: #FFFFFF !important;
    color: #1E1E2F !important;
    -webkit-text-fill-color: #1E1E2F !important;
}

[data-testid="stDateInput"] svg {
    fill: #6C5CE7 !important;
}

div[data-baseweb="calendar"] {
    background-color: #FFFFFF !important;
    color: #1E1E2F !important;
    color-scheme: light !important;
}

div[data-baseweb="calendar"] * {
    color: #1E1E2F !important;
}

/* =========================================================
   FIX: SELECTBOX DROPDOWN ARROW & CONTAINER
   ========================================================= */
[data-testid="stSelectbox"] div[data-baseweb="select"] {
    background-color: #FFFFFF !important;
}

[data-testid="stSelectbox"] div[role="button"] {
    background-color: #FFFFFF !important;
}

/* Removes the dark background behind the arrow icon */
[data-testid="stSelectbox"] [data-baseweb="icon"] {
    background-color: #F5F3FF !important;
    border-top-right-radius: 8px !important;
    border-bottom-right-radius: 8px !important;
}

[data-testid="stSelectbox"] svg {
    fill: #6C5CE7 !important;
}

div[data-baseweb="popover"],
div[data-baseweb="menu"],
ul[role="listbox"] {
    background-color: #FFFFFF !important;
    border: 1px solid #E0D9FF !important;
    border-radius: 8px !important;
}

li[role="option"] {
    background-color: #FFFFFF !important;
    color: #1E1E2F !important;
}

li[role="option"]:hover {
    background-color: #F5F3FF !important;
    color: #6C5CE7 !important;
}

/* =========================================================
   NUMBER INPUT BOX & BUTTONS
   ========================================================= */
[data-testid="stNumberInput"] > div {
    background-color: #FFFFFF !important;
    border: 1px solid #D8D2F5 !important;
    border-radius: 8px !important;
}

[data-testid="stNumberInput"] input {
    background-color: #FFFFFF !important;
    color: #1E1E2F !important;
    -webkit-text-fill-color: #1E1E2F !important;
}

[data-testid="stNumberInput"] button {
    background-color: #F5F3FF !important;
    color: #1E1E2F !important;
    border: none !important;
    border-left: 1px solid #E0D9FF !important;
}

[data-testid="stNumberInput"] button:hover {
    background-color: #EDE7FF !important;
    color: #6C5CE7 !important;
}

/* =========================================================
   FILE UPLOAD ZONE
   ========================================================= */
[data-testid="stFileUploader"] {
    background-color: #FFFFFF !important;
    color: #1E1E2F !important;
}

[data-testid="stFileUploaderDropzone"] {
    background-color: #FAF9FF !important;
    border: 2px dashed #A29BFE !important;
    border-radius: 14px !important;
    padding: 12px 16px !important;
}

[data-testid="stFileUploaderDropzone"] * {
    color: #1E1E2F !important;
}

[data-testid="stFileUploaderDropzone"] button {
    background-color: #6C5CE7 !important;
    color: #FFFFFF !important;
    border: none !important;
    border-radius: 8px !important;
}

[data-testid="stFileUploaderDropzone"] button:hover {
    background-color: #5B4BD6 !important;
}

/* =========================================================
   RADIO BUTTONS
   ========================================================= */
div[role="radiogroup"] {
    display: flex;
    flex-direction: column;
    gap: 12px;
}

div[role="radiogroup"] label {
    background-color: #F5F3FF !important;
    padding: 12px 18px;
    border-radius: 12px;
    border: 1px solid #E0D9FF !important;
    width: 100%;
}

/* =========================================================
   LAYOUT CARDS & HEADER
   ========================================================= */
.main-header {
    text-align: center;
    padding: 30px 20px;
    background: linear-gradient(135deg, #6C5CE7 0%, #A29BFE 100%);
    border-radius: 20px;
    margin-bottom: 25px;
    box-shadow: 0 8px 24px rgba(108, 92, 231, 0.35);
}

.main-header h1, .main-header p {
    color: #FFFFFF !important;
}

.card {
    background: #FFFFFF !important;
    padding: 24px;
    border-radius: 18px;
    box-shadow: 0 6px 18px rgba(108, 92, 231, 0.12);
    margin-bottom: 22px;
    border: 1px solid #EDE9FE;
}

.card h2 {
    color: #6C5CE7 !important;
}

div.stButton > button {
    background: linear-gradient(90deg, #6C5CE7, #A29BFE) !important;
    color: #FFFFFF !important;
    font-weight: 700;
    font-size: 1.05rem;
    border-radius: 12px;
    padding: 12px 24px;
    border: none;
    width: 100%;
    box-shadow: 0 4px 14px rgba(108, 92, 231, 0.4);
    transition: all 0.2s ease-in-out;
}

div.stButton > button:hover {
    background: linear-gradient(90deg, #5B4BD6, #8E86F5) !important;
    transform: translateY(-2px);
    box-shadow: 0 6px 18px rgba(108, 92, 231, 0.5);
}

details {
    border-radius: 12px !important;
    background: #FFFFFF !important;
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
    <img src="https://cdn-icons-png.flaticon.com/512/2436/2436874.png" width="90" style="margin-bottom: 10px;" />
    <h1>AI Study & Assignment Planner</h1>
    <p>Upload your syllabus or assignment and let AI create a personalized study plan for you.</p>
</div>
""",
    unsafe_allow_html=True,
)

# Session State Initializer
if "extracted_text" not in st.session_state:
    st.session_state.extracted_text = ""

# =========================================================
# BASIC DETAILS CARD
# =========================================================
st.markdown(
    """
<div class="card">
<div style="display:flex; align-items:center; gap:12px; margin-bottom:10px;">
    <img src="https://cdn-icons-png.flaticon.com/512/2921/2921222.png" width="36" />
    <h2 style="margin:0;">Basic Details</h2>
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

st.markdown("</div>", unsafe_allow_html=True)

# =========================================================
# SYLLABUS / ASSIGNMENT MATERIAL CARD
# =========================================================
st.markdown(
    """
<div class="card">
<div style="display:flex; align-items:center; gap:12px; margin-bottom:10px;">
    <img src="https://cdn-icons-png.flaticon.com/512/3143/3143460.png" width="36" />
    <h2 style="margin:0;">Syllabus / Assignment Material</h2>
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

st.markdown("</div>", unsafe_allow_html=True)

# =========================================================
# GENERATE STUDY PLAN
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

        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("Your Study Plan")
        st.markdown(response.text)
        st.markdown("</div>", unsafe_allow_html=True)
