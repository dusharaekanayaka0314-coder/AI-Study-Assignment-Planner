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

# Standard stable Gemini model
model = genai.GenerativeModel("gemini-1.5-flash")

st.set_page_config(
    page_title="AI Study & Assignment Planner",
    page_icon="🎓",
    layout="centered"
)

# =========================================================
# MODERN VIBRANT UI STYLING
# =========================================================
st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

html, body, .stApp {
    font-family: 'Plus Jakarta Sans', sans-serif !important;
}

/* VIBRANT & COLORFUL FULL BACKGROUND */
.stApp {
    background: linear-gradient(
        135deg,
        rgba(15, 23, 42, 0.25) 0%,
        rgba(79, 70, 229, 0.15) 100%
    ),
    url('https://images.unsplash.com/photo-1579546929518-9e396f3cc809?q=80&w=2070&auto=format&fit=crop') !important;
    background-size: cover !important;
    background-position: center !important;
    background-attachment: fixed !important;
}

/* Main Container Card Styling for Readability */
[data-testid="stVerticalBlock"] > div {
    border-radius: 20px;
}

/* Field Label Styling */
label, .stMarkdown label p {
    font-size: 0.95rem !important;
    font-weight: 700 !important;
    color: #0F172A !important;
}

/* Header Card Styling */
.main-header {
    text-align: center;
    padding: 42px 24px;
    background: linear-gradient(135deg, rgba(79, 70, 229, 0.95) 0%, rgba(124, 58, 237, 0.95) 100%);
    backdrop-filter: blur(12px);
    border-radius: 24px;
    margin-bottom: 28px;
    box-shadow: 0 16px 36px -10px rgba(79, 70, 229, 0.45);
    color: #FFFFFF;
    border: 1px solid rgba(255, 255, 255, 0.2);
}

.main-header h1 {
    color: #FFFFFF !important;
    font-size: 2.3rem !important;
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
    margin-bottom: 18px;
    margin-top: 10px;
    background: rgba(255, 255, 255, 0.85);
    backdrop-filter: blur(8px);
    padding: 10px 16px;
    border-radius: 14px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.03);
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
    background-color: rgba(226, 232, 240, 0.8);
    backdrop-filter: blur(8px);
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
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1) !important;
}

/* Glassmorphism File Uploader Box */
[data-testid="stFileUploaderDropzone"] {
    background-color: rgba(255, 255, 255, 0.9) !important;
    backdrop-filter: blur(10px) !important;
    border: 2px dashed #818CF8 !important;
    border-radius: 18px !important;
    padding: 24px !important;
    box-shadow: 0 8px 20px rgba(0, 0, 0, 0.05) !important;
}

/* Purple Gradient Upload Button */
[data-testid="stFileUploaderDropzone"] button {
    background: linear-gradient(135deg, #4F46E5 0%, #7C3AED 100%) !important;
    color: #FFFFFF !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 10px 22px !important;
    font-weight: 700 !important;
    box-shadow: 0 4px 14px rgba(79, 70, 229, 0.35) !important;
    transition: all 0.2s ease-in-out !important;
}

[data-testid="stFileUploaderDropzone"] button:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 6px 18px rgba(79, 70, 229, 0.45) !important;
}

/* Prevent text overlapping in Streamlit button */
[data-testid="stFileUploaderDropzone"] button div,
[data-testid="stFileUploaderDropzone"] button span,
[data-testid="stFileUploaderDropzone"] button p {
    color: #FFFFFF !important;
    font-weight: 700 !important;
    position: static !important;
    margin: 0 !important;
    padding: 0 !important;
}

[data-testid="stFileUploaderDropzone"] button::before,
[data-testid="stFileUploaderDropzone"] button::after {
    content: none !important;
    display: none !important;
}

/* Input Fields Glass Styling */
.stTextInput input, .stSelectbox select, .stTextArea textarea, .stNumberInput input {
    background-color: rgba(255, 255, 255, 0.9) !important;
    backdrop-filter: blur(8px) !important;
    border-radius: 12px !important;
    border: 1px solid #CBD5E1 !important;
}

/* Primary Action Button (Generate Study Plan) */
div.stButton > button {
    background: linear-gradient(135deg, #4F46E5 0%, #7C3AED 100%) !important;
    color: #FFFFFF !important;
    font-weight: 700 !important;
    font-size: 1.1rem !important;
    border-radius: 14px !important;
    padding: 16px 28px !important;
    border: none !important;
    width: 100% !important;
    box-shadow: 0 8px 24px rgba(79, 70, 229, 0.4) !important;
    transition: all 0.25s ease-in-out !important;
    margin-top: 15px;
}

div.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 12px 28px rgba(79, 70, 229, 0.5) !important;
}

/* Output Box Container */
.output-box {
    background: rgba(255, 255, 255, 0.95);
    backdrop-filter: blur(12px);
    border: 1px solid #E2E8F0;
    border-radius: 20px;
    padding: 32px;
    box-shadow: 0 12px 30px rgba(0, 0, 0, 0.08);
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
# SYLLABUS / ASSIGNMENT MATERIAL SECTION
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
# GENERATE PLAN (WITH ERROR HANDLING)
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
{st.session_state.extracted_text[:4000]}
"""
            try:
                response = model.generate_content(prompt)
                
                st.markdown('<div class="output-box">', unsafe_allow_html=True)
                st.markdown(response.text)
                st.markdown('</div>', unsafe_allow_html=True)

            except Exception as e:
                error_msg = str(e)
                if "ResourceExhausted" in error_msg or "429" in error_msg:
                    st.error("⚠️ API Request Limit Exceeded! Google Gemini free tier limit එක පැනලා. විනාඩියක් ඉඳලා නැවත උත්සාහ කරන්න (Please wait 1 minute and try again).")
                else:
                    st.error(f"⚠️ An error occurred while generating the plan: {error_msg}")
