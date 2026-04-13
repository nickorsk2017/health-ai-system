"use client";

import { useState } from "react";

import Alert from "@/components/common/Alert/Alert";
import Button from "@/components/common/Button/Button";
import Input from "@/components/common/Input/Input";
import Spinner from "@/components/common/Spinner/Spinner";
import { useAnalysisStore } from "@/stores/useAnalysisStore";
import { usePatientStore } from "@/stores/usePatientStore";
import formatDate from "@/utils/formatDate";

const SNIPPET_LENGTH = 120;

function AnalysisCard({ record }: { record: Entity.AnalysisRecord }) {
  const [expanded, setExpanded] = useState(false);
  const isLong = record.analysis.length > SNIPPET_LENGTH;
  const displayed = expanded || !isLong
    ? record.analysis
    : `${record.analysis.slice(0, SNIPPET_LENGTH)}…`;

  return (
    <div className="rounded-xl border border-slate-200 bg-white p-4">
      <div className="mb-2 flex items-center justify-between">
        <span className="rounded-md bg-blue-50 px-2 py-0.5 text-xs font-medium text-blue-700">
          {formatDate(record.date)}
        </span>
        <span className="text-xs text-slate-400">{formatDate(record.created_at)}</span>
      </div>
      <p className="whitespace-pre-wrap text-sm text-slate-700">{displayed}</p>
      {isLong && (
        <button
          type="button"
          onClick={() => setExpanded((v) => !v)}
          className="mt-2 text-xs font-medium text-blue-600 hover:text-blue-700"
        >
          {expanded ? "Show less" : "Show more"}
        </button>
      )}
    </div>
  );
}

export default function AnalysisList() {
  const { selectedPatientId } = usePatientStore();
  const { analyses, isFetching, fetchError, fetchAnalyses, clearFetchError } = useAnalysisStore();
  const [since, setSince] = useState("2000-01-01");


  const sorted = [...analyses].sort(
    (a, b) => new Date(b.date).getTime() - new Date(a.date).getTime(),
  );

  return (
    <div className="flex flex-col gap-4">
      <div className="flex items-end gap-3">
        <Input
          label="Results from"
          type="date"
          value={since}
          onChange={setSince}
          className="w-44"
        />
        <Button loading={isFetching} onClick={() => fetchAnalyses(selectedPatientId!, since)}>
          Refresh
        </Button>
      </div>

      {fetchError && <Alert message={fetchError} onDismiss={clearFetchError} />}

      {isFetching && (
        <div className="flex justify-center py-8">
          <Spinner />
        </div>
      )}

      {!isFetching && sorted.length > 0 && (
        <div className="flex flex-col gap-3">
          {sorted.map((record, i) => (
            <AnalysisCard key={`${record.date}-${i}`} record={record} />
          ))}
        </div>
      )}

      {!isFetching && sorted.length === 0 && !fetchError && (
        <p className="py-6 text-center text-sm text-slate-400">
          No lab results found. Adjust the date range or save a new analysis.
        </p>
      )}
    </div>
  );
}
