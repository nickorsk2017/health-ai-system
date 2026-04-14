"use client";

import { useState } from "react";

import Button from "@/components/common/Button/Button";
import Input from "@/components/common/Input/Input";
import Modal from "@/components/common/Modal/Modal";
import TextArea from "@/components/common/TextArea/TextArea";
import { useComplaintStore } from "@/stores/useComplaintStore";

type Props = {
  isOpen: boolean;
  userId: string;
  onClose: () => void;
};

export default function AddComplaintModal({ isOpen, userId, onClose }: Props) {
  const { isSubmitting, submitError, createComplaint, clearSubmitError } = useComplaintStore();
  const [problemHealth, setProblemHealth] = useState("");
  const [datePublic, setDatePublic] = useState("");

  const handleClose = () => {
    setProblemHealth("");
    setDatePublic("");
    clearSubmitError();
    onClose();
  };

  const handleSubmit = async () => {
    if (!problemHealth.trim() || !datePublic) return;
    const ok = await createComplaint(userId, {
      problem_health: problemHealth.trim(),
      date_public: datePublic,
    });
    if (ok) handleClose();
  };

  return (
    <Modal isOpen={isOpen} title="Report Health Complaint" onClose={handleClose}>
      <div className="flex flex-col gap-4">
        <TextArea
          label="Health Problem"
          id="problem-health"
          value={problemHealth}
          placeholder="Describe your health concern..."
          rows={4}
          onChange={setProblemHealth}
        />
        <Input
          label="Date Noticed"
          id="date-public"
          type="date"
          value={datePublic}
          onChange={setDatePublic}
        />
        {submitError && (
          <p className="text-sm text-red-600">{submitError}</p>
        )}
        <div className="flex justify-end gap-2 pt-1">
          <Button variant="secondary" onClick={handleClose} disabled={isSubmitting}>
            Cancel
          </Button>
          <Button
            onClick={handleSubmit}
            loading={isSubmitting}
            disabled={!problemHealth.trim() || !datePublic}
          >
            Submit
          </Button>
        </div>
      </div>
    </Modal>
  );
}
