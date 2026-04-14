"use client";

import { useEffect, useState } from "react";
import { Activity } from "lucide-react";

import Spinner from "@/components/common/Spinner/Spinner";
import { usePatientStore } from "@/stores/usePatientStore";

import AddPatientModal from "./AddPatientModal";

export default function PatientGuard() {
  const { isInitialized, selectedPatientId, patients, setSelectedPatientId, initError, init } =
    usePatientStore();
  const [localSelection, setLocalSelection] = useState("");
  const [modalOpen, setModalOpen] = useState(false);

  useEffect(() => {
    init();
  }, []);

  useEffect(() => {
    if (patients.length > 0) setLocalSelection(patients[0].id);
  }, [patients]);

  if (!isInitialized) {
    return (
      <div className="fixed inset-0 z-50 flex items-center justify-center bg-white">
        <Spinner size="lg" />
      </div>
    );
  }

  if (selectedPatientId) return null;

  return (
    <>
      <div className="fixed inset-0 z-40 flex items-center justify-center bg-slate-900/60 backdrop-blur-sm p-4">
        <div className="w-full max-w-sm rounded-2xl border border-slate-200 bg-white p-8 shadow-2xl">
          <div className="mb-6 flex flex-col items-center gap-3 text-center">
            <div className="flex h-12 w-12 items-center justify-center rounded-xl bg-blue-600">
              <Activity className="h-6 w-6 text-white" />
            </div>
            <h1 className="text-lg font-semibold text-slate-800">AI Health System</h1>
            <p className="text-sm text-slate-500">
              Please select or add a patient to continue.
            </p>
          </div>

          {initError && (
            <p className="mb-4 rounded-lg bg-red-50 px-3 py-2 text-center text-xs text-red-600">
              {initError}
            </p>
          )}

          {patients.length > 0 && (
            <div className="mb-4 flex flex-col gap-2">
              <label className="text-xs font-medium text-slate-500">Select existing patient</label>
              <select
                value={localSelection}
                onChange={(e) => setLocalSelection(e.target.value)}
                className="rounded-lg border border-slate-300 bg-white px-3 py-2 text-sm text-slate-800 focus:border-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-500/20"
              >
                {patients.map((p) => (
                  <option key={p.id} value={p.id}>
                    {p.name}
                  </option>
                ))}
              </select>
              <button
                onClick={() => localSelection && setSelectedPatientId(localSelection)}
                className="w-full rounded-lg bg-blue-600 px-4 py-2 text-sm font-medium text-white hover:bg-blue-700"
              >
                Continue with {patients.find((p) => p.id === localSelection)?.name ?? "Patient"}
              </button>
            </div>
          )}

          <div className={patients.length > 0 ? "border-t border-slate-100 pt-4" : ""}>
            <button
              onClick={() => setModalOpen(true)}
              className="w-full rounded-lg border border-blue-200 bg-blue-50 px-4 py-2 text-sm font-medium text-blue-700 hover:bg-blue-100"
            >
              + Add New Patient
            </button>
          </div>
        </div>
      </div>

      <AddPatientModal isOpen={modalOpen} onClose={() => setModalOpen(false)} />
    </>
  );
}
