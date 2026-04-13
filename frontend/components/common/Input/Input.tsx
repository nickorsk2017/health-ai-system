import cx from "@/utils/cx";

type Props = {
  label?: string;
  id?: string;
  type?: string;
  value: string;
  min?: string;
  max?: string;
  placeholder?: string;
  disabled?: boolean;
  onChange: (value: string) => void;
  className?: string;
  autofocus?: boolean;
};

export default function Input({
  label,
  id,
  type = "text",
  value,
  min,
  max,
  placeholder,
  disabled,
  onChange,
  className,
  autofocus,
}: Props) {
  return (
    <div className={cx("flex flex-col gap-1", className)}>
      {label && (
        <label htmlFor={id} className="text-sm font-medium text-slate-700">
          {label}
        </label>
      )}
      <input
        id={id}
        type={type}
        value={value}
        min={min}
        max={max}
        placeholder={placeholder}
        disabled={disabled}
        onChange={(e) => onChange(e.target.value)}
        className="rounded-lg border border-slate-300 bg-white px-3 py-2 text-sm text-slate-800 placeholder:text-slate-400 focus:border-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-500/20 disabled:bg-slate-50 disabled:text-slate-400"
        autoFocus={autofocus}
      />
    </div>
  );
}
