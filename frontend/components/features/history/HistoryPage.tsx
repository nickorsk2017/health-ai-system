"use client";

import Card from "@/components/common/Card/Card";

import HistoryList from "./HistoryList";
import VisitForm from "./VisitForm";

export default function HistoryPage() {
  return (
    <div className="flex flex-col gap-6">
      <div>
        <h1 className="text-xl font-semibold text-slate-800">Clinic History</h1>
        <p className="mt-1 text-sm text-slate-500">Record SOAP notes and review visit history.</p>
      </div>

      <div className="grid grid-cols-1 gap-6 xl:grid-cols-2">
        <Card className="p-6">
          <h2 className="mb-4 text-base font-semibold text-slate-700">New Visit</h2>
          <VisitForm />
        </Card>

        <Card className="p-6">
          <h2 className="mb-4 text-base font-semibold text-slate-700">Visit Records</h2>
          <HistoryList />
        </Card>
      </div>
    </div>
  );
}
