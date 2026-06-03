import streamlit as st
import json
import time
import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv()

from src.agents.resume_agent import ResumeAgent
from src.agents.match_agent import MatchAgent
from src.agents.rank_agent import RankAgent
from src.agents.interview_agent import InterviewAgent

@st.cache_resource
def load_agents():
    return ResumeAgent(), MatchAgent(), RankAgent(), InterviewAgent()

ra, ma, rka, ia = load_agents()

st.set_page_config(page_title="AI Recruitment", layout="wide")
st.title("🤖 AI-Powered Recruitment Assistant")

if 'run' not in st.session_state:
    st.session_state.run = False
if 'res' not in st.session_state:
    st.session_state.res = None
if 'match' not in st.session_state:
    st.session_state.match = None
if 'rank' not in st.session_state:
    st.session_state.rank = None

with st.sidebar:
    st.header("Upload Candidate")
    target = st.selectbox("Select Role", ["REQ-101: AI/ML Engineer", "REQ-102: Data Scientist"])
    j_id = target.split(":")[0]
    
    file = st.file_uploader("Upload Resume", type=["pdf", "docx", "txt"])
    
    if st.button("Run AI Pipeline", type="primary", use_container_width=True):
        if file:
            st.session_state.run = True
            with st.spinner("Processing..."):
                res_json = ra.process_resume(file)
                st.session_state.res = json.loads(res_json)
                
                m_json = ma.eval_cand(res_json, j_id)
                st.session_state.match = json.loads(m_json)
                
                rk_json = rka.rank(j_id)
                st.session_state.rank = json.loads(rk_json)
        else:
            st.warning("Upload a file first.")

if st.session_state.run and st.session_state.res:
    st.divider()
    c1, c2 = st.columns([1, 1])
    
    with c1:
        st.subheader("Candidate Profile")
        st.write(f"**Name:** {st.session_state.res['name']}")
        st.write(f"**Email:** {st.session_state.res['email']}")
        st.write(f"**Education:** {st.session_state.res['edu']}")
        st.write(f"**Experience:** {st.session_state.res['yoe']} years")
        st.button(", ".join(st.session_state.res['skills']), disabled=True)
        
    with c2:
        st.subheader("AI Evaluation")
        col = "normal" if st.session_state.match['score'] >= 75 else "inverse"
        st.metric("Match Score", f"{st.session_state.match['score']}/100", st.session_state.match['status'], delta_color=col)
        st.info(f"**Reason:** {st.session_state.match['reason']}")

    st.divider()
    st.subheader("Leaderboard & Next Steps")
    
    df = pd.DataFrame(st.session_state.rank)
    st.dataframe(df, use_container_width=True, hide_index=True)
    
    if st.session_state.match['status'] == "Shortlisted":
        st.success(f"{st.session_state.res['name']} is shortlisted. Schedule interview?")
        
        if st.button("Approve & Schedule Interview"):
            with st.spinner("Booking..."):
                time.sleep(1.5)
                b_json = ia.book(st.session_state.res['email'])
                b_data = json.loads(b_json)
                
            st.balloons()
            st.success(f"**Booked!** \n\nTime: {b_data['start']} to {b_data['end']}")
    else:
        st.error("Candidate rejected.")
elif not st.session_state.run:
    st.info("Upload a resume to begin.")