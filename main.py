from dotenv import load_dotenv
import os
import streamlit as st

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

import google.generativeai as genai

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-3.6-flash")

st.set_page_config(
    page_title="AI Study & Assignment Planner",
    layout="centered"
)

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700;800&display=swap');

/* =========================================================
   GLOBAL
   ========================================================= */

html,
body,
[class*="css"],
p,
span,
label,
div,
h1,
h2,
h3,
h4 {
    font-family: 'Poppins', sans-serif;
}

[data-testid="stAppViewContainer"],
[data-testid="stHeader"],
.main,
body,
.stApp {
    background-color: #FFFFFF !important;
    color: #1E1E2F !important;
}

label,
.stMarkdown,
p,
span {
    color: #1E1E2F !important;
}


/* =========================================================
   TEXT INPUT - SUBJECT NAME
   ========================================================= */

[data-testid="stTextInput"] div[data-baseweb="input"] {
    background-color: #FFFFFF !important;
    border: 1px solid #D8D2F5 !important;
    border-radius: 8px !important;
    box-shadow: none !important;
}

[data-testid="stTextInput"] div[data-baseweb="input"]:focus-within {
    border-color: #6C5CE7 !important;
    box-shadow: 0 0 0 1px #6C5CE7 !important;
}

[data-testid="stTextInput"] input {
    background-color: #FFFFFF !important;
    color: #1E1E2F !important;
    -webkit-text-fill-color: #1E1E2F !important;
    border: none !important;
    outline: none !important;
    box-shadow: none !important;
}


/* =========================================================
   NUMBER INPUT - STUDY HOURS
   ========================================================= */

/*
   Make the complete number input behave as one clean
   horizontal control.
*/

[data-testid="stNumberInput"] {
    width: 100% !important;
}

[data-testid="stNumberInput"] > div {
    display: flex !important;
    flex-direction: row !important;
    align-items: stretch !important;
    width: 100% !important;

    background-color: #FFFFFF !important;

    border: 1px solid #D8D2F5 !important;
    border-radius: 8px !important;

    overflow: hidden !important;
    box-shadow: none !important;

    min-height: 40px !important;
}


/* Number input text section */

[data-testid="stNumberInput"] div[data-baseweb="input"] {
    flex: 1 1 auto !important;
    min-width: 0 !important;

    background-color: #FFFFFF !important;
    border: none !important;
    box-shadow: none !important;
}


/* Number input text */

[data-testid="stNumberInput"] input {
    width: 100% !important;

    background-color: #FFFFFF !important;
    color: #1E1E2F !important;
    -webkit-text-fill-color: #1E1E2F !important;

    border: none !important;
    outline: none !important;
    box-shadow: none !important;

    text-align: left !important;

    padding: 8px 12px !important;
    font-size: 15px !important;
}


/* Focus state */

[data-testid="stNumberInput"] div[data-baseweb="input"]:focus-within {
    box-shadow: none !important;
}


/* =========================================================
   NUMBER INPUT +/- BUTTONS
   ========================================================= */

[data-testid="stNumberInput"] button {
    width: 38px !important;
    min-width: 38px !important;
    max-width: 38px !important;

    height: 38px !important;
    min-height: 38px !important;

    padding: 0 !important;
    margin: 0 !important;

    display: flex !important;
    align-items: center !important;
    justify-content: center !important;

    background-color: #F5F3FF !important;
    color: #1E1E2F !important;

    border: none !important;
    border-left: 1px solid #E0D9FF !important;

    border-radius: 0 !important;

    box-shadow: none !important;

    font-size: 18px !important;
    font-weight: 600 !important;

    transition: all 0.15s ease !important;
}


/* Hover */

[data-testid="stNumberInput"] button:hover {
    background-color: #EDE7FF !important;
    color: #6C5CE7 !important;
}


/* Active */

[data-testid="stNumberInput"] button:active {
    background-color: #DCD4FF !important;
}


/* Disabled */

[data-testid="stNumberInput"] button:disabled {
    background-color: #F7F6FC !important;
    color: #B8B4C9 !important;
    cursor: not-allowed !important;
}


/* =========================================================
   DATE INPUT - DEADLINE
   ========================================================= */

[data-testid="stDateInput"] {
    color-scheme: light !important;
}

[data-testid="stDateInput"] div[data-baseweb="input"] {
    background-color: #FFFFFF !important;

    border: 1px solid #D8D2F5 !important;
    border-radius: 8px !important;

    box-shadow: none !important;

    color-scheme: light !important;
}

[data-testid="stDateInput"] div[data-baseweb="input"]:focus-within {
    border-color: #6C5CE7 !important;
    box-shadow: 0 0 0 1px #6C5CE7 !important;
}

