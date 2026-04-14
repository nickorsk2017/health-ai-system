"use client";

import { useEffect, useState } from "react";
import { ClipboardX, Plus, RefreshCw, Trash2 } from "lucide-react";

import Alert from "@/components/common/Alert/Alert";
import Button from "@/components/common/Button/Button";
import Spinner from "@/components/common/Spinner/Spinner";
import AddComplaintModal from "@/components/features/complaints/AddComplaintModal";
import ComplaintDetailModal from "@/components/features/complaints/ComplaintDetailModal";
import { useComplaintStore } from "@/stores/useComplaintStore";
import formatDate from "@/utils/formatDate";

const STATUS_LABELS: Record<Entity.ComplaintStatus, string> = {
  unread: "Unread",
  read: "Read",
  appointment: "Scheduled",
};

const STATUS_CLASSES: Record<Entity.ComplaintStatus, string> = {
  unread: "bg-slate-100 text-slate-600",
  read: "bg-blue-50 text-blue-700",
  appointment: "bg-emerald-50 text-emerald-700",
};

type Props = {
  userId: string;
  isDoctor?: boolean;
};

export default function ComplaintList({ userId, isDoctor = false }: Props) {
  const {
    complaints,
    isFetching,
    isSubmitting,
    fetchError,
    fetchComplaints,
    removeComplaint,
    clearFetchError,
  } = useComplaintStore();

  const [isAddOpen, setIsAddOpen] = useState(false);
  const [selected, setSelected] = useState<Entity.Complaint | null>(null);

  useEffect(() => {
    fetchComplaints(userId);
  }, [userId, fetchComplaints]);

  const handleDelete = (e: React.MouseEvent, complaintId: string) => {
    e.stopPropagation();
    removeComplaint(complaintId, userId);
  };

  return (
    <div className="flex flex-col gap-5">
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-base font-semibold text-slate-800">
            {isDoctor ? "Patient Complaints" : "My Complaints"}
          </h2>
          <p className="text-sm text-slate-500">
            {isDoctor ? "Review and schedule appointments" : "Track your health concerns"}
          </p>
        </div>
        <div className="flex items-center gap-2">
          <Button
            variant="secondary"
            size="sm"
            onClick={() => fetchComplaints(userId)}
            disabled={isFetching}
          >
            <RefreshCw className="h-3.5 w-3.5" />
            Refresh
          </Button>
          {!isDoctor && (
            <Button size="sm" onClick={() => setIsAddOpen(true)}>
              <Plus className="h-3.5 w-3.5" />
              Add Complaint
            </Button>
          )}
        </div>
      </div>

      {fetchError && <Alert message={fetchError} onDismiss={clearFetchError} />}

      {isFetching && (
        <div className="flex justify-center py-10">
          <Spinner />
        </div>
      )}

      {!isFetching && complaints.length > 0 && (
        <div className="flex flex-col gap-2">
          {complaints.map((c) => (
            <div
              key={c.complaint_id}
              onClick={() => setSelected(c)}
              className="flex cursor-pointer items-start justify-between gap-4 rounded-xl border border-slate-200 bg-white px-5 py-4 shadow-sm transition-colors hover:border-slate-300 hover:bg-slate-50"
            >
              <div className="flex min-w-0 flex-1 flex-col gap-1.5">
                <p className="truncate text-sm font-medium text-slate-800">{c.problem_health}</p>
                <div className="flex items-center gap-3 text-xs text-slate-500">
                  <span>Reported {formatDate(c.date_public)}</span>
                  <span
                    className={`rounded-full px-2 py-0.5 font-medium ${STATUS_CLASSES[c.status]}`}
                  >
                    {STATUS_LABELS[c.status]}
                  </span>
                </div>
              </div>
              {!isDoctor && (
                <button
                  type="button"
                  disabled={isSubmitting}
                  onClick={(e) => handleDelete(e, c.complaint_id)}
                  className="shrink-0 rounded p-1.5 text-slate-300 transition-colors hover:bg-red-50 hover:text-red-500 disabled:cursor-not-allowed disabled:opacity-40"
                  aria-label="Delete complaint"
                >
                  <Trash2 className="h-4 w-4" />
                </button>
              )}
            </div>
          ))}
        </div>
      )}

      {!isFetching && complaints.length === 0 && !fetchError && (
        <div className="flex flex-col items-center gap-3 rounded-xl border border-dashed border-slate-200 bg-slate-50 py-14 text-center">
          <ClipboardX className="h-8 w-8 text-slate-300" />
          <div>
            <p className="text-sm font-medium text-slate-600">No complaints yet</p>
            <p className="text-xs text-slate-400">
              {isDoctor ? "No patients have submitted complaints" : "Report a health concern to get started"}
            </p>
          </div>
          {!isDoctor && (
            <Button size="sm" onClick={() => setIsAddOpen(true)}>
              Add Complaint
            </Button>
          )}
        </div>
      )}

      {!isDoctor && (
        <AddComplaintModal
          isOpen={isAddOpen}
          userId={userId}
          onClose={() => setIsAddOpen(false)}
        />
      )}

      {selected && (
        <ComplaintDetailModal
          isOpen
          complaint={selected}
          doctorUserId={userId}
          isDoctor={isDoctor}
          onClose={() => setSelected(null)}
        />
      )}
    </div>
  );
}
