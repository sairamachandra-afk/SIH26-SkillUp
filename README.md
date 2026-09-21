# SkillUp

**Team:** CodeNova  
**Live Demo:** [https://sairamachandra-afk.github.io/SIH26-SkillUp/Templates/index.html](https://sairamachandra-afk.github.io/SIH26-SkillUp/Templates/index.html)  
**Description:** A secure, intelligent portal to track employment outcomes, diagnose competency skill gaps via resume parsing, and connect candidates with verified live job pipelines.

---

## Why we made this:

Tracking post-training employment outcomes, identifying specific technical skill gaps, and managing career pathways manually or using disjointed tools gets messy, confusing, and complicated. Enterprise systems feel too heavy and bureaucratic, so we built a fast, lightweight dashboard tailored for candidates and training institutions to handle authentication, skill matching, and career progression directly in the browser.

---

## Key Features & Platform Modules:

* **Secure Access Gateway (Login System):** 
  * Multi-role portal authentication supporting **Trainee**, **Govt Admin**, and **Employer** roles[cite: 3].
  * Secured with national frameworks (DigiLocker, APAAR, & NCVET integration tags)[cite: 3].
* **Dashboard Hub & Analytics:** 
  * High-level performance indices tracking 6-Month Placement Index, 12-Month Retention Rate, Average Salary Growth, and Industry Skill Alignment[cite: 4].
  * Real-time Employment Status Tracker to log and update active job standing for continuous government outcome monitoring[cite: 4].
* **Skill Gap Diagnostics & AI Upskilling Roadmap:** 
  * Target role benchmarking (custom or standard roles like Junior Data Analyst, AI Engineer, etc.)[cite: 6].
  * Drag-and-drop PDF resume parser that extracts verified skills, calculates an **Employability Readiness Index**, and maps missing market demand skills[cite: 6].
  * Personalized AI Upskilling Roadmap generating strategic milestone timelines to reach target competency matches[cite: 6].
* **Employment & Recruitment Feed:** 
  * Active recruitment pipeline displaying live job opportunities across top organizations (Google, Microsoft, Flipkart, Adobe, Cult.fit, Zoho)[cite: 6].
  * Detailed matching analytics showing candidate match fit percentages, required tech stacks (PyTorch, TensorFlow, LLMs, LangChain, Kubernetes), candidate screening numbers, and direct "Apply Now" workflows[cite: 4, 6].

---

## Tech Stack:

* **Backend & Server:** Python, FastAPI / Uvicorn server runtime (`main.py`)[cite: 3, 4]
* **Database & Storage:** SQLite (`database.db`)[cite: 3, 4]
* **Frontend:** HTML5, CSS3, JavaScript templates (`index.html`, `login.html`, `skillgaps.html`, `employement.html`)[cite: 3, 4, 5, 6]

---

## Getting Started & Demo

* **Live Demo:** Try out the hosted version directly at [https://sairamachandra-afk.github.io/SIH26-SkillUp/Templates/index.html](https://sairamachandra-afk.github.io/SIH26-SkillUp/Templates/index.html).
* **Local Setup:** 
  1. Clone the repository and navigate to the project directory.
  2. Run the server using Python (`python main.py` or via uvicorn)[cite: 3, 4].
  3. Open `http://127.0.0.1:8000/login.html` in any modern web browser[cite: 3].

---

## Future Roadmap:

* **AI-Driven Career Pathways:** Integrating advanced machine learning models to suggest personalized upskilling roadmaps based on live job market trends.
* **Automated Employer Integration:** Building deep APIs to directly sync hiring partner data and verify employment outcomes seamlessly.
* **Advanced Predictive Modeling:** Forecasting regional skill shortages and employment shifts before they happen.
* **Multi-Language Support:** Expanding accessibility by adding support for various regional Indian languages.
* **Mobile Companion App:** Launching a dedicated mobile-friendly interface for candidates and administrators on-the-go.

---

## 📁 File Structure

```text
├── main.py                  # FastAPI server application backend[cite: 3, 4]
├── database.db              # SQLite database for user data and tracking[cite: 3, 4]
├── index.html               # Main dashboard hub view[cite: 3, 4]
├── login.html               # Secure access gateway and multi-role login[cite: 3]
├── skillgaps.html           # Competency gap diagnosis & resume parser interface[cite: 5]
├── employement.html         # Active recruitment pipelines & live job feed[cite: 6]
├── Style.css / BorderGlow.css # UI styling and dynamic theme components[cite: 3]
└── README.md                # Project documentation
