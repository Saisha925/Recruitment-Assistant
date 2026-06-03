# 🤖 TalentAI - AI Recruitment Assistant

TalentAI is a modern, full-stack AI recruitment platform designed to automate resume screening, candidate evaluation, and interview scheduling. Powered by Google's Gemini AI, it parses candidate resumes, scores them against specific job requisitions, and seamlessly presents the data in a stunning Next.js dashboard.

## ✨ Features

* **AI Resume Parsing:** Extracts structured data (Name, Email, Education, Skills) directly from raw PDF resumes using PyPDF2 and Gemini.
* **Intelligent Candidate Matching:** Evaluates candidates against specific job descriptions (e.g., REQ-101) and provides a match score out of 100 with detailed AI reasoning.
* **Automated Leaderboards:** Ranks candidates dynamically using SQLite to help recruiters prioritize top talent.
* **Interview Scheduling:** Trigger automated interview workflows for shortlisted candidates.
* **Premium UI/UX:** Built with Next.js, Tailwind CSS, and shadcn/ui for a highly responsive, light-mode dashboard.

## 🛠️ Tech Stack

**Frontend:**
* [Next.js](https://nextjs.org/) (React Framework)
* [Tailwind CSS](https://tailwindcss.com/)
* [shadcn/ui](https://ui.shadcn.com/) (Components)
* [Lucide React](https://lucide.dev/) (Icons)

**Backend:**
* [FastAPI](https://fastapi.tiangolo.com/) (Python Web Framework)
* [Google Gemini API](https://aistudio.google.com/) (`gemini-1.5-flash-8b`)
* SQLite (Database)
* PyPDF2 (PDF Processing)
* Tenacity (Retry logic & error handling)

---

## 🚀 Getting Started

### Prerequisites
* Python 3.9+
* Node.js 18+
* A valid Google Gemini API Key

### 1. Clone the Repository
```bash
git clone [https://github.com/Saisha925/Recruitment-Assistant.git](https://github.com/Saisha925/Recruitment-Assistant.git)
cd Recruitment-Assistant
