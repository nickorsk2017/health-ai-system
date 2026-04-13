"use client";

import { create } from "zustand";

import { AnalysisService } from "@/services/AnalysisService";

type State = {
  analyses: Entity.AnalysisRecord[];
  isSubmitting: boolean;
  isFetching: boolean;
  isImporting: boolean;
  isUpdating: boolean;
  isDeleting: boolean;
  submitError: string | null;
  fetchError: string | null;
  importError: string | null;
  editError: string | null;
  missingAnalyses: string[];
  refreshTrigger: number;
  submitAnalysis: (data: Entity.CreateAnalysis) => Promise<boolean>;
  fetchAnalyses: (userId: string, startDate: string) => Promise<void>;
  importFromPrompt: (data: Entity.AnalysisByPromptRequest) => Promise<Entity.AnalysisByPromptResponse | null>;
  updateAnalysis: (analysisId: string, data: Entity.UpdateAnalysis) => Promise<boolean>;
  deleteAnalysis: (analysisId: string) => Promise<boolean>;
  clearSubmitError: () => void;
  clearFetchError: () => void;
  clearImportError: () => void;
  clearMissingAnalyses: () => void;
  clearEditError: () => void;
};

export const useAnalysisStore = create<State>((set) => ({
  analyses: [],
  isSubmitting: false,
  isFetching: false,
  isImporting: false,
  isUpdating: false,
  isDeleting: false,
  submitError: null,
  fetchError: null,
  importError: null,
  editError: null,
  missingAnalyses: [],
  refreshTrigger: 0,

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

  importFromPrompt: async (data) => {
    set({ isImporting: true, importError: null, missingAnalyses: [] });
    try {
      const response = await AnalysisService.importFromPrompt(data);
      set((s) => ({
        isImporting: false,
        missingAnalyses: response.list_missing_analysis,
        refreshTrigger: s.refreshTrigger + 1,
      }));
      return response;
    } catch (err) {
      set({ isImporting: false, importError: (err as Error).message });
      return null;
    }
  },

  updateAnalysis: async (analysisId, data) => {
    set({ isUpdating: true, editError: null });
    try {
      await AnalysisService.updateAnalysis(analysisId, data);
      set((s) => ({ isUpdating: false, refreshTrigger: s.refreshTrigger + 1 }));
      return true;
    } catch (err) {
      set({ isUpdating: false, editError: (err as Error).message });
      return false;
    }
  },

  deleteAnalysis: async (analysisId) => {
    set({ isDeleting: true, editError: null });
    try {
      await AnalysisService.deleteAnalysis(analysisId);
      set((s) => ({ isDeleting: false, refreshTrigger: s.refreshTrigger + 1 }));
      return true;
    } catch (err) {
      set({ isDeleting: false, editError: (err as Error).message });
      return false;
    }
  },

  clearSubmitError: () => set({ submitError: null }),
  clearFetchError: () => set({ fetchError: null }),
  clearImportError: () => set({ importError: null }),
  clearMissingAnalyses: () => set({ missingAnalyses: [] }),
  clearEditError: () => set({ editError: null }),
}));
