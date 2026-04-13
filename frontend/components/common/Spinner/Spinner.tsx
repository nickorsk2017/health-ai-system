import cx from "@/utils/cx";

type Props = {
  size?: "sm" | "md" | "lg";
  className?: string;
};

const sizes = {
  sm: "h-4 w-4 border-2",
  md: "h-8 w-8 border-2",
  lg: "h-12 w-12 border-[3px]",
};

export default function Spinner({ size = "md", className }: Props) {
  return (
    <span
      role="status"
      aria-label="Loading"
      className={cx(
        "inline-block animate-spin rounded-full border-blue-600 border-t-transparent",
        sizes[size],
        className,
      )}
    />
  );
}
