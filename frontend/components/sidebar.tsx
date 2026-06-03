"use client";

import { useCallback } from "react";
import { useDropzone } from "react-dropzone";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { Label } from "@/components/ui/label";
import { 
  Upload, 
  FileText, 
  Play, 
  Briefcase,
  X,
  CheckCircle2
} from "lucide-react";
import { cn } from "@/lib/utils";

interface SidebarProps {
  selectedRole: string;
  onRoleChange: (role: string) => void;
  uploadedFile: File | null;
  onFileUpload: (file: File | null) => void;
  onRunPipeline: () => void;
  isPipelineRunning: boolean;
  canRunPipeline: boolean;
}

const roles = [
  { value: "REQ-101", label: "REQ-101: AI/ML Engineer" },
  { value: "REQ-102", label: "REQ-102: Data Scientist" },
];

export function Sidebar({
  selectedRole,
  onRoleChange,
  uploadedFile,
  onFileUpload,
  onRunPipeline,
  isPipelineRunning,
  canRunPipeline,
}: SidebarProps) {
  const onDrop = useCallback(
    (acceptedFiles: File[]) => {
      if (acceptedFiles.length > 0) {
        onFileUpload(acceptedFiles[0]);
      }
    },
    [onFileUpload]
  );

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      "application/pdf": [".pdf"],
    },
    maxFiles: 1,
    multiple: false,
  });

  return (
    <aside className="fixed left-0 top-16 h-[calc(100vh-4rem)] w-80 border-r border-border/50 bg-sidebar p-6 overflow-y-auto">
      <div className="space-y-6">
        {/* Role Selector */}
        <Card className="border-border/50 shadow-sm">
          <CardHeader className="pb-3">
            <CardTitle className="flex items-center gap-2 text-base font-semibold text-card-foreground">
              <Briefcase className="h-4 w-4 text-primary" />
              Target Role
            </CardTitle>
          </CardHeader>
          <CardContent>
            <Label htmlFor="role-select" className="sr-only">
              Select Target Role
            </Label>
            <Select value={selectedRole} onValueChange={onRoleChange}>
              <SelectTrigger id="role-select" className="h-11 border-border/80">
                <SelectValue placeholder="Select target role..." />
              </SelectTrigger>
              <SelectContent>
                {roles.map((role) => (
                  <SelectItem key={role.value} value={role.value}>
                    {role.label}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
          </CardContent>
        </Card>

        {/* File Upload */}
        <Card className="border-border/50 shadow-sm">
          <CardHeader className="pb-3">
            <CardTitle className="flex items-center gap-2 text-base font-semibold text-card-foreground">
              <FileText className="h-4 w-4 text-primary" />
              Resume Upload
            </CardTitle>
          </CardHeader>
          <CardContent>
            {!uploadedFile ? (
              <div
                {...getRootProps()}
                className={cn(
                  "relative cursor-pointer rounded-xl border-2 border-dashed p-6 transition-all duration-200",
                  isDragActive
                    ? "border-primary bg-primary/5"
                    : "border-border/80 hover:border-primary/50 hover:bg-muted/30"
                )}
              >
                <input {...getInputProps()} />
                <div className="flex flex-col items-center gap-3 text-center">
                  <div className={cn(
                    "flex h-12 w-12 items-center justify-center rounded-xl transition-colors",
                    isDragActive ? "bg-primary/10 text-primary" : "bg-muted text-muted-foreground"
                  )}>
                    <Upload className="h-6 w-6" />
                  </div>
                  <div>
                    <p className="text-sm font-medium text-foreground">
                      {isDragActive ? "Drop your resume here" : "Drag & drop resume"}
                    </p>
                    <p className="mt-1 text-xs text-muted-foreground">
                      or click to browse (PDF only)
                    </p>
                  </div>
                </div>
              </div>
            ) : (
              <div className="flex items-center gap-3 rounded-xl border border-success/30 bg-success/5 p-4">
                <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-success/10">
                  <CheckCircle2 className="h-5 w-5 text-success" />
                </div>
                <div className="flex-1 min-w-0">
                  <p className="text-sm font-medium text-foreground truncate">
                    {uploadedFile.name}
                  </p>
                  <p className="text-xs text-muted-foreground">
                    {(uploadedFile.size / 1024).toFixed(1)} KB
                  </p>
                </div>
                <Button
                  variant="ghost"
                  size="icon"
                  className="h-8 w-8 text-muted-foreground hover:text-destructive"
                  onClick={() => onFileUpload(null)}
                >
                  <X className="h-4 w-4" />
                </Button>
              </div>
            )}
          </CardContent>
        </Card>

        {/* Run Pipeline Button */}
        <Button
          onClick={onRunPipeline}
          disabled={!canRunPipeline || isPipelineRunning}
          className="w-full h-12 text-base font-semibold bg-primary hover:bg-primary/90 text-primary-foreground shadow-lg shadow-primary/20 transition-all duration-200 disabled:opacity-50 disabled:shadow-none"
        >
          {isPipelineRunning ? (
            <div className="flex items-center gap-2">
              <div className="h-5 w-5 animate-spin rounded-full border-2 border-primary-foreground border-t-transparent" />
              Processing...
            </div>
          ) : (
            <div className="flex items-center gap-2">
              <Play className="h-5 w-5" />
              Run AI Pipeline
            </div>
          )}
        </Button>

        {/* Help Text */}
        <p className="text-xs text-center text-muted-foreground px-2">
          Select a target role and upload a resume to analyze candidates with AI
        </p>
      </div>
    </aside>
  );
}
