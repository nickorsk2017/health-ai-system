"use client";

import { useEffect, useState } from "react";
import { AlertTriangle } from "lucide-react";
import { toast } from "sonner";

import Alert from "@/components/common/Alert/Alert";
import Button from "@/components/common/Button/Button";
import Modal from "@/components/common/Modal/Modal";
import TextArea from "@/components/common/TextArea/TextArea";
import { useAnalysisStore } from "@/stores/useAnalysisStore";
import { usePatientStore } from "@/stores/usePatientStore";

type Props = {
  isOpen: boolean;
  onClose: () => void;
};

export default function ImportLabsModal({ isOpen, onClose }: Props) {
  const { selectedPatientId } = usePatientStore();
  const {
    isImporting,
    importError,
    missingAnalyses,
    importFromPrompt,
    clearImportError,
    clearMissingAnalyses,
  } = useAnalysisStore();
  const [prompt, setPrompt] = useState("");

  useEffect(() => {
    if (isOpen) {
      setPrompt("");
      clearImportError();
      clearMissingAnalyses();
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [isOpen]);

  const handleClose = () => {
    clearImportError();
    clearMissingAnalyses();
    onClose();
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    const response = await importFromPrompt({ user_id: selectedPatientId!, prompt });
    if (!response) return;

    if (response.list_missing_analysis.length === 0) {
      toast.success("Lab results imported successfully.");
      handleClose();
    }
  };

  const hasMissing = missingAnalyses.length > 0;

  return (
    <Modal isOpen={isOpen} title="Add Labs by prompt" onClose={handleClose} className="max-w-xl">
      {!hasMissing ? (
        <form onSubmit={handleSubmit} className="flex flex-col gap-4">
          <p className="text-sm text-slate-500">
            Paste raw lab notes. Our AI will parse them into individual analysis records
            automatically.
          </p>
          <TextArea
            label="Lab notes"
            value={prompt}
            rows={8}
            placeholder={`e.g. March 5: Glucose 105 mg/dL, HbA1c 5.7%, Creatinine 0.9 mg/dL\n\nMarch 20: CBC — WBC 6.2, RBC 4.8, HGB 14.2 g/dL, PLT 220`}
            onChange={setPrompt}
          />
          {importError && <Alert message={importError} onDismiss={clearImportError} />}
          <div className="flex items-center justify-end gap-2 border-t border-slate-100 pt-4">
            <Button variant="ghost" type="button" onClick={handleClose}>
              Cancel
            </Button>
            <Button type="submit" loading={isImporting} disabled={!prompt.trim()}>
              Import
            </Button>
          </div>
        </form>
      ) : (
        <div className="flex flex-col gap-4">
          <div className="rounded-lg border border-yellow-200 bg-yellow-50 p-4">
            <div className="mb-3 flex items-center gap-2">
              <AlertTriangle className="h-4 w-4 shrink-0 text-yellow-600" />
              <span className="text-sm font-semibold text-yellow-800">
                Some data is incomplete
              </span>
            </div>
            <ul className="mb-3 list-inside list-disc space-y-1 text-sm text-yellow-700">
              {missingAnalyses.map((entry, i) => (
                <li key={i}>{entry}</li>
              ))}
            </ul>
            <p className="text-xs text-yellow-600">
              These records were saved. Please edit them manually in the analysis history.
            </p>
          </div>
          <div className="flex justify-end border-t border-slate-100 pt-4">
            <Button onClick={handleClose}>Close</Button>
          </div>
        </div>
      )}
    </Modal>
  );
}
