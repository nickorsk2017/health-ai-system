"use client";

import { useEffect, useState } from "react";
import { Cpu, RefreshCw, Smartphone, Trash2, Watch } from "lucide-react";

import Alert from "@/components/common/Alert/Alert";
import Button from "@/components/common/Button/Button";
import Spinner from "@/components/common/Spinner/Spinner";
import AddDeviceModal from "@/components/features/devices/AddDeviceModal";
import { useDeviceStore } from "@/stores/useDeviceStore";
import { usePatientStore } from "@/stores/usePatientStore";
import formatDate from "@/utils/formatDate";

const DEVICE_LABELS: Record<Entity.DeviceType, string> = {
  apple_health: "Apple Health",
  oura_ring: "Oura Ring",
};

const DEVICE_ICONS: Record<Entity.DeviceType, React.ComponentType<{ className?: string }>> = {
  apple_health: Smartphone,
  oura_ring: Watch,
};

function DeviceCard({
  device,
  onDelete,
  isDeleting,
}: {
  device: Entity.Device;
  onDelete: (id: string) => void;
  isDeleting: boolean;
}) {
  const Icon = DEVICE_ICONS[device.type_device as Entity.DeviceType] ?? Cpu;
  const label = DEVICE_LABELS[device.type_device as Entity.DeviceType] ?? device.type_device;

  return (
    <div className="flex flex-col gap-3 rounded-xl border border-slate-200 bg-white p-5 shadow-sm">
      <div className="flex items-start justify-between">
        <div className="flex items-center gap-3">
          <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-lg bg-blue-50">
            <Icon className="h-5 w-5 text-blue-600" />
          </div>
          <div>
            <p className="text-sm font-semibold text-slate-800">{label}</p>
            <span className="inline-flex items-center gap-1 text-xs text-emerald-600">
              <span className="h-1.5 w-1.5 rounded-full bg-emerald-500" />
              Active
            </span>
          </div>
        </div>
        <button
          type="button"
          disabled={isDeleting}
          onClick={() => onDelete(device.id)}
          className="rounded p-1.5 text-slate-300 transition-colors hover:bg-red-50 hover:text-red-500 disabled:cursor-not-allowed disabled:opacity-40"
          aria-label="Remove device"
        >
          {isDeleting ? (
            <span className="block h-4 w-4 animate-spin rounded-full border-2 border-current border-t-transparent" />
          ) : (
            <Trash2 className="h-4 w-4" />
          )}
        </button>
      </div>

      <div className="flex flex-col gap-1.5 text-xs text-slate-500">
        {device.diagnosis_mock && (
          <div className="flex items-center gap-1.5">
            <span className="font-medium text-slate-600">Simulation:</span>
            <span className="rounded-md bg-amber-50 px-2 py-0.5 font-medium text-amber-700">
              {device.diagnosis_mock}
            </span>
          </div>
        )}
        <div className="flex items-center gap-1.5">
          <span className="font-medium text-slate-600">Connected:</span>
          <span>{formatDate(device.created_at)}</span>
        </div>
      </div>
    </div>
  );
}

export default function DeviceList() {
  const { selectedPatientId } = usePatientStore();
  const { devices, isFetching, isDeleting, fetchError, fetchDevices, removeDevice, clearFetchError } =
    useDeviceStore();
  const [isModalOpen, setIsModalOpen] = useState(false);

  useEffect(() => {
    if (selectedPatientId) {
      fetchDevices(selectedPatientId);
    }
  }, [selectedPatientId, fetchDevices]);

  const handleDelete = (deviceId: string) => {
    if (selectedPatientId) {
      removeDevice(selectedPatientId, deviceId);
    }
  };

  return (
    <div className="flex flex-col gap-5">
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-base font-semibold text-slate-800">Connected Devices</h2>
          <p className="text-sm text-slate-500">Auto-synced every 10 minutes</p>
        </div>
        <div className="flex items-center gap-2">
          <Button
            variant="secondary"
            size="sm"
            onClick={() => selectedPatientId && fetchDevices(selectedPatientId)}
            disabled={isFetching}
          >
            <RefreshCw className="h-3.5 w-3.5" />
            Refresh
          </Button>
          <Button size="sm" onClick={() => setIsModalOpen(true)}>
            Add Device
          </Button>
        </div>
      </div>

      {fetchError && <Alert message={fetchError} onDismiss={clearFetchError} />}

      {isFetching && (
        <div className="flex justify-center py-10">
          <Spinner />
        </div>
      )}

      {!isFetching && devices.length > 0 && (
        <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3">
          {devices.map((device) => (
            <DeviceCard
              key={device.id}
              device={device}
              onDelete={handleDelete}
              isDeleting={isDeleting === device.id}
            />
          ))}
        </div>
      )}

      {!isFetching && devices.length === 0 && !fetchError && (
        <div className="flex flex-col items-center gap-3 rounded-xl border border-dashed border-slate-200 bg-slate-50 py-14 text-center">
          <Cpu className="h-8 w-8 text-slate-300" />
          <div>
            <p className="text-sm font-medium text-slate-600">No devices connected</p>
            <p className="text-xs text-slate-400">Add your first device to start syncing data</p>
          </div>
          <Button size="sm" onClick={() => setIsModalOpen(true)}>
            Add Device
          </Button>
        </div>
      )}

      {selectedPatientId && (
        <AddDeviceModal
          isOpen={isModalOpen}
          userId={selectedPatientId}
          onClose={() => setIsModalOpen(false)}
        />
      )}
    </div>
  );
}
