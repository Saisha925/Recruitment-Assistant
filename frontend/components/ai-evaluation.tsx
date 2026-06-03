"use client";

import type { Evaluation } from "@/components/dashboard";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Brain, CheckCircle2, XCircle, Clock } from "lucide-react";
import { cn } from "@/lib/utils";

interface AIEvaluationProps {
  evaluation: Evaluation | null;
  isLoading?: boolean;
}

export function AIEvaluation({ evaluation, isLoading }: AIEvaluationProps) {
  const getStatusConfig = (status: Evaluation["status"]) => {
    switch (status) {
      case "shortlisted":
        return {
          icon: CheckCircle2,
          label: "Shortlisted",
          className: "bg-success/10 text-success border-success/20",
        };
      case "rejected":
        return {
          icon: XCircle,
          label: "Rejected",
          className: "bg-destructive/10 text-destructive border-destructive/20",
        };
      default:
        return {
          icon: Clock,
          label: "Pending",
          className: "bg-muted text-muted-foreground border-border",
        };
    }
  };

  const getScoreColor = (score: number) => {
    if (score >= 80) return "text-success";
    if (score >= 60) return "text-chart-4";
    return "text-destructive";
  };

  return (
    <Card className="border-border/50 shadow-sm hover:shadow-md transition-shadow duration-200">
      <CardHeader className="pb-4">
        <CardTitle className="flex items-center gap-2 text-lg font-semibold text-card-foreground">
          <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-primary/10">
            <Brain className="h-4 w-4 text-primary" />
          </div>
          AI Evaluation
        </CardTitle>
      </CardHeader>
      <CardContent>
        {isLoading ? (
          <div className="flex flex-col items-center justify-center py-8 text-center">
            <div className="relative flex h-20 w-20 items-center justify-center mb-4">
              <div className="absolute inset-0 rounded-full border-4 border-primary/20" />
              <div className="absolute inset-0 rounded-full border-4 border-primary border-t-transparent animate-spin" />
              <Brain className="h-8 w-8 text-primary" />
            </div>
            <p className="text-sm font-medium text-foreground">Analyzing candidate...</p>
            <p className="text-xs text-muted-foreground mt-1">AI is evaluating the resume</p>
          </div>
        ) : evaluation ? (
          <div className="space-y-4">
            {/* Score and Status */}
            <div className="flex items-center justify-between">
              {/* Score Circle */}
              <div className="flex items-center gap-4">
                <div className="relative flex h-20 w-20 items-center justify-center">
                  <svg className="absolute inset-0 -rotate-90" viewBox="0 0 100 100">
                    <circle
                      cx="50"
                      cy="50"
                      r="42"
                      fill="none"
                      stroke="currentColor"
                      strokeWidth="8"
                      className="text-muted"
                    />
                    <circle
                      cx="50"
                      cy="50"
                      r="42"
                      fill="none"
                      stroke="currentColor"
                      strokeWidth="8"
                      strokeLinecap="round"
                      strokeDasharray={`${evaluation.matchScore * 2.64} 264`}
                      className={getScoreColor(evaluation.matchScore)}
                    />
                  </svg>
                  <div className="text-center">
                    <span className={cn("text-2xl font-bold", getScoreColor(evaluation.matchScore))}>
                      {evaluation.matchScore}
                    </span>
                    <span className="text-xs text-muted-foreground block">/100</span>
                  </div>
                </div>
                <div>
                  <p className="text-xs font-medium text-muted-foreground uppercase tracking-wide">Match Score</p>
                  <p className="text-sm text-foreground mt-0.5">
                    {evaluation.matchScore >= 80
                      ? "Excellent match"
                      : evaluation.matchScore >= 60
                      ? "Good match"
                      : "Low match"}
                  </p>
                </div>
              </div>

              {/* Status Badge */}
              {(() => {
                const config = getStatusConfig(evaluation.status);
                const Icon = config.icon;
                return (
                  <Badge
                    variant="outline"
                    className={cn("flex items-center gap-1.5 px-3 py-1.5 text-sm font-medium", config.className)}
                  >
                    <Icon className="h-4 w-4" />
                    {config.label}
                  </Badge>
                );
              })()}
            </div>

            {/* AI Reasoning */}
            <div className="pt-3 border-t border-border/50">
              <p className="text-xs font-medium text-muted-foreground uppercase tracking-wide mb-2">
                AI Reasoning
              </p>
              <p className="text-sm text-foreground leading-relaxed">
                {evaluation.reasoning}
              </p>
            </div>
          </div>
        ) : (
          <div className="flex flex-col items-center justify-center py-8 text-center">
            <div className="flex h-16 w-16 items-center justify-center rounded-2xl bg-muted mb-4">
              <Brain className="h-8 w-8 text-muted-foreground" />
            </div>
            <p className="text-sm font-medium text-muted-foreground">No evaluation yet</p>
            <p className="text-xs text-muted-foreground mt-1">Run the AI pipeline to get insights</p>
          </div>
        )}
      </CardContent>
    </Card>
  );
}
