# 🎓 AI Study & Assignment Planner

An intelligent, AI-powered web application designed to help students, developers and self-learners convert complex syllabi, assignment guidelines, or course documents into personalized, day-by-day study roadmaps. 

Powered by **Google Gemini AI** and built with **Streamlit**, this tool features a modern, glassmorphism-inspired UI for an intuitive and seamless user experience.

---

## 🚀 Live Demo & Links

* 🌐 **Live Web App:** [AI Study & Assignment Planner](https://ai-study-assignment-planner-mbffdxwpcveidcyqodwaz6.streamlit.app)
* 📁 **GitHub Repository:** [AI-Study-Assignment-Planner](https://github.com/dusharaekanayaka0314-coder/AI-Study-Assignment-Planner.git)

---

## ✨ Key Features

* 📄 **Multi-Format Document Parsing:** Extract text seamlessly from PDF, DOCX, and TXT files.
* ✍️ **Direct Text Input Option:** Paste course syllabi or assignment prompts directly into the app.
* 🧠 **Personalized AI Roadmaps:** Generates tailored study plans based on:
  * Exam / Assignment deadline
  * Target daily study hours
  * Skill level (Beginner, Intermediate, Advanced)
  * Personal target goals
* 📊 **Structured Insights:** Outputs categorized lists including:
  * Key / Important Topics
  * High-Priority Areas
  * Day-by-Day Actionable Timetable
  * Strategic Focus Advice
* 🎨 **Modern Vibrant Glassmorphism UI:** Complete with purple gradient theme styling, responsive layouts, and clean typography.

---

## 🛠️ Tech Stack

* **Frontend / Framework:** [Streamlit](https://streamlit.io/)
* **AI Model Engine:** [Google Gemini AI API](https://ai.google.dev/) (`google-generativeai`)
* **File Processing:** `PyPDF2`, `python-docx`
* **Environment Management:** `python-dotenv`
* **Styling:** Custom CSS (Glassmorphism, CSS Grid/Flexbox)

---

## 📁 Repository Structure

```text
├── .env                  # Environment variables (API Keys)
├── main.py               # Main Streamlit application
├── requirements.txt      # Python dependencies
└── README.md             # Project documentation
```

## 💻 Local Setup & Installation

Follow these steps to run the application on your local machine:

### 1. Clone the Repository
```bash
git clone [https://github.com/dusharaekanayaka0314-coder/AI-Study-Assignment-Planner.git](https://github.com/dusharaekanayaka0314-coder/AI-Study-Assignment-Planner.git)
cd AI-Study-Assignment-Planner
```
2. Create and Activate a Virtual Environment
  ```bash
 # On macOS / Linux
python3 -m venv venv
source venv/bin/activate

# On Windows
python -m venv venv
venv\Scripts\activate
```
3. Install Dependencies
  ```bash
pip install -r requirements.txt
 ```
4. Set Up Environment Variables
Create a .env file in the project root directory and add your Google Gemini API key
  ```bash
GEMINI_API_KEY=your_google_gemini_api_key_here
  ```
5. Run the Streamlit App
```Bash
streamlit run main.py
The app will open automatically in your browser at http://localhost:8501.
```
## 🔮 Future Improvements & Roadmap

- [ ] **RAG Architecture Integration:** Implement LangChain/LlamaIndex with Vector DBs (FAISS/ChromaDB) to process massive textbooks without text truncation.
- [ ] **Calendar Integration:** Export generated daily schedules directly to Google Calendar or Apple iCal.
- [ ] **Progress Tracking Dashboard:** Allow users to check off completed days, topics, and study milestones.
- [ ] **Download Options:** One-click PDF / Markdown export for generated study plans.
- [ ] **Multi-Language Support:** Enhanced parsing and study roadmap generation for Sinhala and Tamil study materials.
- [ ] **Automated Reminders:** Email and push notifications for daily study sessions based on the plan.
      
🤝 Contributing
- Contributions, issues and feature requests are welcome! 
- Feel free to check the Issues page if you want to contribute.

