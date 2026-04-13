import cx from "@/utils/cx";

type Option = {
  value: string;
  label: string;
};

type Props = {
  label?: string;
  id?: string;
  value: string;
  options: Option[];
  placeholder?: string;
  disabled?: boolean;
  onChange: (value: string) => void;
  className?: string;
};

export default function Select({
  label,
  id,
  value,
  options,
  placeholder,
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
      <select
        id={id}
        value={value}
        disabled={disabled}
        onChange={(e) => onChange(e.target.value)}
        className="rounded-lg border border-slate-300 bg-white px-3 py-2 text-sm text-slate-800 focus:border-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-500/20 disabled:bg-slate-50 disabled:text-slate-400"
      >
        {placeholder && (
          <option value="" disabled>
            {placeholder}
          </option>
        )}
        {options.map((opt) => (
          <option key={opt.value} value={opt.value}>
            {opt.label}
          </option>
        ))}
      </select>
    </div>
  );
}
