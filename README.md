# SkillUp

**Team:** CodeNova  
**Description:** A secure, intelligent portal to track employment outcomes, diagnose competency skill gaps via resume parsing, and connect candidates with verified live job pipelines.

---

## Why we made this:

Tracking post-training employment outcomes, identifying specific technical skill gaps, and managing career pathways manually or using disjointed tools gets messy, confusing, and complicated. Enterprise systems feel too heavy and bureaucratic, so we built a fast, lightweight dashboard tailored for candidates and training institutions to handle authentication, skill matching, and career progression directly in the browser.

---

## Key Features & Platform Modules:

* **Secure Access Gateway (Login System):** 
  * Multi-role portal authentication supporting **Trainee**, **Govt Admin**, and **Employer** roles.
  * Secured with national frameworks (DigiLocker, APAAR, & NCVET integration tags).
* **Dashboard Hub & Analytics:** 
  * High-level performance indices tracking 6-Month Placement Index, 12-Month Retention Rate, Average Salary Growth, and Industry Skill Alignment.
  * Real-time Employment Status Tracker to log and update active job standing for continuous government outcome monitoring.
* **Skill Gap Diagnostics & AI Upskilling Roadmap:** 
  * Target role benchmarking (custom or standard roles like Junior Data Analyst, AI Engineer, etc.).
  * Drag-and-drop PDF resume parser that extracts verified skills, calculates an **Employability Readiness Index**, and maps missing market demand skills.
  * Personalized AI Upskilling Roadmap generating strategic milestone timelines to reach target competency matches.
* **Employment & Recruitment Feed:** 
  * Active recruitment pipeline displaying live job opportunities across top organizations (Google, Microsoft, Flipkart, Adobe, Cult.fit, Zoho).
  * Detailed matching analytics showing candidate match fit percentages, required tech stacks (PyTorch, TensorFlow, LLMs, LangChain, Kubernetes), candidate screening numbers, and direct "Apply Now" workflows.

---

## Tech Stack:

* **Backend & Server:** Python, FastAPI / Uvicorn server runtime (`main.py`)
* **Database & Storage:** SQLite (`database.db`)
* **Frontend:** HTML5, CSS3, JavaScript templates (`index.html`, `login.html`, `skillgaps.html`, `employement.html`)

---

## Getting Started & Demo

* **Local Setup:** 
  1. Clone the repository and navigate to the project directory.
  2. Run the server using Python (`python main.py` or via uvicorn).
  3. Open `http://127.0.0.1:8000/login.html` in any modern web browser.

---

## Future Roadmap:

### 1.Trainee Roadmap
* **AI-Driven Personal Upskilling Paths:** Integrate machine learning models to analyze resume gaps and automatically generate step-by-step custom learning milestones.
* **Interactive Skill Simulation & Practice:** Introduce integrated coding environments, mock interviews, and micro-assessments directly within the trainee dashboard.
* **Mobile Companion App:** Launch a dedicated mobile application (Android/iOS) for push notifications on job matches, application statuses, and daily learning goals.

### 2.Government Administrator Roadmap
* **Predictive Regional Analytics Engine:** Build advanced modeling tools to forecast regional skill shortages, employment trends, and scheme success before they happen.
* **Automated Scheme Compliance & Verification:** Integrate deep government identification and credential lockers (such as DigiLocker and APAAR) for instant, automated background tracking.
* **Multi-Language Regional Expansion:** Roll out complete support for multiple regional Indian languages to make tracking and governance seamless across rural and urban sectors.

### 3.Employer & Enterprise Roadmap
* **Direct Applicant Tracking System (ATS) Integration:** Build robust APIs to sync corporate job openings and applicant data directly with the SkillUp recruitment feed.
* **Automated Candidate Shortlisting:** Implement advanced matching algorithms that sort applicants by their verified skill fit percentage and resume rating score.
* **Post-Placement Retention Analytics:** Create feedback loops for employers to report employee performance and long-term retention metrics back to training institutions.

---

## 📁 File Structure

```text
├── main.py                  # FastAPI server application backend
├── database.db              # SQLite database for user data and tracking
├── index.html               # Main dashboard hub view
├── login.html               # Secure access gateway and multi-role login
├── skillgaps.html           # Competency gap diagnosis & resume parser interface
├── employement.html         # Active recruitment pipelines & live job feed
├── Style.css / BorderGlow.css # UI styling and dynamic theme components
└── README.md                # Project documentation
