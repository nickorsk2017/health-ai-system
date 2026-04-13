"use client";

import { create } from "zustand";

import { DiagnosisService } from "@/services/DiagnosisService";

type State = {
  consultation: Entity.GPConsultation | null;
  isLoading: boolean;
  error: string | null;
  fetchDiagnosis: (userId: string, startDate: string) => Promise<void>;
  clearError: () => void;
};

export const useDiagnosisStore = create<State>((set) => ({
  consultation: null,
  isLoading: false,
  error: null,

  fetchDiagnosis: async (userId, startDate) => {
    set({ isLoading: true, error: null, consultation: null });
    try {
      const consultation = await DiagnosisService.fetchDiagnosis(userId, startDate);
      set({ consultation, isLoading: false });
    } catch (err) {
      set({ isLoading: false, error: (err as Error).message });
    }
  },

  clearError: () => set({ error: null }),
}));
