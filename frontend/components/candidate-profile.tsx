"use client";

import { useState } from "react";

// 1. Defined locally to prevent cross-file import crashes
export interface Candidate {
  name: string;
  email: string;
  education: string;
  skills: string[];
}

// 2. Fixed relative imports (using ./ instead of @/components/)
import { Card, CardContent, CardHeader, CardTitle } from "./ui/card";
import { Badge } from "./ui/badge";
import { Button } from "./ui/button";
import { User, Mail, GraduationCap, Code2, Calendar } from "lucide-react";

interface Props {
  cand: Candidate | null;
  jobId?: string;
}

export function CandidateProfile({ cand, jobId = "REQ-101" }: Props) {
  const [ld, setLd] = useState(false);
  const [dt, setDt] = useState<{ email_body: string; invite_link: string } | null>(null);
  const [sts, setSts] = useState("Pending");

  const reqSch = async () => {
    // 🔴 THE TRIPWIRE: This proves the button is alive!
    alert("Button click registered! Starting request...");

    if (!cand) {
      alert("Error: No candidate data found.");
      return;
    }

    setLd(true);
    try {
      const res = await fetch("http://127.0.0.1:8000/api/schedule", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          cand_id: 1,
          name: cand.name,
          email: cand.email,
          job_id: jobId
        }),
      });

      const jsn = await res.json();

      if (res.ok && jsn.success) {
        setDt(jsn);
        setSts("Scheduled");
      } else {
        alert("Backend Error: " + (jsn.detail || "Unknown error"));
      }
    } catch (err) {
      alert("Network Error: Could not reach the Python backend.");
      console.error(err);
    } finally {
      setLd(false);
    }
  };

  return (
    <Card className="border-border/50 shadow-sm hover:shadow-md transition-shadow duration-200">
      <CardHeader className="pb-4 flex flex-row items-center justify-between">
        <CardTitle className="flex items-center gap-2 text-lg font-semibold text-card-foreground">
          <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-primary/10">
            <User className="h-4 w-4 text-primary" />
          </div>
          Candidate Profile
        </CardTitle>
        {cand && (
          <Button
            onClick={reqSch}
            disabled={ld || sts === "Scheduled"}
            className="bg-primary text-primary-foreground"
            size="sm"
          >
            {ld ? "Processing..." : sts === "Scheduled" ? "Scheduled" : "Approve & Schedule"}
          </Button>
        )}
      </CardHeader>
      <CardContent>
        {cand ? (
          <div className="space-y-4">
            <div className="flex items-start gap-3">
              <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-full bg-primary/10 text-primary font-semibold">
                {cand.name.charAt(0)}
              </div>
              <div>
                <p className="font-semibold text-foreground text-lg">{cand.name}</p>
                <div className="flex items-center gap-1.5 text-sm text-muted-foreground mt-0.5">
                  <Mail className="h-3.5 w-3.5" />
                  {cand.email}
                </div>
              </div>
            </div>

            <div className="flex items-start gap-3 pt-2 border-t border-border/50">
              <div className="flex h-8 w-8 shrink-0 items-center justify-center rounded-lg bg-muted">
                <GraduationCap className="h-4 w-4 text-muted-foreground" />
              </div>
              <div>
                <p className="text-xs font-medium text-muted-foreground uppercase tracking-wide">Education</p>
                <p className="text-sm text-foreground mt-0.5">{cand.education}</p>
              </div>
            </div>

            <div className="flex items-start gap-3 pt-2 border-t border-border/50">
              <div className="flex h-8 w-8 shrink-0 items-center justify-center rounded-lg bg-muted">
                <Code2 className="h-4 w-4 text-muted-foreground" />
              </div>
              <div className="flex-1">
                <p className="text-xs font-medium text-muted-foreground uppercase tracking-wide mb-2">Skills</p>
                <div className="flex flex-wrap gap-1.5">
                  {cand.skills.map((s) => (
                    <Badge
                      key={s}
                      variant="secondary"
                      className="bg-primary/10 text-primary border-0 font-medium text-xs"
                    >
                      {s}
                    </Badge>
                  ))}
                </div>
              </div>
            </div>

            {dt && (
              <div className="mt-4 p-4 border border-border/50 rounded-lg space-y-3 bg-muted/30">
                <div className="flex items-center gap-2">
                  <Calendar className="h-4 w-4 text-primary" />
                  <h3 className="font-semibold text-sm">Generated Communication</h3>
                </div>
                <div>
                  <p className="text-xs font-medium text-muted-foreground uppercase mb-1">Calendar Link</p>
                  <a href={dt.invite_link} target="_blank" rel="noreferrer" className="text-sm text-blue-500 hover:underline break-all">
                    {dt.invite_link}
                  </a>
                </div>
                <div>
                  <p className="text-xs font-medium text-muted-foreground uppercase mb-1">Email Draft</p>
                  <textarea
                    readOnly
                    value={dt.email_body}
                    className="w-full h-32 p-3 text-sm bg-background border border-border/50 rounded-md resize-none focus:outline-none"
                  />
                </div>
              </div>
            )}
          </div>
        ) : (
          <div className="flex flex-col items-center justify-center py-8 text-center">
            <div className="flex h-16 w-16 items-center justify-center rounded-2xl bg-muted mb-4">
              <User className="h-8 w-8 text-muted-foreground" />
            </div>
            <p className="text-sm font-medium text-muted-foreground">No candidate selected</p>
            <p className="text-xs text-muted-foreground mt-1">Run the AI pipeline to analyze resumes</p>
          </div>
        )}
      </CardContent>
    </Card>
  );
}