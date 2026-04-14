"use client";

import { create } from "zustand";

import { PatientHistoryService } from "@/services/PatientHistoryService";

type State = {
  history: Entity.PatientHistoryRecord[];
  isSubmitting: boolean;
  isFetchingHistory: boolean;
  isProcessingPrompt: boolean;
  isUpdating: boolean;
  isDeleting: boolean;
  error: string | null;
  promptError: string | null;
  editError: string | null;
  refreshTrigger: number;
  submitHistory: (data: Entity.CreatePatientHistory) => Promise<boolean>;
  fetchHistory: (userId: string, lastHistoryDate: string) => Promise<void>;
  submitByPrompt: (data: Entity.HistoryFromPromptRequest) => Promise<boolean>;
  updateHistory: (historyId: string, data: Entity.UpdatePatientHistory) => Promise<boolean>;
  deleteHistory: (historyId: string) => Promise<boolean>;
  clearError: () => void;
  clearPromptError: () => void;
  clearEditError: () => void;
};

export const usePatientHistoryStore = create<State>((set) => ({
  history: [],
  isSubmitting: false,
  isFetchingHistory: false,
  isProcessingPrompt: false,
  isUpdating: false,
  isDeleting: false,
  error: null,
  promptError: null,
  editError: null,
  refreshTrigger: 0,

  submitHistory: async (data) => {
    set({ isSubmitting: true, error: null });
    try {
      await PatientHistoryService.recordHistory(data);
      set({ isSubmitting: false });
      return true;
    } catch (err) {
      set({ isSubmitting: false, error: (err as Error).message });
      return false;
    }
  },

  fetchHistory: async (userId, lastHistoryDate) => {
    set({ isFetchingHistory: true, error: null, history: [] });
    try {
      const history = await PatientHistoryService.fetchHistory(userId, lastHistoryDate);
      set({ history, isFetchingHistory: false });
    } catch (err) {
      set({ isFetchingHistory: false, error: (err as Error).message });
    }
  },

  submitByPrompt: async (data) => {
    set({ isProcessingPrompt: true, promptError: null });
    try {
      await PatientHistoryService.createByPrompt(data);
      set((s) => ({ isProcessingPrompt: false, refreshTrigger: s.refreshTrigger + 1 }));
      return true;
    } catch (err) {
      set({ isProcessingPrompt: false, promptError: (err as Error).message });
      return false;
    }
  },

  updateHistory: async (historyId, data) => {
    set({ isUpdating: true, editError: null });
    try {
      await PatientHistoryService.updateHistory(historyId, data);
      set((s) => ({ isUpdating: false, refreshTrigger: s.refreshTrigger + 1 }));
      return true;
    } catch (err) {
      set({ isUpdating: false, editError: (err as Error).message });
      return false;
    }
  },

  deleteHistory: async (historyId) => {
    set({ isDeleting: true, editError: null });
    try {
      await PatientHistoryService.deleteHistory(historyId);
      set((s) => ({ isDeleting: false, refreshTrigger: s.refreshTrigger + 1 }));
      return true;
    } catch (err) {
      set({ isDeleting: false, editError: (err as Error).message });
      return false;
    }
  },

  clearError: () => set({ error: null }),
  clearPromptError: () => set({ promptError: null }),
  clearEditError: () => set({ editError: null }),
}));
