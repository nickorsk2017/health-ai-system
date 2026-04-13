import cx from "@/utils/cx";

type Props = {
  children: React.ReactNode;
  className?: string;
  accent?: string;
};

export default function Card({ children, className, accent }: Props) {
  return (
    <div
      className={cx(
        "rounded-xl border border-slate-200 bg-white shadow-sm",
        accent && `border-t-4 ${accent}`,
        className,
      )}
    >
      {children}
    </div>
  );
}
