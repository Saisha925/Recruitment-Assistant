"use client";

import { Button } from "@/components/ui/button";
import { CheckCircle2, Calendar, PartyPopper } from "lucide-react";

interface SuccessBannerProps {
  candidateName: string;
}

export function SuccessBanner({ candidateName }: SuccessBannerProps) {
  return (
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
        
        <Button className="bg-success hover:bg-success/90 text-success-foreground font-semibold shadow-lg shadow-success/20 transition-all duration-200">
          <Calendar className="mr-2 h-4 w-4" />
          Approve & Schedule Interview
        </Button>
      </div>
    </div>
  );
}
