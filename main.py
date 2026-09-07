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
    page_icon="🎓",
    layout="centered"
)

# =========================================================
# MODERN UI STYLING WITH FULL BACKGROUND IMAGE
# =========================================================
st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

/* Apply modern font across application */
html, body, [class*="css"], p, span, label, div, h1, h2, h3, h4, h5, h6 {
    font-family: 'Plus Jakarta Sans', sans-serif !important;
}

/* Full Screen Background Image with Overlay */
.stApp {
    background: linear-gradient(
        rgba(248, 250, 252, 0.88), 
        rgba(248, 250, 252, 0.92)
    ),
    url('https://images.unsplash.com/photo-1516979187457-637abb4f9353?q=80&w=2070&auto=format&fit=crop') !important;
    background-size: cover !important;
    background-position: center !important;
    background-attachment: fixed !important;
}

/* Main Container Card Effect */
[data-testid="stVerticalBlock"] > div {
    border-radius: 16px;
}

/* Field Label Styling */
label, .stMarkdown label p {
    font-size: 0.95rem !important;
    font-weight: 700 !important;
    color: #1E293B !important;
}

/* Header Card Styling */
.main-header {
    text-align: center;
    padding: 40px 24px;
    background: linear-gradient(135deg, #4F46E5 0%, #7C3AED 100%);
    border-radius: 24px;
    margin-bottom: 28px;
    box-shadow: 0 12px 30px -8px rgba(79, 70, 229, 0.35);
    color: #FFFFFF;
}

.main-header h1 {
    color: #FFFFFF !important;
    font-size: 2.2rem !important;
    font-weight: 800 !important;
    margin-bottom: 8px !important;
    letter-spacing: -0.02em;
}

.main-header p {
    color: #E0E7FF !important;
    font-size: 1.05rem !important;
    font-weight: 500 !important;
    max-width: 600px;
    margin: 0 auto;
}

/* Section Title Styling */
.card-title {
    display: flex;
    align-items: center;
    gap: 12px;
    font-size: 1.25rem;
    font-weight: 800;
    color: #0F172A;
    margin-bottom: 20px;
    margin-top: 10px;
}

.card-title span {
    background: #EEF2FF;
    padding: 8px;
    border-radius: 12px;
    display: flex;
    align-items: center;
    justify-content: center;
    color: #4F46E5;
}

/* Custom Styled Tabs for File / Text Selection */
.stTabs [data-baseweb="tab-list"] {
    gap: 12px;
    background-color: #E2E8F0;
    padding: 6px;
    border-radius: 14px;
    margin-bottom: 20px;
}

.stTabs [data-baseweb="tab"] {
    height: 48px;
    border-radius: 10px;
    font-weight: 700 !important;
    font-size: 0.95rem !important;
    color: #475569 !important;
    background-color: transparent;
    border: none !important;
}

.stTabs [aria-selected="true"] {
    background-color: #FFFFFF !important;
    color: #4F46E5 !important;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08) !important;
}

/* Primary Action Button */
div.stButton > button {
    background: linear-gradient(135deg, #4F46E5 0%, #7C3AED 100%) !important;
    color: #FFFFFF !important;
    font-weight: 700 !important;
    font-size: 1.1rem !important;
    border-radius: 14px !important;
    padding: 16px 28px !important;
    border: none !important;
    width: 100% !important;
    box-shadow: 0 8px 20px rgba(79, 70, 229, 0.35) !important;
    transition: all 0.25s ease-in-out !important;
    margin-top: 15px;
}

div.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 12px 24px rgba(79, 70, 229, 0.45) !important;
}

/* Output Box Container */
.output-box {
    background: rgba(255, 255, 255, 0.95);
    border: 1px solid #E2E8F0;
    border-radius: 20px;
    padding: 32px;
    box-shadow: 0 10px 25px rgba(0, 0, 0, 0.05);
    margin-top: 28px;
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
    <div style="font-size: 3.2rem; margin-bottom: 10px;">🎓</div>
    <h1>AI Study & Assignment Planner</h1>
    <p>Upload your syllabus or assignment guidelines to generate an actionable, day-by-day study roadmap.</p>
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
<div class="card-title">
    <span>
        <svg width="22" height="22" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"></path>
        </svg>
    </span>
    Basic Details
</div>
""",
    unsafe_allow_html=True,
)

col1, col2 = st.columns(2)

with col1:
    subject = st.text_input("Subject Name", placeholder="e.g. Data Structures & Algorithms")
    study_hours = st.number_input(
        "Study Hours per Day", min_value=1, max_value=16, value=2
    )

with col2:
    deadline = st.date_input("Exam / Assignment Deadline")
    level = st.selectbox(
        "Current Level", ["Beginner", "Intermediate", "Advanced"]
    )

goal = st.text_area(
    "Goal",
    placeholder="e.g., Pass with A grade, Master core concepts, Complete assignment before deadline",
    height=100
)

st.write("")

# =========================================================
# SYLLABUS / ASSIGNMENT MATERIAL SECTION (TABS DESIGN)
# =========================================================
st.markdown(
    """
<div class="card-title">
    <span>
        <svg width="22" height="22" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
        </svg>
    </span>
    Syllabus / Assignment Material
</div>
""",
    unsafe_allow_html=True,
)

# Replacing crowded Radio Buttons with Clean Modern Tabs
tab1, tab2 = st.tabs(["📁 Upload File (PDF / DOCX / TXT)", "✏️ Paste Text Directly"])

with tab1:
    uploaded_file = st.file_uploader(
        "Upload your study material document", 
        type=["pdf", "docx", "txt"],
        key="file_uploader_tab"
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
            with st.expander("Preview Extracted Text"):
                st.write(text[:2000] + ("..." if len(text) > 2000 else ""))
        else:
            st.warning("No text could be extracted from this file. Try another file.")

with tab2:
    pasted = st.text_area(
        "Paste your syllabus content or guidelines below:", 
        height=180,
        placeholder="e.g. Chapter 1: Introduction to Java, Data Types, Control Statements..."
    )
    if pasted:
        st.session_state.extracted_text = pasted

st.write("")

# =========================================================
# GENERATE PLAN
# =========================================================
if st.button("Generate Study Plan"):
    if not st.session_state.extracted_text.strip():
        st.error("Please upload a file or paste text first.")
    else:
        with st.spinner("Analyzing material and creating your customized study roadmap..."):
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

        st.markdown('<div class="output-box">', unsafe_allow_html=True)
        st.markdown(response.text)
        st.markdown('</div>', unsafe_allow_html=True)
