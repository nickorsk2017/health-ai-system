"use client";

import { create } from "zustand";

import { DeviceService } from "@/services/DeviceService";

type State = {
  devices: Entity.Device[];
  isFetching: boolean;
  isAdding: boolean;
  isDeleting: string | null;
  fetchError: string | null;
  addError: string | null;
  fetchDevices: (userId: string) => Promise<void>;
  addDevice: (userId: string, form: Entity.AddDeviceForm) => Promise<boolean>;
  removeDevice: (userId: string, deviceId: string) => Promise<boolean>;
  clearAddError: () => void;
  clearFetchError: () => void;
};

export const useDeviceStore = create<State>((set) => ({
  devices: [],
  isFetching: false,
  isAdding: false,
  isDeleting: null,
  fetchError: null,
  addError: null,

  fetchDevices: async (userId) => {
    set({ isFetching: true, fetchError: null });
    try {
      const devices = await DeviceService.getByUser(userId);
      set({ devices, isFetching: false });
    } catch (err) {
      set({ isFetching: false, fetchError: (err as Error).message });
    }
  },

  addDevice: async (userId, form) => {
    set({ isAdding: true, addError: null });
    try {
      await DeviceService.add(userId, form);
      const devices = await DeviceService.getByUser(userId);
      set({ devices, isAdding: false });
      return true;
    } catch (err) {
      set({ isAdding: false, addError: (err as Error).message });
      return false;
    }
  },

  removeDevice: async (userId, deviceId) => {
    set({ isDeleting: deviceId });
    try {
      await DeviceService.remove(deviceId);
      const devices = await DeviceService.getByUser(userId);
      set({ devices, isDeleting: null });
      return true;
    } catch (err) {
      set({ isDeleting: null, fetchError: (err as Error).message });
      return false;
    }
  },

  clearAddError: () => set({ addError: null }),
  clearFetchError: () => set({ fetchError: null }),
}));
