import streamlit as st
import json
import time
import pandas as pd

# Import our AI Agents
from src.agents.resume_agent import ResumeAgent
from src.agents.match_agent import MatchAgent
from src.agents.rank_agent import RankAgent
from src.agents.interview_agent import InterviewAgent

# Initialize Agents
@st.cache_resource
def load_agents():
    return ResumeAgent(), MatchAgent(), RankAgent(), InterviewAgent()

resume_agent, match_agent, rank_agent, interview_agent = load_agents()

# --- UI Setup ---
st.set_page_config(page_title="AI Recruitment Assistant", layout="wide", page_icon="🤖")
st.title("🤖 AI-Powered Recruitment Assistant")
st.markdown("Automate resume screening, job matching, and interview scheduling with multi-agent AI.")

# --- Sidebar: Input Controls ---
with st.sidebar:
    st.header("Upload Candidate")
    target_job = st.selectbox("Select Target Role", ["REQ-101: AI/ML Engineer", "REQ-102: Data Scientist"])
    job_id = target_job.split(":")[0]
    
    uploaded_file = st.file_uploader("Upload Resume (PDF/Docx)", type=["pdf", "docx", "txt"])
    
    start_pipeline = st.button("Run AI Pipeline", type="primary", use_container_width=True)

# --- Main Dashboard ---
if start_pipeline and uploaded_file is not None:
    # We use st.status to show the user exactly what the agents are doing in real-time
    with st.status("Initializing AI Agent Pipeline...", expanded=True) as status:
        
        # 1. Resume Agent
        st.write("📄 **Resume Agent:** Extracting and structuring candidate data...")
        time.sleep(1) # Simulated network delay for UI feel
        resume_json = resume_agent.process_resume(uploaded_file.name)
        resume_data = json.loads(resume_json)
        
        # 2. Match Agent
        st.write(f"🎯 **Job Matching Agent:** Evaluating against {job_id} requirements...")
        time.sleep(1)
        match_json = match_agent.eval_cand(resume_json, job_id)
        match_data = json.loads(match_json)
        
        # 3. Rank Agent
        st.write("📊 **Ranking Agent:** Updating candidate leaderboard...")
        time.sleep(1)
        rank_json = rank_agent.rank(job_id)
        rank_data = json.loads(rank_json)
        
        status.update(label="AI Pipeline Complete!", state="complete", expanded=False)

    # --- Results Visualization ---
    st.divider()
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("Candidate Profile")
        st.write(f"**Name:** {resume_data['name']}")
        st.write(f"**Email:** {resume_data['email']}")
        st.write(f"**Education:** {resume_data['edu']}")
        st.write(f"**Years of Experience:** {resume_data['yoe']}")
        st.write("**Identified Skills:**")
        st.button(", ".join(resume_data['skills']), disabled=True) # Used as a styling pill
        
    with col2:
        st.subheader("AI Evaluation")
        
        # Color code the metric based on score
        delta_color = "normal" if match_data['score'] >= 75 else "inverse"
        st.metric(label="Match Score", value=f"{match_data['score']}/100", delta=match_data['status'], delta_color=delta_color)
        
        st.info(f"**AI Reasoning:** {match_data['reason']}")

    st.divider()

    # --- Human-in-the-Loop & Interview Agent ---
    st.subheader("Leaderboard & Next Steps")
    
    # Display leaderboard as a clean Pandas dataframe
    df = pd.DataFrame(rank_data)
    st.dataframe(df, use_container_width=True, hide_index=True)
    
    if match_data['status'] == "Shortlisted":
        st.success(f"{resume_data['name']} has been shortlisted by the AI. Would you like to schedule an interview?")
        
        if st.button("Approve & Schedule Interview"):
            with st.spinner("🗓️ Interview Agent checking calendars..."):
                time.sleep(1.5)
                booking_json = interview_agent.book(resume_data['email'])
                booking_data = json.loads(booking_json)
                
            st.balloons()
            st.success(f"**Interview successfully booked!** \n\nTime: {booking_data['start']} to {booking_data['end']}")
    else:
        st.error("Candidate did not meet the minimum threshold for this role.")

elif start_pipeline and uploaded_file is None:
    st.warning("Please upload a resume file in the sidebar to begin.")
else:
    st.info("👈 Upload a resume in the sidebar to trigger the AI pipeline.")