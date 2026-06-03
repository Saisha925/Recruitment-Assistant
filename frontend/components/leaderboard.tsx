"use client";

import type { LeaderboardEntry } from "@/components/dashboard";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import { Trophy, CheckCircle2, XCircle, Clock, TrendingUp } from "lucide-react";
import { cn } from "@/lib/utils";

interface LeaderboardProps {
  entries: LeaderboardEntry[];
  onSelectCandidate: (index: number) => void;
  selectedIndex: number;
}

export function Leaderboard({ entries, onSelectCandidate, selectedIndex }: LeaderboardProps) {
  const getStatusConfig = (status: LeaderboardEntry["status"]) => {
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

  const getRankBadge = (rank: number) => {
    if (rank === 1)
      return (
        <div className="flex h-7 w-7 items-center justify-center rounded-full bg-yellow-100 text-yellow-700 font-bold text-sm">
          1
        </div>
      );
    if (rank === 2)
      return (
        <div className="flex h-7 w-7 items-center justify-center rounded-full bg-gray-100 text-gray-600 font-bold text-sm">
          2
        </div>
      );
    if (rank === 3)
      return (
        <div className="flex h-7 w-7 items-center justify-center rounded-full bg-orange-100 text-orange-700 font-bold text-sm">
          3
        </div>
      );
    return (
      <div className="flex h-7 w-7 items-center justify-center rounded-full bg-muted text-muted-foreground font-medium text-sm">
        {rank}
      </div>
    );
  };

  const getScoreColor = (score: number) => {
    if (score >= 80) return "text-success font-semibold";
    if (score >= 60) return "text-chart-4 font-semibold";
    return "text-destructive font-semibold";
  };

  return (
    <Card className="border-border/50 shadow-sm">
      <CardHeader className="pb-4">
        <CardTitle className="flex items-center gap-2 text-lg font-semibold text-card-foreground">
          <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-primary/10">
            <Trophy className="h-4 w-4 text-primary" />
          </div>
          Candidate Leaderboard
          {entries.length > 0 && (
            <Badge variant="secondary" className="ml-auto font-medium">
              {entries.length} candidates
            </Badge>
          )}
        </CardTitle>
      </CardHeader>
      <CardContent>
        {entries.length > 0 ? (
          <div className="rounded-xl border border-border/50 overflow-hidden">
            <Table>
              <TableHeader>
                <TableRow className="bg-muted/30 hover:bg-muted/30">
                  <TableHead className="w-20 text-center font-semibold">Rank</TableHead>
                  <TableHead className="font-semibold">Candidate Email</TableHead>
                  <TableHead className="w-24 text-center font-semibold">Score</TableHead>
                  <TableHead className="w-32 text-center font-semibold">Status</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {entries.map((entry, index) => {
                  const config = getStatusConfig(entry.status);
                  const Icon = config.icon;
                  return (
                    <TableRow
                      key={entry.email}
                      className={cn(
                        "cursor-pointer transition-colors",
                        selectedIndex === index
                          ? "bg-primary/5 hover:bg-primary/10"
                          : "hover:bg-muted/50"
                      )}
                      onClick={() => onSelectCandidate(index)}
                    >
                      <TableCell className="text-center">
                        <div className="flex justify-center">{getRankBadge(entry.rank)}</div>
                      </TableCell>
                      <TableCell>
                        <span className={cn(
                          "text-sm",
                          selectedIndex === index ? "text-primary font-medium" : "text-foreground"
                        )}>
                          {entry.email}
                        </span>
                      </TableCell>
                      <TableCell className="text-center">
                        <span className={getScoreColor(entry.score)}>{entry.score}</span>
                      </TableCell>
                      <TableCell className="text-center">
                        <Badge
                          variant="outline"
                          className={cn(
                            "inline-flex items-center gap-1 px-2 py-0.5 text-xs font-medium",
                            config.className
                          )}
                        >
                          <Icon className="h-3 w-3" />
                          {config.label}
                        </Badge>
                      </TableCell>
                    </TableRow>
                  );
                })}
              </TableBody>
            </Table>
          </div>
        ) : (
          <div className="flex flex-col items-center justify-center py-12 text-center">
            <div className="flex h-16 w-16 items-center justify-center rounded-2xl bg-muted mb-4">
              <TrendingUp className="h-8 w-8 text-muted-foreground" />
            </div>
            <p className="text-sm font-medium text-muted-foreground">No rankings yet</p>
            <p className="text-xs text-muted-foreground mt-1">
              Run the AI pipeline to generate the leaderboard
            </p>
          </div>
        )}
      </CardContent>
    </Card>
  );
}
