"use client";

import { create } from "zustand";

import { VisitService } from "@/services/VisitService";

type State = {
  history: Entity.VisitRecord[];
  isSubmitting: boolean;
  isFetchingHistory: boolean;
  error: string | null;
  submitVisit: (data: Entity.CreateVisit) => Promise<boolean>;
  fetchHistory: (userId: string, lastDateVisit: string) => Promise<void>;
  clearError: () => void;
};

export const useVisitStore = create<State>((set) => ({
  history: [],
  isSubmitting: false,
  isFetchingHistory: false,
  error: null,

  submitVisit: async (data) => {
    set({ isSubmitting: true, error: null });
    try {
      await VisitService.recordVisit(data);
      set({ isSubmitting: false });
      return true;
    } catch (err) {
      set({ isSubmitting: false, error: (err as Error).message });
      return false;
    }
  },

  fetchHistory: async (userId, lastDateVisit) => {
    set({ isFetchingHistory: true, error: null, history: [] });
    try {
      const history = await VisitService.fetchHistory(userId, lastDateVisit);
      set({ history, isFetchingHistory: false });
    } catch (err) {
      set({ isFetchingHistory: false, error: (err as Error).message });
    }
  },

  clearError: () => set({ error: null }),
}));