[data-testid="stDateInput"] input {
    background-color: #FFFFFF !important;

    color: #1E1E2F !important;
    -webkit-text-fill-color: #1E1E2F !important;

    border: none !important;
    outline: none !important;
    box-shadow: none !important;

    color-scheme: light !important;
}

[data-testid="stDateInput"] svg {
    color: #6C5CE7 !important;
    fill: #6C5CE7 !important;
}


/* =========================================================
   CALENDAR POPUP
   ========================================================= */

/*
   IMPORTANT:
   Do NOT use:
       calendar *
   with background-color.
   
   That was causing the dark/incorrect calendar appearance.
*/

div[data-baseweb="calendar"] {
    background-color: #FFFFFF !important;

    border: 1px solid #E0D9FF !important;
    border-radius: 12px !important;

    box-shadow: 0 10px 30px rgba(30, 30, 47, 0.15) !important;

    color: #1E1E2F !important;

    padding: 8px !important;

    color-scheme: light !important;
}


/* Calendar popover */

div[data-baseweb="popover"] {
    background-color: #FFFFFF !important;
    border-radius: 12px !important;
    color-scheme: light !important;
}


/* Calendar header */

div[data-baseweb="calendar"] header {
    background-color: #FFFFFF !important;
    color: #1E1E2F !important;
}


/* Calendar navigation buttons */

div[data-baseweb="calendar"] button {
    background-color: #FFFFFF !important;

    color: #1E1E2F !important;

    border: none !important;

    box-shadow: none !important;

    border-radius: 8px !important;
}


/* Navigation button hover */

div[data-baseweb="calendar"] button:hover {
    background-color: #F5F3FF !important;
    color: #6C5CE7 !important;
}


/* Calendar text */

div[data-baseweb="calendar"] [role="grid"] {
    background-color: #FFFFFF !important;
}

div[data-baseweb="calendar"] [role="gridcell"] {
    background-color: #FFFFFF !important;
    color: #1E1E2F !important;
}


/* Date buttons */

div[data-baseweb="calendar"] [role="gridcell"] button {
    background-color: #FFFFFF !important;

    color: #1E1E2F !important;

    border: none !important;

    border-radius: 50% !important;

    width: 32px !important;
    height: 32px !important;

    display: flex !important;
    align-items: center !important;
    justify-content: center !important;

    margin: 2px auto !important;

    font-size: 13px !important;

    transition: all 0.15s ease !important;
}


/* Date hover */

div[data-baseweb="calendar"] [role="gridcell"] button:hover {
    background-color: #EDE7FF !important;
    color: #6C5CE7 !important;
}


/* Selected date */

div[data-baseweb="calendar"] [role="gridcell"] button[aria-selected="true"],
div[data-baseweb="calendar"] [aria-selected="true"] {
    background-color: #6C5CE7 !important;
    color: #FFFFFF !important;

    font-weight: 600 !important;
}


/* Selected date hover */

div[data-baseweb="calendar"] [role="gridcell"] button[aria-selected="true"]:hover {
    background-color: #5B4BD6 !important;
    color: #FFFFFF !important;
}


/* Disabled dates */

div[data-baseweb="calendar"] [role="gridcell"] button:disabled {
    background-color: #FFFFFF !important;
    color: #C8C5D2 !important;

    opacity: 1 !important;

    cursor: not-allowed !important;
}


/* Today */

div[data-baseweb="calendar"] [role="gridcell"] button[aria-label*="Today"] {
    border: 1px solid #6C5CE7 !important;
}


/* Selected + Today */

div[data-baseweb="calendar"] [role="gridcell"] button[aria-selected="true"][aria-label*="Today"] {
    border: 2px solid #FFFFFF !important;
    background-color: #6C5CE7 !important;
    color: #FFFFFF !important;
}


/* Weekday headings */

div[data-baseweb="calendar"] [role="columnheader"] {
    background-color: #FFFFFF !important;
    color: #6B6878 !important;

    font-size: 12px !important;
    font-weight: 600 !important;
}


/* Month / year text */

div[data-baseweb="calendar"] div {
    color: #1E1E2F !important;
}


/* =========================================================
   SELECTBOX - CURRENT LEVEL
   ========================================================= */

[data-testid="stSelectbox"] div[data-baseweb="select"] {
    background-color: #FFFFFF !important;
}

[data-testid="stSelectbox"] div[data-baseweb="select"] > div {
    background-color: #FFFFFF !important;

    border: 1px solid #D8D2F5 !important;
    border-radius: 8px !important;

    color: #1E1E2F !important;
}

[data-testid="stSelectbox"] div[data-baseweb="select"] > div:focus-within {
    border-color: #6C5CE7 !important;
}

[data-testid="stSelectbox"] svg {
    fill: #1E1E2F !important;
    color: #1E1E2F !important;
}


/* Selectbox dropdown menu */

div[data-baseweb="popover"] ul {
    background-color: #FFFFFF !important;
}

