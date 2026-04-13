import { AlertCircle, CheckCircle, Info, X } from "lucide-react";

import cx from "@/utils/cx";

type Props = {
  variant?: "error" | "success" | "info";
  message: string;
  onDismiss?: () => void;
  className?: string;
};

const styles = {
  error: {
    container: "bg-red-50 border-red-200 text-red-800",
    icon: <AlertCircle className="h-4 w-4 shrink-0 text-red-500" />,
  },
  success: {
    container: "bg-green-50 border-green-200 text-green-800",
    icon: <CheckCircle className="h-4 w-4 shrink-0 text-green-500" />,
  },
  info: {
    container: "bg-blue-50 border-blue-200 text-blue-800",
    icon: <Info className="h-4 w-4 shrink-0 text-blue-500" />,
  },
};

export default function Alert({ variant = "error", message, onDismiss, className }: Props) {
  const { container, icon } = styles[variant];

  return (
    <div
      role="alert"
      className={cx("flex items-start gap-3 rounded-lg border p-3 text-sm", container, className)}
    >
      {icon}
      <span className="flex-1">{message}</span>
      {onDismiss && (
        <button onClick={onDismiss} className="shrink-0 opacity-60 hover:opacity-100">
          <X className="h-4 w-4" />
        </button>
      )}
    </div>
  );
}
