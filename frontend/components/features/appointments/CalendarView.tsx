"use client";

import { useMemo, useState } from "react";
import dayjs from "dayjs";
import { ChevronLeft, ChevronRight } from "lucide-react";

import cx from "@/utils/cx";

const WEEKDAYS = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"];

const MONTH_NAMES = [
  "January", "February", "March", "April", "May", "June",
  "July", "August", "September", "October", "November", "December",
];

type Props = {
  appointments: Entity.Appointment[];
  onDayClick?: (date: string, appointments: Entity.Appointment[]) => void;
};

export default function CalendarView({ appointments, onDayClick }: Props) {
  const today = new Date();
  const [year, setYear] = useState(today.getFullYear());
  const [month, setMonth] = useState(today.getMonth());

  const firstDay = new Date(year, month, 1).getDay();
  const daysInMonth = new Date(year, month + 1, 0).getDate();

  const goBack = () => {
    if (month === 0) { setYear((y) => y - 1); setMonth(11); }
    else setMonth((m) => m - 1);
  };

  const goForward = () => {
    if (month === 11) { setYear((y) => y + 1); setMonth(0); }
    else setMonth((m) => m + 1);
  };

  const appointmentsByDate = useMemo(
    () =>
      appointments.reduce<Record<string, Entity.Appointment[]>>((acc, appt) => {
        const key = dayjs(appt.appointment_date).local().format("YYYY-MM-DD");
        if (!acc[key]) acc[key] = [];
        acc[key].push(appt);
        return acc;
      }, {}),
    [appointments],
  );

  const appointmentPreviewByDate = useMemo(
    () =>
      Object.entries(appointmentsByDate).reduce<
        Record<string, Array<{ appointment_id: string; doctor_type: string; local_time: string }>>
      >((acc, [dateKey, list]) => {
        acc[dateKey] = list.slice(0, 2).map((appt) => ({
          appointment_id: appt.appointment_id,
          doctor_type: appt.doctor_type,
          local_time: dayjs(appt.appointment_date).local().format("HH:mm"),
        }));
        return acc;
      }, {}),
    [appointmentsByDate],
  );

  const cells: (number | null)[] = [
    ...Array(firstDay).fill(null),
    ...Array.from({ length: daysInMonth }, (_, i) => i + 1),
  ];

  const todayKey = `${today.getFullYear()}-${String(today.getMonth() + 1).padStart(2, "0")}-${String(today.getDate()).padStart(2, "0")}`;

  

  return (
    <div className="flex flex-col gap-4">
      <div className="flex items-center justify-between">
        <h3 className="text-base font-semibold text-slate-800">
          {MONTH_NAMES[month]} {year}
        </h3>
        <div className="flex gap-1">
          <button
            type="button"
            onClick={goBack}
            className="rounded-lg p-1.5 text-slate-500 hover:bg-slate-100"
          >
            <ChevronLeft className="h-4 w-4" />
          </button>
          <button
            type="button"
            onClick={goForward}
            className="rounded-lg p-1.5 text-slate-500 hover:bg-slate-100"
          >
            <ChevronRight className="h-4 w-4" />
          </button>
        </div>
      </div>

      <div className="grid grid-cols-7 gap-px rounded-xl border border-slate-200 bg-slate-200 overflow-hidden">
        {WEEKDAYS.map((day) => (
          <div
            key={day}
            className="bg-slate-50 py-2 text-center text-xs font-medium text-slate-500"
          >
            {day}
          </div>
        ))}

        {cells.map((day, idx) => {
          if (day === null) {
            return <div key={`empty-${idx}`} className="bg-white h-20" />;
          }
          const dateKey = `${year}-${String(month + 1).padStart(2, "0")}-${String(day).padStart(2, "0")}`;
          const dayAppts = appointmentsByDate[dateKey] ?? [];
          const dayPreview = appointmentPreviewByDate[dateKey] ?? [];
          const isToday = dateKey === todayKey;

          return (
            <div
              key={dateKey}
              onClick={() => onDayClick?.(dateKey, dayAppts)}
              className={cx(
                "bg-white h-20 p-1.5 flex flex-col gap-1 transition-colors",
                onDayClick && "cursor-pointer hover:bg-blue-50",
              )}
            >
              <span
                className={cx(
                  "inline-flex h-6 w-6 items-center justify-center rounded-full text-xs font-medium",
                  isToday ? "bg-blue-600 text-white" : "text-slate-600",
                )}
              >
                {day}
              </span>
              <div className="flex flex-col gap-0.5 overflow-hidden">
                {dayPreview.map((appt) => {
                  return (
                    <span
                      key={appt.appointment_id}
                      className="truncate rounded bg-blue-100 px-1 py-0.5 text-xs font-medium text-blue-700"
                      title={`${appt.doctor_type} — ${appt.local_time}`}
                    >
                      {appt.local_time} {appt.doctor_type}
                    </span>
                  );
                })}
                {dayAppts.length > 2 && (
                  <span className="text-xs text-slate-400">+{dayAppts.length - 2} more</span>
                )}
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
