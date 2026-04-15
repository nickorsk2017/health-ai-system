"use client";

import { useState } from "react";
import { CalendarPlus, CheckCircle } from "lucide-react";

import Button from "@/components/common/Button/Button";
import Modal from "@/components/common/Modal/Modal";
import ScheduleAppointmentModal from "@/components/features/complaints/ScheduleAppointmentModal";
import { useComplaintStore } from "@/stores/useComplaintStore";
import formatDate from "@/utils/formatDate";

const STATUS_LABELS: Record<Entity.ComplaintStatus, string> = {
  unread: "Unread",
  read: "Read",
  appointment: "Appointment Scheduled",
};

const STATUS_CLASSES: Record<Entity.ComplaintStatus, string> = {
  unread: "bg-slate-100 text-slate-600",
  read: "bg-blue-50 text-blue-700",
  appointment: "bg-emerald-50 text-emerald-700",
};

type Props = {
  isOpen: boolean;
  complaint: Entity.Complaint;
  doctorUserId: string;
  isDoctor: boolean;
  onClose: () => void;
};

export default function ComplaintDetailModal({ isOpen, complaint, doctorUserId, isDoctor, onClose }: Props) {
  const { markRead } = useComplaintStore();
  const [isScheduleOpen, setIsScheduleOpen] = useState(false);

  const handleMarkRead = async () => {
    await markRead(complaint.complaint_id, doctorUserId);
    onClose();
  };

  const handleScheduleClose = () => {
    setIsScheduleOpen(false);
    onClose();
  };

  return (
    <>
      <Modal isOpen={isOpen && !isScheduleOpen} title="Complaint Detail" onClose={onClose}>
        <div className="flex flex-col gap-4">
          <div className="flex items-center justify-between">
            <span className="text-xs text-slate-500">
              Reported {formatDate(complaint.date_public, "MMM D, YYYY, HH:mm")}
            </span>
            <span
              className={`rounded-full px-2.5 py-0.5 text-xs font-medium ${STATUS_CLASSES[complaint.status]}`}
            >
              {STATUS_LABELS[complaint.status]}
            </span>
          </div>

          <div className="rounded-lg border border-slate-100 bg-slate-50 px-4 py-3">
            <p className="text-sm text-slate-700">{complaint.problem_health}</p>
          </div>

          {isDoctor && (
            <div className="flex justify-end gap-2 pt-1">
              {complaint.status === "unread" && (
                <Button variant="secondary" onClick={handleMarkRead}>
                  <CheckCircle className="h-4 w-4" />
                  Mark as Read
                </Button>
              )}
              {complaint.status !== "appointment" && (
                <Button onClick={() => setIsScheduleOpen(true)}>
                  <CalendarPlus className="h-4 w-4" />
                  Schedule Appointment
                </Button>
              )}
              {complaint.status === "appointment" && (
                <Button variant="secondary" onClick={onClose}>
                  Close
                </Button>
              )}
            </div>
          )}
        </div>
      </Modal>

      <ScheduleAppointmentModal
        isOpen={isScheduleOpen}
        complaint={complaint}
        onClose={handleScheduleClose}
      />
    </>
  );
}
