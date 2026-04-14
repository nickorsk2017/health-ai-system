"use client";

import AppointmentsPage from "@/components/features/appointments/AppointmentsPage";
import CalendarPage from "@/components/features/appointments/CalendarPage";
import { useRole } from "@/contexts/RoleContext";
import { usePatientStore } from "@/stores/usePatientStore";

export default function AppointmentsWrapper() {
  const { role } = useRole();
  const { selectedPatientId } = usePatientStore();

  if (role === "doctor") {
    return (
      <div className="flex flex-col gap-6 p-6">
        <CalendarPage />
      </div>
    );
  }

  if (!selectedPatientId) {
    return (
      <div className="flex items-center justify-center py-20 text-sm text-slate-500">
        No patient selected.
      </div>
    );
  }

  return (
    <div className="flex flex-col gap-6 p-6">
      <AppointmentsPage userId={selectedPatientId} />
    </div>
  );
}
