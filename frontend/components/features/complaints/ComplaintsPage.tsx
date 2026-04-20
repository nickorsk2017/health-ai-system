"use client";

import { useState } from "react";
import { Sparkles } from "lucide-react";

import Alert from "@/components/common/Alert/Alert";
import AddComplaintsByPromptModal from "@/components/features/complaints/AddComplaintsByPromptModal";
import ComplaintList from "@/components/features/complaints/ComplaintList";
import { useRole } from "@/contexts/RoleContext";
import { usePatientStore } from "@/stores/usePatientStore";

export default function ComplaintsPage() {
  const { role } = useRole();
  const { selectedPatientId } = usePatientStore();
  const [modalOpen, setModalOpen] = useState(false);
  const [promptSuccess, setPromptSuccess] = useState(false);

  const isDoctor = role === "doctor";
  const userId = selectedPatientId ?? "";

  if (!selectedPatientId) {
    return (
      <div className="flex items-center justify-center py-20 text-sm text-slate-500">
        Select a patient to view complaints.
      </div>
    );
  }

  const handleSuccess = () => {
    setModalOpen(false);
    setPromptSuccess(true);
  };

  return (
    <div className="flex flex-col gap-6 p-6">
      {!isDoctor && (
        <div className="flex justify-end">
          <button
            type="button"
            onClick={() => setModalOpen(true)}
            className="inline-flex animate-breathe cursor-pointer items-center gap-2 rounded-lg bg-violet-600 px-4 py-2 text-sm font-medium text-white will-change-transform hover:scale-105 hover:brightness-110 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-violet-500 focus-visible:ring-offset-1"
          >
            <Sparkles className="h-4 w-4" />
            Add complaints by prompt
          </button>
        </div>
      )}

      {promptSuccess && (
        <Alert
          variant="success"
          message="Complaints saved successfully. The list has been refreshed."
          onDismiss={() => setPromptSuccess(false)}
        />
      )}

      <ComplaintList userId={userId} isDoctor={isDoctor} />

      {!isDoctor && (
        <AddComplaintsByPromptModal
          isOpen={modalOpen}
          userId={userId}
          onClose={() => setModalOpen(false)}
          onSuccess={handleSuccess}
        />
      )}
    </div>
  );
}
