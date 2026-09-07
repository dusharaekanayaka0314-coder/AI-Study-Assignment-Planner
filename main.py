from dotenv import load_dotenv
import os
import streamlit as st

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

import google.generativeai as genai
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-3.6-flash")

st.set_page_config(page_title="AI Study & Assignment Planner", layout="centered")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"], p, span, label, div, h1, h2, h3, h4 {
    font-family: 'Poppins', sans-serif;
}

[data-testid="stAppViewContainer"], [data-testid="stHeader"], .main, body, .stApp {
    background-color: #FFFFFF !important;
    color: #1E1E2F !important;
}

label, .stMarkdown, p, span {
    color: #1E1E2F !important;
}

input, textarea, select,
div[data-baseweb="input"] input,
div[data-baseweb="textarea"] textarea,
div[data-baseweb="select"] div,
div[data-baseweb="datepicker"] input,
[data-testid="stNumberInput"] input,
[data-testid="stTextInput"] input,
[data-testid="stDateInput"] input {
    background-color: #FFFFFF !important;
    color: #1E1E2F !important;
    border: 1px solid #D8D2F5 !important;
}

[data-testid="stNumberInput"] button {
    background-color: #F5F3FF !important;
    color: #1E1E2F !important;
}

ul[data-baseweb="menu"], li[role="option"] {
    background-color: #FFFFFF !important;
    color: #1E1E2F !important;
}

/* ---- FIX: Date input inner wrapper (real container is div[data-baseweb="input"], not "datepicker") ---- */
[data-testid="stDateInput"] div[data-baseweb="input"] {
    background-color: #FFFFFF !important;
}
[data-testid="stDateInput"] div[data-baseweb="input"] > div {
    background-color: #FFFFFF !important;
    color: #1E1E2F !important;
}
[data-testid="stDateInput"] input {
    background-color: #FFFFFF !important;
    color: #1E1E2F !important;
}

/* ---- FIX: Calendar popup when date input is clicked ---- */
div[data-baseweb="calendar"] {
    background-color: #FFFFFF !important;
    color: #1E1E2F !important;
}
div[data-baseweb="calendar"] * {
    color: #1E1E2F !important;
}

/* ---- FIX: File uploader "Browse files" button ---- */
[data-testid="stFileUploaderDropzone"] button,
[data-testid="stBaseButton-secondary"] {
    background-color: #6C5CE7 !important;
    color: #FFFFFF !important;
    border: none !important;
    border-radius: 8px !important;
}
[data-testid="stFileUploaderDropzone"] button:hover,
[data-testid="stBaseButton-secondary"]:hover {
    background-color: #5B4BD6 !important;
    color: #FFFFFF !important;
}

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

/* ---- DATE INPUT FIX ---- */

[data-testid="stDateInput"] {
    color-scheme: light !important;
}

[data-testid="stDateInput"] div[data-baseweb="input"] {
    background-color: #FFFFFF !important;
    color: #1E1E2F !important;
    border: 1px solid #D8D2F5 !important;
    border-radius: 8px !important;
}

[data-testid="stDateInput"] div[data-baseweb="input"] > div {
    background-color: #FFFFFF !important;
    color: #1E1E2F !important;
}

[data-testid="stDateInput"] input {
    background-color: #FFFFFF !important;
    color: #1E1E2F !important;
    -webkit-text-fill-color: #1E1E2F !important;
    color-scheme: light !important;
}

/* Calendar icon */
[data-testid="stDateInput"] svg {
    color: #6C5CE7 !important;
    fill: #6C5CE7 !important;
}

/* Calendar popup */
div[data-baseweb="calendar"] {
    background-color: #FFFFFF !important;
    color: #1E1E2F !important;
    color-scheme: light !important;
}

div[data-baseweb="calendar"] * {
    color: #1E1E2F !important;
}

div[role="radiogroup"] {
    display: flex;
    flex-direction: column;
    gap: 12px;
}

div[role="radiogroup"] label {
    background: #F5F3FF !important;
    padding: 12px 18px;
    border-radius: 12px;
    border: 1px solid #E0D9FF !important;
    width: 100%;
}

div[data-testid="stAlert"] {
    border-radius: 12px;
}

details {
    border-radius: 12px !important;
    background: #FFFFFF !important;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="main-header">
    <img src="https://cdn-icons-png.flaticon.com/512/2436/2436874.png" width="90" style="margin-bottom: 10px;" />
    <h1>AI Study & Assignment Planner</h1>
    <p>Upload your syllabus or assignment and let AI create a personalized study plan for you.</p>
</div>
""", unsafe_allow_html=True)

if "extracted_text" not in st.session_state:
    st.session_state.extracted_text = ""

st.markdown("""
<div class="card">
<div style="display:flex; align-items:center; gap:12px; margin-bottom:10px;">
<img src="https://cdn-icons-png.flaticon.com/512/2921/2921222.png" width="36" />
<h2 style="margin:0;">Basic Details</h2>
</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    subject = st.text_input("Subject Name")
    study_hours = st.number_input("Study Hours per Day", min_value=1, max_value=16, value=2)
with col2:
    deadline = st.date_input("Exam / Assignment Deadline")
    level = st.selectbox("Current Level", ["Beginner", "Intermediate", "Advanced"])

goal = st.text_area("Goal (e.g., Pass the exam, Score above 80%, Finish assignment)")
st.markdown('</div>', unsafe_allow_html=True)

st.markdown("""
<div class="card">
<div style="display:flex; align-items:center; gap:12px; margin-bottom:10px;">
<img src="https://cdn-icons-png.flaticon.com/512/3143/3143460.png" width="36" />
<h2 style="margin:0;">Syllabus / Assignment Material</h2>
</div>
""", unsafe_allow_html=True)

input_method = st.radio("Select Input Method:", ["Upload File (PDF/DOCX/TXT)", "Paste Text"])

if input_method == "Upload File (PDF/DOCX/TXT)":
    uploaded_file = st.file_uploader("Upload a PDF, DOCX, or TXT file", type=["pdf", "docx", "txt"])

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
                st.write(text[:2000] + ("..." if len(text) > 2000 else ""))
        else:
            st.warning("No text could be extracted from this file. Try another file.")

else:
    pasted = st.text_area("Paste your syllabus/assignment text here", height=200)
    st.session_state.extracted_text = pasted

st.markdown('</div>', unsafe_allow_html=True)

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
        st.markdown('</div>', unsafe_allow_html=True)