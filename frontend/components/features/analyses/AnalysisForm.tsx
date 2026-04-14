"use client";

import { useState } from "react";

import Alert from "@/components/common/Alert/Alert";
import Button from "@/components/common/Button/Button";
import Input from "@/components/common/Input/Input";
import TextArea from "@/components/common/TextArea/TextArea";
import { useAnalysisStore } from "@/stores/useAnalysisStore";
import { usePatientStore } from "@/stores/usePatientStore";

const TODAY = new Date().toISOString().split("T")[0];

const EMPTY = { analysis_date: TODAY, analysis_text: "" };

export default function AnalysisForm() {
  const { selectedPatientId } = usePatientStore();
  const { isSubmitting, submitError, submitAnalysis, clearSubmitError } = useAnalysisStore();
  const [form, setForm] = useState(EMPTY);
  const [success, setSuccess] = useState(false);

  const set = (key: keyof typeof EMPTY, value: string) =>
    setForm((prev) => ({ ...prev, [key]: value }));

  const handleSubmit = async (e: React.SubmitEvent<HTMLFormElement>) => {
    e.preventDefault();
    setSuccess(false);
    const ok = await submitAnalysis({ ...form, user_id: selectedPatientId! });
    if (ok) {
      setSuccess(true);
      setForm(EMPTY);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="flex flex-col gap-4">
      <Input
        label="Analysis Date"
        type="date"
        value={form.analysis_date}
        max={TODAY}
        onChange={(v) => set("analysis_date", v)}
        className="w-48"
      />
      <TextArea
        label="Lab Results"
        value={form.analysis_text}
        rows={7}
        placeholder="Paste or type lab results here, e.g. Glucose: 105 mg/dL, HbA1c: 5.7%, Calcium: 11.2 mg/dL..."
        onChange={(v) => set("analysis_text", v)}
      />
      {submitError && <Alert message={submitError} onDismiss={clearSubmitError} />}
      {success && (
        <Alert
          variant="success"
          message="Analysis saved successfully."
          onDismiss={() => setSuccess(false)}
        />
      )}
      <Button
        type="submit"
        loading={isSubmitting}
        disabled={!form.analysis_text.trim()}
        className="self-end"
      >
        Save Analysis
      </Button>
    </form>
  );
}
