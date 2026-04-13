import Card from "@/components/common/Card/Card";

type Props = {
  finding: Entity.SpecialistFinding;
};

const ACCENT_COLORS: Record<string, string> = {
  oncology: "border-t-rose-400",
  gastroenterology: "border-t-orange-400",
  cardiology: "border-t-red-500",
  hematology: "border-t-purple-400",
  nephrology: "border-t-cyan-500",
  nutrition: "border-t-green-400",
  endocrinology: "border-t-amber-400",
  mental_health: "border-t-violet-400",
  pulmonology: "border-t-sky-400",
};

function Field({ label, value }: { label: string; value: string }) {
  return (
    <div>
      <p className="mb-0.5 text-xs font-semibold uppercase tracking-wide text-slate-400">{label}</p>
      <p className="text-sm text-slate-700">{value || "—"}</p>
    </div>
  );
}

export default function SpecialistCard({ finding }: Props) {
  const accent = ACCENT_COLORS[finding.specialty.toLowerCase()] ?? "border-t-slate-300";

  return (
    <Card accent={accent} className="p-5">
      <h3 className="mb-4 text-sm font-semibold capitalize text-slate-800">
        {finding.specialty.replace("_", " ")}
      </h3>
      <div className="flex flex-col gap-3">
        <Field label="Probable Diagnosis" value={finding.probable_diagnosis} />
        <Field label="Risks" value={finding.risks} />
        <Field label="Treatment" value={finding.treatment} />
        <Field label="Prognosis" value={finding.prognosis} />
      </div>
    </Card>
  );
}
