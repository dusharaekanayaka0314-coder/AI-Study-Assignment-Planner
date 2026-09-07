import os
import google.generativeai as genai
from dotenv import load_dotenv
import streamlit as st

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-3.6-flash")

st.set_page_config(page_title="AI Study & Assignment Planner", layout="centered")

# =========================================================
# ENHANCED CUSTOM CSS
# =========================================================
st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"], p, span, label, div, h1, h2, h3, h4 {
    font-family: 'Poppins', sans-serif !important;
}

.stApp {
    background-color: #F8F9FA !important;
    color: #1E1E2F !important;
}

/* Base Card UI */
.card {
    background: #FFFFFF !important;
    padding: 28px;
    border-radius: 16px;
    box-shadow: 0 4px 20px rgba(108, 92, 231, 0.08);
    margin-bottom: 24px;
    border: 1px solid #EAE7FF;
}

.card h2 {
    color: #2D3748 !important;
    font-size: 1.35rem !important;
    font-weight: 700 !important;
}

/* Universal Input Override (Fixes Dark Backgrounds) */
div[data-baseweb="input"], 
div[data-baseweb="select"] > div, 
div[data-baseweb="textarea"], 
textarea, 
input {
    background-color: #FAFAFF !important;
    color: #1E1E2F !important;
    -webkit-text-fill-color: #1E1E2F !important;
    border-color: #E2E0F0 !important;
    border-radius: 10px !important;
}

/* Focus States */
div[data-baseweb="input"]:focus-within, 
div[data-baseweb="select"]:focus-within > div,
textarea:focus {
    border-color: #6C5CE7 !important;
    box-shadow: 0 0 0 3px rgba(108, 92, 231, 0.15) !important;
}

/* Dropdown Menu Popup Overlay Fix */
div[data-baseweb="popover"], 
div[data-baseweb="menu"], 
ul[role="listbox"], 
li[role="option"] {
    background-color: #FFFFFF !important;
    color: #1E1E2F !important;
}

li[role="option"]:hover {
    background-color: #F5F3FF !important;
}

/* Date Picker Fixes */
[data-testid="stDateInput"] {
    color-scheme: light !important;
}

div[data-baseweb="calendar"] {
    background-color: #FFFFFF !important;
}

/* Header Styling */
.main-header {
    text-align: center;
    padding: 36px 20px;
    background: linear-gradient(135deg, #6C5CE7 0%, #8E7CFF 100%);
    border-radius: 20px;
    margin-bottom: 28px;
    box-shadow: 0 10px 25px rgba(108, 92, 231, 0.25);
}

.main-header h1 {
    color: #FFFFFF !important;
    font-weight: 800;
    margin-top: 10px;
    margin-bottom: 6px;
}

.main-header p {
    color: #F0EDFF !important;
    font-size: 0.95rem;
    margin: 0;
}

/* Primary Button Styling */
div.stButton > button {
    background: linear-gradient(90deg, #6C5CE7 0%, #8E7CFF 100%) !important;
    color: #FFFFFF !important;
    font-weight: 600 !important;
    font-size: 1rem !important;
    border-radius: 12px !important;
    padding: 12px 24px !important;
    border: none !important;
    width: 100% !important;
    box-shadow: 0 4px 14px rgba(108, 92, 231, 0.3) !important;
    transition: all 0.2s ease !important;
}

div.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 18px rgba(108, 92, 231, 0.4) !important;
}

/* File Uploader Custom Styling */
[data-testid="stFileUploaderDropzone"] {
    border-radius: 12px !important;
    border: 2px dashed #C0B7FE !important;
    background: #FAF9FF !important;
}

[data-testid="stFileUploaderDropzone"] button {
    background-color: #6C5CE7 !important;
    color: #FFFFFF !important;
    border-radius: 8px !important;
    border: none !important;
}

/* Radio Group Custom Styling */
div[role="radiogroup"] label {
    background: #FAFAFF !important;
    padding: 10px 16px;
    border-radius: 10px;
    border: 1px solid #E2E0F0 !important;
    transition: all 0.2s ease;
}

div[role="radiogroup"] label:hover {
    border-color: #6C5CE7 !important;
    background: #F5F3FF !important;
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
    <img src="https://cdn-icons-png.flaticon.com/512/2436/2436874.png" width="80" style="margin-bottom: 5px;" />
    <h1>AI Study & Assignment Planner</h1>
    <p>Upload your syllabus or assignment and let AI create a personalized study plan for you.</p>
</div>
""",
    unsafe_allow_html=True,
)

# =========================================================
# SESSION STATE
# =========================================================
if "extracted_text" not in st.session_state:
    st.session_state.extracted_text = ""

# =========================================================
# BASIC DETAILS
# =========================================================
st.markdown(
    """
<div class="card">
<div style="display:flex; align-items:center; gap:12px; margin-bottom:16px;">
<img src="https://cdn-icons-png.flaticon.com/512/2921/2921222.png" width="32" />
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
    "Goal (e.g., Pass the exam, Score above 80%, Finish assignment)", height=100
)

st.markdown("</div>", unsafe_allow_html=True)

# =========================================================
# MATERIAL
# =========================================================
st.markdown(
    """
<div class="card">
<div style="display:flex; align-items:center; gap:12px; margin-bottom:16px;">
<img src="https://cdn-icons-png.flaticon.com/512/3143/3143460.png" width="32" />
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
            import PyPDF2

            reader = PyPDF2.PdfReader(uploaded_file)
            for page in reader.pages:
                text += page.extract_text() or ""
        elif uploaded_file.name.endswith(".docx"):
            import docx

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
            prompt = f"""You are a study planner AI. Based on the details and material below, respond using EXACTLY this format with markdown headers:

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
{st.session_state.extracted_text[:5000]}"""

            response = model.generate_content(prompt)

        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("Your Study Plan")
        st.markdown(response.text)
        st.markdown("</div>", unsafe_allow_html=True)