div[data-baseweb="popover"] li {
    background-color: #FFFFFF !important;
    color: #1E1E2F !important;
}

div[data-baseweb="popover"] li:hover {
    background-color: #F5F3FF !important;
    color: #6C5CE7 !important;
}


/* =========================================================
   TEXTAREA - GOAL / PASTE TEXT
   ========================================================= */

[data-testid="stTextArea"] textarea {
    width: 100% !important;

    background-color: #FFFFFF !important;

    color: #1E1E2F !important;
    -webkit-text-fill-color: #1E1E2F !important;

    border: 1px solid #D8D2F5 !important;
    border-radius: 8px !important;

    box-shadow: none !important;

    resize: vertical !important;
}

[data-testid="stTextArea"] textarea:focus {
    border-color: #6C5CE7 !important;

    box-shadow: 0 0 0 1px #6C5CE7 !important;
}


/* =========================================================
   FILE UPLOADER
   ========================================================= */

[data-testid="stFileUploader"] {
    background-color: #FFFFFF !important;
    color: #1E1E2F !important;
}

[data-testid="stFileUploaderDropzone"] {
    background-color: #FAF9FF !important;

    border: 2px dashed #A29BFE !important;
    border-radius: 14px !important;

    color: #1E1E2F !important;

    display: flex !important;
    align-items: center !important;
    justify-content: space-between !important;

    padding: 12px 16px !important;
}

[data-testid="stFileUploaderDropzone"] * {
    color: #1E1E2F !important;
}

[data-testid="stFileUploaderDropzoneInstructions"] {
    background-color: transparent !important;
    color: #1E1E2F !important;

    display: flex !important;
    flex-direction: column !important;
    justify-content: center !important;
}

[data-testid="stFileUploaderDropzone"] button,
[data-testid="stBaseButton-secondary"] {
    background-color: #6C5CE7 !important;
    color: #FFFFFF !important;

    border: none !important;
    border-radius: 8px !important;

    position: static !important;

    margin-left: 12px !important;
}

[data-testid="stFileUploaderDropzone"] button:hover,
[data-testid="stBaseButton-secondary"]:hover {
    background-color: #5B4BD6 !important;
    color: #FFFFFF !important;
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

    display: flex !important;
    align-items: center !important;

    cursor: pointer;
}

div[role="radiogroup"] label p {
    color: #1E1E2F !important;
    margin: 0 !important;
}


/* Radio indicator */

div[role="radiogroup"] label span[data-baseweb="radio"] {
    background-color: #FFFFFF !important;

    border: 2px solid #6C5CE7 !important;

    border-radius: 50% !important;

    width: 18px !important;
    height: 18px !important;

    margin-right: 10px !important;

    flex-shrink: 0;
}


/* Selected radio */

div[role="radiogroup"] label input:checked + div span[data-baseweb="radio"],
div[role="radiogroup"] label[data-checked="true"] span[data-baseweb="radio"] {
    background-color: #6C5CE7 !important;

    box-shadow: inset 0 0 0 3px #FFFFFF !important;
}


/* Selected option */

div[role="radiogroup"] label:has(input:checked) {
    background-color: #EDE7FF !important;

    border: 1px solid #6C5CE7 !important;
}


/* =========================================================
   MAIN HEADER
   ========================================================= */

.main-header {
    text-align: center;

    padding: 30px 20px;

    background: linear-gradient(
        135deg,
        #6C5CE7 0%,
        #A29BFE 100%
    );

    border-radius: 20px;

    margin-bottom: 25px;

    box-shadow:
        0 8px 24px rgba(108, 92, 231, 0.35);
}

.main-header h1,
.main-header p {
    color: #FFFFFF !important;
}


/* =========================================================
   CARDS
   ========================================================= */

.card {
    background: #FFFFFF !important;

    padding: 24px;

    border-radius: 18px;

    box-shadow:
        0 6px 18px rgba(108, 92, 231, 0.12);

    margin-bottom: 22px;

    border: 1px solid #EDE9FE;
}

.card h2 {
    color: #6C5CE7 !important;
}


/* =========================================================
   MAIN BUTTON
   ========================================================= */

div.stButton > button {
    background: linear-gradient(
        90deg,
        #6C5CE7,
        #A29BFE
    ) !important;

    color: #FFFFFF !important;

    font-weight: 700;
    font-size: 1.05rem;

    border-radius: 12px;

    padding: 12px 24px;

    border: none;

    width: 100%;

    box-shadow:
        0 4px 14px rgba(108, 92, 231, 0.4);

    transition: all 0.2s ease-in-out;
}

div.stButton > button:hover {
    background: linear-gradient(
        90deg,
        #5B4BD6,
        #8E86F5
    ) !important;

    transform: translateY(-2px);

    box-shadow:
        0 6px 18px rgba(108, 92, 231, 0.5);
}


