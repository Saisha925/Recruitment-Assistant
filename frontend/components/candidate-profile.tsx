"use client";

import type { Candidate } from "@/components/dashboard";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { User, Mail, GraduationCap, Code2 } from "lucide-react";

interface CandidateProfileProps {
  candidate: Candidate | null;
}

export function CandidateProfile({ candidate }: CandidateProfileProps) {
  return (
    <Card className="border-border/50 shadow-sm hover:shadow-md transition-shadow duration-200">
      <CardHeader className="pb-4">
        <CardTitle className="flex items-center gap-2 text-lg font-semibold text-card-foreground">
          <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-primary/10">
            <User className="h-4 w-4 text-primary" />
          </div>
          Candidate Profile
        </CardTitle>
      </CardHeader>
      <CardContent>
        {candidate ? (
          <div className="space-y-4">
            {/* Name */}
            <div className="flex items-start gap-3">
              <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-full bg-primary/10 text-primary font-semibold">
                {candidate.name.charAt(0)}
              </div>
              <div>
                <p className="font-semibold text-foreground text-lg">{candidate.name}</p>
                <div className="flex items-center gap-1.5 text-sm text-muted-foreground mt-0.5">
                  <Mail className="h-3.5 w-3.5" />
                  {candidate.email}
                </div>
              </div>
            </div>

            {/* Education */}
            <div className="flex items-start gap-3 pt-2 border-t border-border/50">
              <div className="flex h-8 w-8 shrink-0 items-center justify-center rounded-lg bg-muted">
                <GraduationCap className="h-4 w-4 text-muted-foreground" />
              </div>
              <div>
                <p className="text-xs font-medium text-muted-foreground uppercase tracking-wide">Education</p>
                <p className="text-sm text-foreground mt-0.5">{candidate.education}</p>
              </div>
            </div>

            {/* Skills */}
            <div className="flex items-start gap-3 pt-2 border-t border-border/50">
              <div className="flex h-8 w-8 shrink-0 items-center justify-center rounded-lg bg-muted">
                <Code2 className="h-4 w-4 text-muted-foreground" />
              </div>
              <div className="flex-1">
                <p className="text-xs font-medium text-muted-foreground uppercase tracking-wide mb-2">Skills</p>
                <div className="flex flex-wrap gap-1.5">
                  {candidate.skills.map((skill) => (
                    <Badge
                      key={skill}
                      variant="secondary"
                      className="bg-primary/10 text-primary border-0 font-medium text-xs"
                    >
                      {skill}
                    </Badge>
                  ))}
                </div>
              </div>
            </div>
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
