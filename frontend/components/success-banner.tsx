"use client";

import { useState } from "react";
import { Button } from "@/components/ui/button";
import { CheckCircle2, Calendar, PartyPopper } from "lucide-react";

interface SuccessBannerProps {
  candidateName: string;
  // I made these optional so it doesn't crash your dashboard if they aren't passed yet
  candidateEmail?: string;
  jobId?: string;
}

export function SuccessBanner({
  candidateName,
  candidateEmail = "candidate@example.com",
  jobId = "REQ-101"
}: SuccessBannerProps) {
  const [isScheduling, setIsScheduling] = useState(false);
  const [scheduleData, setScheduleData] = useState<{ email_body: string; invite_link: string } | null>(null);

  const handleScheduleClick = async () => {
    setIsScheduling(true);
    try {
      const res = await fetch("http://127.0.0.1:8000/api/schedule", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          cand_id: 1,
          name: candidateName,
          email: candidateEmail,
          job_id: jobId
        }),
      });

      const jsn = await res.json();

      if (res.ok && jsn.success) {
        setScheduleData(jsn);
      } else {
        alert("Backend Error: " + (jsn.detail || "Unknown error"));
      }
    } catch (err) {
      alert("Network Error: Could not reach the Python backend.");
      console.error(err);
    } finally {
      setIsScheduling(false);
    }
  };

  return (
    <div className="flex flex-col gap-4">
      <div className="relative overflow-hidden rounded-xl border border-success/30 bg-gradient-to-r from-success/10 via-success/5 to-transparent p-6">
        {/* Decorative elements */}
        <div className="absolute -right-4 -top-4 h-24 w-24 rounded-full bg-success/10 blur-2xl" />
        <div className="absolute -right-8 -bottom-8 h-32 w-32 rounded-full bg-success/5 blur-3xl" />

        <div className="relative flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
          <div className="flex items-center gap-4">
            <div className="flex h-12 w-12 shrink-0 items-center justify-center rounded-xl bg-success/20">
              <CheckCircle2 className="h-6 w-6 text-success" />
            </div>
            <div>
              <div className="flex items-center gap-2">
                <h3 className="text-lg font-semibold text-foreground">
                  Candidate Approved!
                </h3>
                <PartyPopper className="h-5 w-5 text-success" />
              </div>
              <p className="text-sm text-muted-foreground mt-0.5">
                <span className="font-medium text-foreground">{candidateName}</span> has been shortlisted and is ready for the next stage
              </p>
            </div>
          </div>

          <Button
            onClick={handleScheduleClick}
            disabled={isScheduling || scheduleData !== null}
            className="bg-success hover:bg-success/90 text-success-foreground font-semibold shadow-lg shadow-success/20 transition-all duration-200"
          >
            <Calendar className="mr-2 h-4 w-4" />
            {isScheduling ? "Processing..." : scheduleData ? "Scheduled!" : "Approve & Schedule Interview"}
          </Button>
        </div>
      </div>

      {/* This section will magically appear once the AI returns the draft */}
      {scheduleData && (
        <div className="p-5 rounded-xl border border-success/30 bg-success/5 animate-in fade-in slide-in-from-top-4">
          <h4 className="font-semibold text-success mb-3 flex items-center gap-2">
            <CheckCircle2 className="h-5 w-5" />
            Interview Scheduled & AI Email Drafted
          </h4>
          <div className="space-y-4">
            <div>
              <span className="text-xs font-bold uppercase tracking-wider text-muted-foreground block mb-1">Calendar Link</span>
              <a href={scheduleData.invite_link} target="_blank" rel="noreferrer" className="text-sm text-blue-600 hover:text-blue-800 underline transition-colors">
                {scheduleData.invite_link}
              </a>
            </div>
            <div>
              <span className="text-xs font-bold uppercase tracking-wider text-muted-foreground block mb-1">Draft Email to Candidate</span>
              <textarea
                readOnly
                className="w-full h-40 p-4 text-sm rounded-lg border border-border bg-background resize-none focus:ring-1 focus:ring-success outline-none"
                value={scheduleData.email_body}
              />
            </div>
          </div>
        </div>
      )}
    </div>
  );
}