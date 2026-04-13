"use client";

import { create } from "zustand";

import { AnalysisService } from "@/services/AnalysisService";

type State = {
  analyses: Entity.AnalysisRecord[];
  isSubmitting: boolean;
  isFetching: boolean;
  submitError: string | null;
  fetchError: string | null;
  submitAnalysis: (data: Entity.CreateAnalysis) => Promise<boolean>;
  fetchAnalyses: (userId: string, startDate: string) => Promise<void>;
  clearSubmitError: () => void;
  clearFetchError: () => void;
};

export const useAnalysisStore = create<State>((set) => ({
  analyses: [],
  isSubmitting: false,
  isFetching: false,
  submitError: null,
  fetchError: null,

  submitAnalysis: async (data) => {
    set({ isSubmitting: true, submitError: null });
    try {
      await AnalysisService.recordAnalysis(data);
      set({ isSubmitting: false });
      return true;
    } catch (err) {
      set({ isSubmitting: false, submitError: (err as Error).message });
      return false;
    }
  },

  fetchAnalyses: async (userId, startDate) => {
    set({ isFetching: true, fetchError: null, analyses: [] });
    try {
      const analyses = await AnalysisService.fetchAnalyses(userId, startDate);
      set({ analyses, isFetching: false });
    } catch (err) {
      set({ isFetching: false, fetchError: (err as Error).message });
    }
  },

  clearSubmitError: () => set({ submitError: null }),
  clearFetchError: () => set({ fetchError: null }),
}));
