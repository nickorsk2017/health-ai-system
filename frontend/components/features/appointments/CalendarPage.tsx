"use client";

import { useEffect, useState } from "react";
import { RefreshCw } from "lucide-react";

import Alert from "@/components/common/Alert/Alert";
import Button from "@/components/common/Button/Button";
import Modal from "@/components/common/Modal/Modal";
import Spinner from "@/components/common/Spinner/Spinner";
import CalendarView from "@/components/features/appointments/CalendarView";
import { useAppointmentStore } from "@/stores/useAppointmentStore";
import formatDate from "@/utils/formatDate";

export default function CalendarPage() {
  const { appointments, isFetching, fetchError, fetchAppointments, clearFetchError } =
    useAppointmentStore();
  const [dayAppts, setDayAppts] = useState<{ date: string; list: Entity.Appointment[] } | null>(
    null,
  );

  useEffect(() => {
    fetchAppointments("");
  }, [fetchAppointments]);

  return (
    <div className="flex flex-col gap-5">
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-base font-semibold text-slate-800">Appointment Calendar</h2>
          <p className="text-sm text-slate-500">All patients — upcoming visits</p>
        </div>
        <Button
          variant="secondary"
          size="sm"
          onClick={() => fetchAppointments("")}
          disabled={isFetching}
        >
          <RefreshCw className="h-3.5 w-3.5" />
          Refresh
        </Button>
      </div>

      {fetchError && <Alert message={fetchError} onDismiss={clearFetchError} />}

      {isFetching ? (
        <div className="flex justify-center py-10">
          <Spinner />
        </div>
      ) : (
        <CalendarView
          appointments={appointments}
          onDayClick={(date, list) => list.length > 0 && setDayAppts({ date, list })}
        />
      )}

      {dayAppts && (
        <Modal
          isOpen
          title={`Appointments — ${formatDate(dayAppts.date)}`}
          onClose={() => setDayAppts(null)}
        >
          <div className="flex flex-col gap-3">
            {dayAppts.list.map((appt) => (
              <div
                key={appt.appointment_id}
                className="rounded-lg border border-slate-100 bg-slate-50 px-4 py-3"
              >
                <div className="flex items-center justify-between">
                  <p className="text-sm font-semibold text-slate-800">{appt.doctor_type}</p>
                  <span className="text-xs text-slate-500">
                    {appt.appointment_date.slice(11, 16)}
                  </span>
                </div>
                <p className="mt-0.5 text-xs text-slate-500">Patient: {appt.user_id}</p>
                {appt.problem_notes && (
                  <p className="mt-1 text-sm text-slate-600">{appt.problem_notes}</p>
                )}
              </div>
            ))}
          </div>
        </Modal>
      )}
    </div>
  );
}
