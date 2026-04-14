"use client";

import { useState } from "react";

import Alert from "@/components/common/Alert/Alert";
import Button from "@/components/common/Button/Button";
import Input from "@/components/common/Input/Input";
import Modal from "@/components/common/Modal/Modal";
import Select from "@/components/common/Select/Select";
import { usePatientStore } from "@/stores/usePatientStore";

const GENDER_OPTIONS = [
  { value: "male", label: "Male" },
  { value: "female", label: "Female" },
  { value: "other", label: "Other" },
];

const EMPTY: Entity.NewPatientForm = {
  name: "",
  date_of_birth: "1980-01-01",
  gender: "male",
  email: "",
};

type Props = {
  isOpen: boolean;
  onClose: () => void;
};

export default function AddPatientModal({ isOpen, onClose }: Props) {
  const { createPatient, isCreating, createError, clearCreateError } = usePatientStore();
  const [form, setForm] = useState<Entity.NewPatientForm>(EMPTY);
  const [validationError, setValidationError] = useState<string | null>(null);

  const set = <K extends keyof Entity.NewPatientForm>(key: K, value: Entity.NewPatientForm[K]) =>
    setForm((prev) => ({ ...prev, [key]: value }));

  const handleClose = () => {
    setForm(EMPTY);
    setValidationError(null);
    clearCreateError();
    onClose();
  };

  const handleSave = async () => {
    if (!form.name.trim()) {
      setValidationError("Full name is required.");
      return;
    }
    if (!form.date_of_birth) {
      setValidationError("Date of birth is required.");
      return;
    }
    if (!form.email.trim()) {
      setValidationError("Email is required.");
      return;
    }
    setValidationError(null);
    await createPatient(form);
  };

  const error = validationError ?? createError;

  return (
    <Modal isOpen={isOpen} title="Add New Patient" onClose={handleClose}>
      <div className="flex flex-col gap-4">
        <Input
          label="Full Name"
          value={form.name}
          placeholder="e.g. Sarah Connor"
          onChange={(v) => set("name", v)}
          autofocus
        />
        <Input
          label="Date of Birth"
          type="date"
          value={form.date_of_birth}
          max={new Date().toISOString().split("T")[0]}
          onChange={(v) => set("date_of_birth", v)}
        />
        <Input
          label="Email"
          type="email"
          value={form.email}
          placeholder="e.g. sarah@example.com"
          onChange={(v) => set("email", v)}
        />
        <Select
          label="Gender"
          value={form.gender}
          options={GENDER_OPTIONS}
          onChange={(v) => set("gender", v as Entity.Gender)}
        />
        {error && (
          <Alert
            message={error}
            onDismiss={() => {
              setValidationError(null);
              clearCreateError();
            }}
          />
        )}
        <div className="flex justify-end gap-2 pt-2">
          <Button variant="secondary" onClick={handleClose} disabled={isCreating}>
            Cancel
          </Button>
          <Button loading={isCreating} onClick={handleSave}>
            Add Patient
          </Button>
        </div>
      </div>
    </Modal>
  );
}
