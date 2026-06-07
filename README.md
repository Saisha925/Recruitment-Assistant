# 🤖 TalentAI - AI Recruitment Assistant

TalentAI is a modern, full-stack AI recruitment platform designed to automate resume screening, candidate evaluation, and interview scheduling. Powered by Google's Gemini AI, it parses candidate resumes, scores them against specific job requisitions, and seamlessly presents the data in a stunning Next.js dashboard.

✨ Key Features
📄 Automated Resume Parsing: Extracts key information (education, skills, experience) from uploaded candidate PDFs.

🧠 AI-Powered Matching & Ranking: Utilizes Gemini AI (gemini-2.5-flash / gemini-3.5-flash) to evaluate candidates against specific job requisitions (e.g., REQ-101) and ranks them on a dynamic leaderboard.

✉️ One-Click Interview Scheduling: Automatically generates personalized email drafts and mock Calendly invite links for shortlisted candidates.

🔐 Secure Authentication: Full JWT-based user authentication system (Login, Sign Up, Protected Profiles) using bcrypt password hashing.

📊 Modern Interactive Dashboard: Built with Next.js and shadcn/ui, featuring real-time state updates, success banners, and clean candidate profiles.

🛠️ Tech Stack
Frontend:

Next.js (React Framework)

Tailwind CSS (Styling)

shadcn/ui (UI Components)

Lucide React (Icons)

Backend:

Python 3.x

FastAPI (RESTful API framework)

SQLite (Database)

PyJWT & Passlib (Authentication & Security)

AI & Agents:

Google Gemini API (LLM processing)

Custom Python Agent Architecture (ResumeAgent, MatchAgent, RankAgent, InterviewAgent)

recruitment-assistant/
│
├── frontend/                  # Next.js React Application
│   ├── app/                   # Next.js App Router pages
│   ├── components/            # UI Components (Dashboard, SuccessBanner, etc.)
│   ├── package.json
│   └── tailwind.config.js
│
├── src/                       # Backend AI Logic
│   └── agents/
│       ├── resume_agent.py    # Extracts text from PDFs
│       ├── match_agent.py     # Evaluates candidate against job reqs
│       ├── rank_agent.py      # Generates leaderboard scores
│       └── interview_agent.py # Drafts emails and scheduling links
│
├── data/                      # Local SQLite Database storage
│   └── recruitment.db
│
├── api.py                     # Main FastAPI application & routes
├── check_models.py            # Utility script to verify Gemini API access
├── .env                       # Environment variables (API keys)
└── requirements.txt           # Python dependencies


⚙️ Installation & Setup
Prerequisites
Node.js (v18+)

Python (3.9+)

A valid Google Gemini API Key

1. Clone the Repository
Bash
git clone https://github.com/yourusername/recruitment-assistant.git
cd recruitment-assistant
2. Backend Setup (FastAPI)
Open your terminal and navigate to the root directory:

Bash
# Create a virtual environment (optional but recommended)
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`

# Install required Python packages
pip install fastapi uvicorn python-multipart python-dotenv google-genai "passlib[bcrypt]" PyJWT

# Create a .env file in the root directory
echo "GEMINI_API_KEY=your_actual_api_key_here" > .env
echo "DATABASE_URL=data/recruitment.db" >> .env
3. Frontend Setup (Next.js)
Open a second terminal window and navigate to the frontend directory:

Bash
cd frontend

# Install Node dependencies
npm install

# Run the development server
npm run dev

🚀 Usage
Start the Backend: In your first terminal (root directory), run:

Bash
python api.py
The FastAPI server will start on http://127.0.0.1:8000

Start the Frontend: In your second terminal (/frontend directory), ensure the Next.js server is running.

Open the App: Navigate to http://localhost:3000 in your web browser.

Workflow:

Create an account / Log in.

Upload a candidate's PDF resume.

View the AI-generated matching analysis and leaderboard ranking.

Click Approve & Schedule Interview to instantly generate an invite link and email draft.

🐛 Troubleshooting
404 NOT_FOUND or limit: 0 from Gemini API: This means your specific API key does not have access to the model defined in the agents. Run python check_models.py to see which models your key supports, and update the string in the agent files accordingly (e.g., 'gemini-3.5-flash').

CORS Errors: Ensure your frontend is running on exactly http://localhost:3000 or update the allow_origins array in api.py.

Database Errors (no such table): Ensure the backend auth initialization function has run at least once to create the users and candidates tables in SQLite.
🚀 Usageecruitment-Assistant.git](https://github.com/Saisha925/Recruitment-Assistant.git)
cd Recruitment-Assistant
