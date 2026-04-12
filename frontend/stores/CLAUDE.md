# Stores Rules

## Purpose
Global client-side state management via Zustand.

## Rules
- One store per domain (e.g. `useAuthStore.ts`, `useUserStore.ts`).
- Store actions call `services/` and update state.
- No store imports other stores directly (compose at component level).
- State shape typed via `Entity` namespace.
- No server-side data in stores. Stores are client-only (`"use client"` context).

## Naming
- File: `use{Domain}Store.ts`
- Hook export: `use{Domain}Store`

## Pattern
```ts
"use client";
import { create } from "zustand";
import { UserService } from "@/services/UserService";

type State = {
  users: Entity.User[];
  selected: Entity.User | null;
  fetchAll: () => Promise<void>;
  select: (user: Entity.User) => void;
  reset: () => void;
};

export const useUserStore = create<State>((set) => ({
  users: [],
  selected: null,
  fetchAll: async () => {
    const users = await UserService.getAll();
    set({ users });
  },
  select: (user) => set({ selected: user }),
  reset: () => set({ users: [], selected: null }),
}));
```

## Forbidden
- Calling `fetch()` directly in stores (use services)
- Importing from `components/` or `app/`
- Persisting sensitive data (tokens belong in httpOnly cookies)
