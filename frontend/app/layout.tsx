import type { Metadata } from "next";

import Sidebar from "@/components/layout/Sidebar/Sidebar";
import TopBar from "@/components/layout/TopBar/TopBar";
import PatientGuard from "@/components/features/patient/PatientGuard";
import PatientSelector from "@/components/features/patient/PatientSelector";

import "./globals.css";

export const metadata: Metadata = {
  title: "Personal Health OS",
  description: "AI-powered health assistant gateway",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>
        <PatientGuard />
        <div className="flex h-screen overflow-hidden">
          <Sidebar />
          <div className="flex flex-1 flex-col overflow-hidden">
            <TopBar>
              <PatientSelector />
            </TopBar>
            <main className="flex-1 overflow-y-auto p-6">{children}</main>
          </div>
        </div>
      </body>
    </html>
  );
}
