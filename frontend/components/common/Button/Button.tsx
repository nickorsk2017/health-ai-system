import cx from "@/utils/cx";

type Props = {
  variant?: "primary" | "secondary" | "ghost" | "special";
  size?: "sm" | "md" | "lg";
  type?: "button" | "submit" | "reset";
  disabled?: boolean;
  loading?: boolean;
  onClick?: () => void;
  children: React.ReactNode;
  className?: string;
};

const variants = {
  primary: "bg-blue-600 hover:bg-blue-700 text-white shadow-sm disabled:bg-blue-300",
  secondary:
    "bg-white border border-slate-300 text-slate-700 hover:bg-slate-50 disabled:opacity-50",
  ghost: "text-slate-600 hover:bg-slate-100 disabled:opacity-50",
  special: "inline-flex animate-breathe cursor-pointer items-center gap-2 rounded-lg !bg-violet-600 px-4 py-2 text-sm font-medium text-white will-change-transform hover:scale-105 hover:brightness-110 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-violet-500 focus-visible:ring-offset-1"
};

const sizes = {
  sm: "px-3 py-1.5 text-sm",
  md: "px-4 py-2 text-sm",
  lg: "px-6 py-2.5 text-base",
};

export default function Button({
  variant = "primary",
  size = "md",
  type = "button",
  disabled,
  loading,
  onClick,
  children,
  className,
}: Props) {
  return (
    <button
      type={type}
      disabled={disabled || loading}
      onClick={onClick}
      className={cx(
        "inline-flex items-center justify-center gap-2 rounded-lg font-medium transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-blue-500 focus-visible:ring-offset-1 cursor-pointer disabled:cursor-not-allowed",
        variants[variant],
        sizes[size],
        className,
      )}
    >
      {loading && (
        <span className="h-4 w-4 animate-spin rounded-full border-2 border-current border-t-transparent" />
      )}
      {children}
    </button>
  );
}
