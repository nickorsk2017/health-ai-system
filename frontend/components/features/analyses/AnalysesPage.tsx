"use client";

import Card from "@/components/common/Card/Card";

import AnalysisForm from "./AnalysisForm";
import AnalysisList from "./AnalysisList";

export default function AnalysesPage() {
  return (
    <div className="flex flex-col gap-6">
      <div>
        <h1 className="text-xl font-semibold text-slate-800">Laboratory Analyses</h1>
        <p className="mt-1 text-sm text-slate-500">
          Record lab results and review the patient's analysis history.
        </p>
      </div>

      <div className="grid grid-cols-1 gap-6 xl:grid-cols-2">
        <Card className="p-6">
          <h2 className="mb-4 text-base font-semibold text-slate-700">New Analysis</h2>
          <AnalysisForm />
        </Card>

        <Card className="p-6">
          <h2 className="mb-4 text-base font-semibold text-slate-700">Analysis History</h2>
          <AnalysisList />
        </Card>
      </div>
    </div>
  );
}
