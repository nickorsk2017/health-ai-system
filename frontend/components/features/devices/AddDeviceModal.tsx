"use client";

import { useEffect, useState } from "react";

import Alert from "@/components/common/Alert/Alert";
import Button from "@/components/common/Button/Button";
import Input from "@/components/common/Input/Input";
import Modal from "@/components/common/Modal/Modal";
import Select from "@/components/common/Select/Select";
import { useDeviceStore } from "@/stores/useDeviceStore";

const ALL_DEVICE_OPTIONS: { value: Entity.DeviceType; label: string }[] = [
  { value: "oura_ring", label: "Oura Ring" },
  { value: "apple_health", label: "Apple Watch / Apple Health" },
];

type Props = {
  isOpen: boolean;
  userId: string;
  onClose: () => void;
};

export default function AddDeviceModal({ isOpen, userId, onClose }: Props) {
  const { devices, isAdding, addError, addDevice, clearAddError } = useDeviceStore();

  const connectedTypes = new Set(devices.map((d) => d.type_device));
  const availableOptions = ALL_DEVICE_OPTIONS.filter((opt) => !connectedTypes.has(opt.value));
  const allConnected = availableOptions.length === 0;

  const [typeDevice, setTypeDevice] = useState<Entity.DeviceType>(
    availableOptions[0]?.value ?? "oura_ring",
  );
  const [diagnosisMock, setDiagnosisMock] = useState("");

  useEffect(() => {
    if (availableOptions.length > 0 && !availableOptions.some((o) => o.value === typeDevice)) {
      setTypeDevice(availableOptions[0].value);
    }
  }, [availableOptions, typeDevice]);

  const handleSubmit = async () => {
    const ok = await addDevice(userId, { type_device: typeDevice, diagnosis_mock: diagnosisMock });
    if (ok) {
      setDiagnosisMock("");
      onClose();
    }
  };

  const handleClose = () => {
    clearAddError();
    onClose();
  };

  return (
    <Modal isOpen={isOpen} title="Add Device" onClose={handleClose}>
      <div className="flex flex-col gap-4">
        {allConnected ? (
          <p className="rounded-lg bg-slate-50 px-4 py-3 text-sm text-slate-500">
            All supported devices are already connected.
          </p>
        ) : (
          <>
            <Select
              label="Device Type"
              value={typeDevice}
              options={availableOptions}
              onChange={(v) => setTypeDevice(v as Entity.DeviceType)}
            />
            <Input
              label="Diagnosis for Simulation (optional)"
              placeholder="e.g. Pheochromocytoma"
              value={diagnosisMock}
              onChange={setDiagnosisMock}
            />
            <p className="text-xs text-slate-400">
              If provided, the device generates synthetic data consistent with this diagnosis.
            </p>
          </>
        )}

        {addError && <Alert message={addError} onDismiss={clearAddError} />}

        <div className="flex justify-end gap-2 pt-1">
          <Button variant="ghost" onClick={handleClose} disabled={isAdding}>
            Cancel
          </Button>
          <Button loading={isAdding} disabled={allConnected} onClick={handleSubmit}>
            Connect Device
          </Button>
        </div>
      </div>
    </Modal>
  );
}
