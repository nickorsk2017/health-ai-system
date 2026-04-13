"use client";

import { create } from "zustand";

import { PatientService } from "@/services/PatientService";

const STORAGE_KEY = "health_os_selected_patient_id";

type State = {
  patients: Entity.MockPatient[];
  selectedPatientId: string | null;
  isInitialized: boolean;
  isCreating: boolean;
  initError: string | null;
  createError: string | null;
  init: () => Promise<void>;
  setSelectedPatientId: (id: string) => void;
  createPatient: (form: Entity.NewPatientForm) => Promise<void>;
  clearCreateError: () => void;
};

export const usePatientStore = create<State>((set) => ({
  patients: [],
  selectedPatientId: null,
  isInitialized: false,
  isCreating: false,
  initError: null,
  createError: null,

  init: async () => {
    const storedId =
      typeof window !== "undefined" ? localStorage.getItem(STORAGE_KEY) : null;
    try {
      const patients = await PatientService.getAll();
      const selectedPatientId =
        storedId && patients.some((p) => p.id === storedId) ? storedId : null;
      set({ patients, selectedPatientId, isInitialized: true });
    } catch {
      set({ patients: [], selectedPatientId: null, isInitialized: true, initError: "Could not reach patient service." });
    }
  },

  setSelectedPatientId: (id) => {
    if (typeof window !== "undefined") {
      localStorage.setItem(STORAGE_KEY, id);
      window.location.reload();
    }
  },

  createPatient: async (form) => {
    set({ isCreating: true, createError: null });
    try {
      const patient = await PatientService.create(form);
      if (typeof window !== "undefined") {
        localStorage.setItem(STORAGE_KEY, patient.id);
        window.location.reload();
      }
    } catch (err) {
      set({ isCreating: false, createError: (err as Error).message });
    }
  },

  clearCreateError: () => set({ createError: null }),
}));
