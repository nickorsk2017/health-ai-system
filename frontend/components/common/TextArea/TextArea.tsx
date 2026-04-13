import cx from "@/utils/cx";

type Props = {
  label?: string;
  id?: string;
  value: string;
  placeholder?: string;
  rows?: number;
  disabled?: boolean;
  onChange: (value: string) => void;
  className?: string;
};

export default function TextArea({
  label,
  id,
  value,
  placeholder,
  rows = 3,
  disabled,
  onChange,
  className,
}: Props) {
  return (
    <div className={cx("flex flex-col gap-1", className)}>
      {label && (
        <label htmlFor={id} className="text-sm font-medium text-slate-700">
          {label}
        </label>
      )}
      <textarea
        id={id}
        value={value}
        rows={rows}
        placeholder={placeholder}
        disabled={disabled}
        onChange={(e) => onChange(e.target.value)}
        className="resize-none rounded-lg border border-slate-300 bg-white px-3 py-2 text-sm text-slate-800 placeholder:text-slate-400 focus:border-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-500/20 disabled:bg-slate-50 disabled:text-slate-400"
      />
    </div>
  );
}
