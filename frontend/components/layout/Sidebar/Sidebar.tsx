"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { Activity, ClipboardList, FlaskConical, Stethoscope } from "lucide-react";

import cx from "@/utils/cx";

const NAV_ITEMS = [
  { href: "/history", label: "Clinic History", icon: ClipboardList },
  { href: "/analyses", label: "Lab Analyses", icon: FlaskConical },
  { href: "/consilium", label: "Consilium", icon: Activity },
  { href: "/diagnosis", label: "Diagnosis PB", icon: Stethoscope },
];

export default function Sidebar() {
  const pathname = usePathname();

  return (
    <aside className="flex h-screen w-56 shrink-0 flex-col border-r border-slate-200 bg-white">
      <div className="flex items-center gap-2 border-b border-slate-200 px-5 py-4">
        <div className="flex h-7 w-7 items-center justify-center rounded-lg bg-blue-600">
          <Activity className="h-4 w-4 text-white" />
        </div>
        <span className="text-sm font-semibold text-slate-800">Health OS</span>
      </div>

      <nav className="flex flex-col gap-0.5 p-3">
        {NAV_ITEMS.map(({ href, label, icon: Icon }) => {
          const active = pathname.startsWith(href);
          return (
            <Link
              key={href}
              href={href}
              className={cx(
                "flex items-center gap-3 rounded-lg px-3 py-2 text-sm font-medium transition-colors",
                active
                  ? "bg-blue-50 text-blue-700"
                  : "text-slate-600 hover:bg-slate-100 hover:text-slate-800",
              )}
            >
              <Icon className="h-4 w-4 shrink-0" />
              {label}
            </Link>
          );
        })}
      </nav>
    </aside>
  );
}
