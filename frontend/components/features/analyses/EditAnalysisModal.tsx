"use client";

import { useEffect, useState } from "react";
import { Trash2 } from "lucide-react";
import { toast } from "sonner";

import Alert from "@/components/common/Alert/Alert";
import Button from "@/components/common/Button/Button";
import Input from "@/components/common/Input/Input";
import Modal from "@/components/common/Modal/Modal";
import TextArea from "@/components/common/TextArea/TextArea";
import { useAnalysisStore } from "@/stores/useAnalysisStore";

type Props = {
  record: Entity.AnalysisRecord;
  isOpen: boolean;
  onClose: () => void;
};

const TODAY = new Date().toISOString().split("T")[0];

export default function EditAnalysisModal({ record, isOpen, onClose }: Props) {
  const { isUpdating, isDeleting, editError, updateAnalysis, deleteAnalysis, clearEditError } =
    useAnalysisStore();
  const [form, setForm] = useState<Entity.UpdateAnalysis>({
    analysis_text: record.analysis_text,
    analysis_date: record.analysis_date,
  });
  const [confirmDelete, setConfirmDelete] = useState(false);

  useEffect(() => {
    if (isOpen) {
      setForm({ analysis_text: record.analysis_text, analysis_date: record.analysis_date });
      setConfirmDelete(false);
      clearEditError();
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [isOpen]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    const ok = await updateAnalysis(record.analysis_id, form);
    if (ok) {
      toast.success("Analysis updated successfully.");
      onClose();
    } else {
      toast.error("Failed to update analysis.");
    }
  };

  const handleDelete = async () => {
    if (!confirmDelete) {
      setConfirmDelete(true);
      return;
    }
    const ok = await deleteAnalysis(record.analysis_id);
    if (ok) {
      toast.success("Analysis deleted.");
      onClose();
    } else {
      toast.error("Failed to delete analysis.");
    }
  };

  return (
    <Modal isOpen={isOpen} title="Edit Analysis" onClose={onClose} className="max-w-2xl">
      <form onSubmit={handleSubmit} className="flex flex-col gap-4">
        <Input
          label="Analysis Date"
          type="date"
          value={form.analysis_date ?? ""}
          min="2000-01-01"
          max={TODAY}
          onChange={(v) => setForm((prev) => ({ ...prev, analysis_date: v || null }))}
        />
        <TextArea
          label="Lab Results"
          value={form.analysis_text ?? ""}
          rows={7}
          placeholder="Paste or type lab results here, e.g. Glucose: 105 mg/dL, HbA1c: 5.7%..."
          onChange={(v) => setForm((prev) => ({ ...prev, analysis_text: v || null }))}
        />
        {editError && <Alert message={editError} onDismiss={clearEditError} />}
        <div className="flex items-center justify-between border-t border-slate-100 pt-4">
          <Button
            type="button"
            variant="ghost"
            loading={isDeleting}
            onClick={handleDelete}
            className={
              confirmDelete
                ? "text-red-600 bg-red-100 hover:bg-red-200"
                : "text-red-500 bg-red-50 hover:bg-red-100"
            }
          >
            <Trash2 className="h-4 w-4" />
            {confirmDelete ? "Confirm Delete" : "Delete"}
          </Button>
          <div className="flex items-center gap-2">
            <Button variant="ghost" type="button" onClick={onClose}>
              Cancel
            </Button>
            <Button type="submit" loading={isUpdating}>
              Save Changes
            </Button>
          </div>
        </div>
      </form>
    </Modal>
  );
}
