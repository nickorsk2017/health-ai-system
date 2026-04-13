"use client";

import { create } from "zustand";

import { ConsiliumService } from "@/services/ConsiliumService";

type State = {
  findings: Entity.SpecialistFinding[];
  isLoading: boolean;
  error: string | null;
  fetchConsilium: (userId: string, startDate: string) => Promise<void>;
  clearError: () => void;
};

export const useConsiliumStore = create<State>((set) => ({
  findings: [],
  isLoading: false,
  error: null,

  fetchConsilium: async (userId, startDate) => {
    set({ isLoading: true, error: null, findings: [] });
    try {
      const findings = await ConsiliumService.fetchConsilium(userId, startDate);
      set({ findings, isLoading: false });
    } catch (err) {
      set({ isLoading: false, error: (err as Error).message });
    }
  },

  clearError: () => set({ error: null }),
}));
