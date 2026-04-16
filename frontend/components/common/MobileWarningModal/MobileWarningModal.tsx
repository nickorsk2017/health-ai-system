"use client";

import { Monitor } from "lucide-react";

import Modal from "@/components/common/Modal/Modal";

type Props = {
  isOpen: boolean;
  text: string;
};

export default function MobileWarningModal({ isOpen, text }: Props) {
  return (
    <Modal isOpen={isOpen} title="Desktop Required" onClose={() => {}} closable={false}>
      <div className="flex flex-col items-center gap-4 py-2 text-center">
        <div className="flex h-14 w-14 items-center justify-center rounded-full bg-blue-50">
          <Monitor className="h-7 w-7 text-blue-500" />
        </div>
        <div className="space-y-1">
          <p className="text-sm font-medium text-slate-800">
            This app is optimized for desktop use
          </p>
          <p className="text-sm text-slate-500">
            Please open it on a computer or a larger screen for the best experience.
          </p>
          <p className="mt-2 text-xs italic text-slate-400">{text}</p>
        </div>
      </div>
    </Modal>
  );
}
