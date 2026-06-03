"use client";

import React, { useState } from "react";
import type { User } from "@/app/page";
import { TopNav } from "@/components/top-nav";
import { Sidebar } from "@/components/sidebar";
import { CandidateProfile } from "@/components/candidate-profile";
import { AIEvaluation } from "@/components/ai-evaluation";
import { Leaderboard } from "@/components/leaderboard";
import { SuccessBanner } from "@/components/success-banner";

interface DashboardProps {
  user: User;
  onLogout: () => void;
}

export function Dashboard({ user, onLogout }: DashboardProps) {
  const [selectedRole, setSelectedRole] = useState<string>("");
  const [uploadedFile, setUploadedFile] = useState<File | null>(null);
  const [isPipelineRunning, setIsPipelineRunning] = useState(false);
  const [pipelineComplete, setPipelineComplete] = useState(false);
  
  // State to hold the real data from our Python AI
  const [pipelineResults, setPipelineResults] = useState<any>(null);

  const handleRunPipeline = async () => {
    if (!selectedRole || !uploadedFile) return;
    
    setIsPipelineRunning(true);
    setPipelineComplete(false);
    
    const formData = new FormData();
    formData.append("file", uploadedFile);
    formData.append("job_id", selectedRole); 

    try {
      // Connect to the FastAPI Python Backend!
      const res = await fetch("http://localhost:8000/api/process-resume", {
        method: "POST",
        body: formData,
      });
      const data = await res.json();
      
      if (data.status === "success") {
        setPipelineResults(data);
        setPipelineComplete(true);
      } else {
        alert("API Error: Please check the Python terminal.");
      }
    } catch (err) {
      console.error(err);
      alert("Failed to connect to the Python Backend. Is FastAPI running?");
    } finally {
      setIsPipelineRunning(false);
    }
  };

  // Map the Python JSON format to the format the React components expect
  let currentCandidate = null;
  let currentEvaluation = null;
  let leaderboardEntries = [];

  if (pipelineResults) {
    currentCandidate = {
      name: pipelineResults.candidate.name,
      email: pipelineResults.candidate.email,
      education: pipelineResults.candidate.edu, // Mapped from your Python schema
      skills: pipelineResults.candidate.skills,
    };

    const rawStatus = pipelineResults.match.status.toLowerCase();
    currentEvaluation = {
      matchScore: pipelineResults.match.score,
      status: rawStatus === "shortlisted" || rawStatus === "rejected" ? rawStatus : "pending",
      reasoning: pipelineResults.match.reason,
    };

    leaderboardEntries = pipelineResults.leaderboard.map((entry: any) => ({
      rank: entry.rank,
      email: entry.cand_id, // Mapped from SQLite
      score: entry.score,
      status: entry.status.toLowerCase() === "shortlisted" || entry.status.toLowerCase() === "rejected" ? entry.status.toLowerCase() : "pending",
    }));
  }

  return (
    <div className="min-h-screen bg-background">
      <TopNav user={user} onLogout={onLogout} />
      
      <div className="flex">
        <Sidebar
          selectedRole={selectedRole}
          onRoleChange={setSelectedRole}
          uploadedFile={uploadedFile}
          onFileUpload={setUploadedFile}
          onRunPipeline={handleRunPipeline}
          isPipelineRunning={isPipelineRunning}
          canRunPipeline={!!selectedRole && !!uploadedFile}
        />
        
        <main className="flex-1 p-6 ml-80">
          <div className="max-w-6xl mx-auto space-y-6">
            {/* Top Grid - Profile and Evaluation */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              <CandidateProfile candidate={currentCandidate} />
              <AIEvaluation 
                evaluation={currentEvaluation}
                isLoading={isPipelineRunning}
              />
            </div>

            {/* Bottom - Leaderboard */}
            <Leaderboard 
              entries={leaderboardEntries}
              onSelectCandidate={() => {}} 
              selectedIndex={-1}
            />

            {/* Success Banner */}
            {pipelineComplete && currentEvaluation?.status === "shortlisted" && (
              <SuccessBanner candidateName={currentCandidate?.name || ""} />
            )}
          </div>
        </main>
      </div>
    </div>
  );
}