/* =========================================================
   ALERTS
   ========================================================= */

div[data-testid="stAlert"] {
    border-radius: 12px;
}


/* =========================================================
   EXPANDER
   ========================================================= */

details {
    border-radius: 12px !important;
    background: #FFFFFF !important;
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# HEADER
# =========================================================

st.markdown("""
<div class="main-header">

    <img
        src="https://cdn-icons-png.flaticon.com/512/2436/2436874.png"
        width="90"
        style="margin-bottom: 10px;"
    />

    <h1>AI Study & Assignment Planner</h1>

    <p>
        Upload your syllabus or assignment and let AI create
        a personalized study plan for you.
    </p>

</div>
""", unsafe_allow_html=True)


# =========================================================
# SESSION STATE
# =========================================================

if "extracted_text" not in st.session_state:
    st.session_state.extracted_text = ""


# =========================================================
# BASIC DETAILS CARD
# =========================================================

st.markdown("""
<div class="card">

<div style="
    display:flex;
    align-items:center;
    gap:12px;
    margin-bottom:10px;
">

    <img
        src="https://cdn-icons-png.flaticon.com/512/2921/2921222.png"
        width="36"
    />

    <h2 style="margin:0;">
        Basic Details
    </h2>

</div>
""", unsafe_allow_html=True)


col1, col2 = st.columns(2)


with col1:

    subject = st.text_input("Subject Name")

    study_hours = st.number_input(
        "Study Hours per Day",
        min_value=1,
        max_value=16,
        value=2
    )


with col2:

    deadline = st.date_input(
        "Exam / Assignment Deadline"
    )

    level = st.selectbox(
        "Current Level",
        [
            "Beginner",
            "Intermediate",
            "Advanced"
        ]
    )


goal = st.text_area(
    "Goal (e.g., Pass the exam, Score above 80%, Finish assignment)"
)


st.markdown(
    '</div>',
    unsafe_allow_html=True
)


# =========================================================
# SYLLABUS / ASSIGNMENT MATERIAL CARD
# =========================================================

st.markdown("""
<div class="card">

<div style="
    display:flex;
    align-items:center;
    gap:12px;
    margin-bottom:10px;
">

    <img
        src="https://cdn-icons-png.flaticon.com/512/3143/3143460.png"
        width="36"
    />

    <h2 style="margin:0;">
        Syllabus / Assignment Material
    </h2>

</div>
""", unsafe_allow_html=True)


input_method = st.radio(
    "Select Input Method:",
    [
        "Upload File (PDF/DOCX/TXT)",
        "Paste Text"
    ]
)


# =========================================================
# FILE UPLOAD
# =========================================================

if input_method == "Upload File (PDF/DOCX/TXT)":

    uploaded_file = st.file_uploader(
        "Upload a PDF, DOCX, or TXT file",
        type=["pdf", "docx", "txt"]
    )

    if uploaded_file is not None:

        text = ""

        # -----------------------------
        # PDF
        # -----------------------------

        if uploaded_file.name.endswith(".pdf"):

            import PyPDF2

            reader = PyPDF2.PdfReader(uploaded_file)

            for page in reader.pages:
                text += page.extract_text() or ""


        # -----------------------------
        # DOCX
        # -----------------------------

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


        # -----------------------------
        # TXT
        # -----------------------------

        elif uploaded_file.name.endswith(".txt"):

            text = uploaded_file.read().decode("utf-8")


        st.session_state.extracted_text = text


        if text.strip():

            st.success(
                "File processed successfully."
            )

            with st.expander(
                "View Extracted Text"
            ):

                st.write(
                    text[:2000]
                    + (
                        "..."
                        if len(text) > 2000
                        else ""
                    )
                )

        else:

            st.warning(
                "No text could be extracted from this file. "
                "Try another file."
            )


# =========================================================
# PASTE TEXT
# =========================================================

else:

    pasted = st.text_area(
        "Paste your syllabus/assignment text here",
        height=200
    )

    st.session_state.extracted_text = pasted


st.markdown(
    '</div>',
    unsafe_allow_html=True
)


# =========================================================
# GENERATE STUDY PLAN
# =========================================================

if st.button("Generate Study Plan"):

    if not st.session_state.extracted_text.strip():

        st.error(
            "Please upload a file or paste text first."
        )

    else:

        with st.spinner(
            "Gemini is analyzing your material..."
        ):

            prompt = f"""
You are a study planner AI.

Based on the details and material below,
respond using EXACTLY this format with markdown headers:

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

            response = model.generate_content(
                prompt
            )


        st.markdown(
            '<div class="card">',
            unsafe_allow_html=True
        )

        st.subheader(
            "Your Study Plan"
        )

        st.markdown(
            response.text
        )

        st.markdown(
            '</div>',
            unsafe_allow_html=True
        )
