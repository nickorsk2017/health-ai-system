"use client";

import { useState } from "react";

import Alert from "@/components/common/Alert/Alert";
import Button from "@/components/common/Button/Button";
import Modal from "@/components/common/Modal/Modal";
import TextArea from "@/components/common/TextArea/TextArea";
import { useComplaintStore } from "@/stores/useComplaintStore";

type Props = {
  isOpen: boolean;
  userId: string;
  onClose: () => void;
  onSuccess: () => void;
};

export default function AddComplaintsByPromptModal({ isOpen, userId, onClose, onSuccess }: Props) {
  const { isProcessingPrompt, promptError, submitByPrompt, clearPromptError } = useComplaintStore();
  const [prompt, setPrompt] = useState("");

  const handleClose = () => {
    setPrompt("");
    clearPromptError();
    onClose();
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    const ok = await submitByPrompt({ user_id: userId, prompt });
    if (ok) {
      setPrompt("");
      onSuccess();
    }
  };

  return (
    <Modal
      isOpen={isOpen}
      title="Add complaints by prompt"
      onClose={handleClose}
      className="max-w-xl"
    >
      <form onSubmit={handleSubmit} className="flex flex-col gap-4">
        <p className="text-sm text-slate-500">
          Describe your health concerns in plain language. Our AI will extract and save each
          complaint automatically.
        </p>
        <TextArea
          label="Health concerns"
          value={prompt}
          rows={8}
          placeholder={`e.g. I've had a headache since yesterday morning. Last Monday I noticed my right knee was swollen after a run. I also had a fever two days ago that went away on its own.`}
          onChange={setPrompt}
        />
        {promptError && <Alert message={promptError} onDismiss={clearPromptError} />}
        <div className="flex items-center justify-end gap-2 border-t border-slate-100 pt-4">
          <Button variant="ghost" type="button" onClick={handleClose}>
            Cancel
          </Button>
          <Button type="submit" loading={isProcessingPrompt} disabled={!prompt.trim()}>
            Process & Save
          </Button>
        </div>
      </form>
    </Modal>
  );
}
