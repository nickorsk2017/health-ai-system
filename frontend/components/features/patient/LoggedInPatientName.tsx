"use client";

import { User } from "lucide-react";

import { usePatientStore } from "@/stores/usePatientStore";

export default function LoggedInPatientName() {
  const { patients, selectedPatientId, isInitialized } = usePatientStore();

  if (!isInitialized) {
    return <div className="h-7 w-36 animate-pulse rounded-lg bg-slate-200" />;
  }

  const name = patients.find((p) => p.id === selectedPatientId)?.name;
  if (!name) {
    return null;
  }

  return (
    <div className="flex items-center gap-2 rounded-lg border border-slate-200 bg-slate-50 px-3 py-1.5">
      <User className="h-4 w-4 shrink-0 text-slate-400" aria-hidden />
      <span className="text-sm text-slate-500">Signed in as</span>
      <span className="text-sm font-semibold text-slate-800">{name}</span>
    </div>
  );
}
