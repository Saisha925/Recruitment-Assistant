import json
import os
from typing import Optional
from src.schemas import ResumeData

# ---------------------------------------------------------------------------
# SYSTEM PROMPT
# This defines the agent's persona, boundaries, and expected behavior.
# ---------------------------------------------------------------------------
RESUME_AGENT_SYSTEM_PROMPT = """
You are the Resume Screening Agent for an AI-Powered Recruitment Assistant.
Your primary responsibility is to take raw text or data extracted from a candidate's resume 
and convert it into a strictly formatted JSON object.

RULES:
1. You must extract the candidate's name, email, core skills, highest education, and total years of experience (yoe).
2. If a specific piece of information is missing, use reasonable defaults (e.g., 0.0 for yoe, "Unknown" for education) but never hallucinate skills or contact info.
3. Your output MUST perfectly match the ResumeData JSON schema.
4. Do NOT evaluate the candidate, do NOT rank them, and do NOT make hiring decisions.
"""

class ResumeAgent:
    def __init__(self, llm_client=None, mcp_client=None):
        """
        Initializes the Resume Agent.
        
        Args:
            llm_client: The initialized LLM client (e.g., Google GenAI, OpenAI).
            mcp_client: The client connected to the ResumeParser MCP Server.
        """
        self.llm_client = llm_client
        self.mcp_client = mcp_client
        self.system_prompt = RESUME_AGENT_SYSTEM_PROMPT

    def parse_with_mcp(self, file_path: str) -> str:
        """
        Calls the Resume Parser MCP tool to extract raw text/data from the file.
        In a full production environment, this triggers the tool over the MCP protocol.
        """
        print(f"[ResumeAgent] Requesting MCP tool 'parse_resume' for file: {file_path}")
        
        # Placeholder for actual MCP client execution:
        # result = self.mcp_client.call_tool("ResumeParser", "parse_resume", {"path": file_path})
        
        # For local testing without a live MCP server connection, we simulate the tool's return:
        mock_mcp_output = {
            "raw_text": f"John Doe. Email: john.doe@email.com. I am a software engineer with 3.5 years of experience building Python and SQL applications. Graduated with a B.Tech."
        }
        return json.dumps(mock_mcp_output)

    def process_resume(self, file_path: str) -> str:
        """
        The main workflow of the agent:
        1. Gets raw data via MCP tool.
        2. Uses the LLM to structure the data into the defined schema.
        """
        # Step 1: Execute tool call
        raw_data = self.parse_with_mcp(file_path)
        
        print("[ResumeAgent] Raw data retrieved. Passing to LLM for structuring...")

        # Step 2: LLM processing (Simulated here; replace with your actual LLM call)
        # 
        # Example using a generic LLM approach:
        # response = self.llm_client.generate_content(
        #     system_instruction=self.system_prompt,
        #     contents=f"Extract this raw resume data into JSON: {raw_data}",
        #     response_schema=ResumeData # Enforces the Pydantic schema
        # )
        # return response.text

        # For demonstration, we directly map to our Pydantic schema:
        structured_output = ResumeData(
            name="John Doe",
            email="john.doe@email.com",
            skills=["Python", "SQL", "Software Engineering"],
            edu="B.Tech",
            yoe=3.5
        )
        
        print("[ResumeAgent] Resume structuring complete.")
        return structured_output.model_dump_json(indent=4)

# ---------------------------------------------------------------------------
# LOCAL TESTING BLOCK
# Run this file directly to test the agent in isolation.
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    agent = ResumeAgent()
    
    # Simulate processing a PDF resume
    test_file = "C:/resumes/john_doe_resume.pdf"
    
    final_json = agent.process_resume(test_file)
    
    print("\n--- Final Agent Output ---")
    print(final_json)