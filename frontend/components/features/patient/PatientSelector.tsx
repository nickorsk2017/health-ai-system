"use client";

import { useState } from "react";
import { Plus, User } from "lucide-react";

import { usePatientStore } from "@/stores/usePatientStore";

import AddPatientModal from "./AddPatientModal";

export default function PatientSelector() {
  const { patients, selectedPatientId, setSelectedPatientId, isInitialized } = usePatientStore();
  const [modalOpen, setModalOpen] = useState(false);

  if (!isInitialized) {
    return <div className="h-7 w-40 animate-pulse rounded-lg bg-slate-200" />;
  }

  return (
    <>
      <div className="flex items-center gap-2">
        <User className="h-4 w-4 text-slate-400" />
        <label htmlFor="patient-select" className="text-sm text-slate-500">
          Patient:
        </label>
        <select
          id="patient-select"
          value={selectedPatientId ?? ""}
          onChange={(e) => e.target.value && setSelectedPatientId(e.target.value)}
          className="rounded-lg border border-slate-200 bg-white px-2 py-1 text-sm font-medium text-slate-700 focus:border-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-500/20"
        >
          {patients.map((p) => (
            <option key={p.id} value={p.id}>
              {p.name}
            </option>
          ))}
        </select>
        <button
          onClick={() => setModalOpen(true)}
          title="Add new patient"
          className="flex h-7 w-7 items-center justify-center rounded-lg border border-blue-200 bg-blue-50 text-blue-600 transition-colors hover:bg-blue-100 hover:border-blue-300"
        >
          <Plus className="h-3.5 w-3.5" />
        </button>
      </div>

      <AddPatientModal isOpen={modalOpen} onClose={() => setModalOpen(false)} />
    </>
  );
}
