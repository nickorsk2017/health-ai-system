# Types Rules

## Purpose
Single source of truth for all TypeScript types in the frontend.

## Rules
- All application types live here. No type definitions elsewhere.
- All types are declared inside the global `Entity` namespace.
- Root file is `entity.d.ts` — contains the namespace declaration shell.
- Each domain gets its own `{domain}.d.ts` file inside the namespace.
- No imports inside `.d.ts` files (ambient declarations only).
- No utility types or helpers here — only data shape declarations.

## Root File: entity.d.ts
```ts
declare global {
  namespace Entity {}
}
```

## Child Type File Pattern ({domain}.d.ts)
```ts
declare namespace Entity {
  type User = {
    id: string;
    full_name: string;
    address: string;
  };

  type UserRole = "admin" | "member" | "guest";
}
```

## Naming
- Types: PascalCase (`User`, `AuthSession`, `DashboardStats`).
- Union/literal types: PascalCase (`UserRole`, `ThemeMode`).
- File names: lowercase domain (`user.d.ts`, `auth.d.ts`).

## Forbidden
- `interface` — use `type` exclusively.
- `any`, `unknown` without a narrowing guard.
- Non-Entity types in this folder (no util types, no component prop types).

## Example Structure
```
types/
├── entity.d.ts    # namespace shell
├── user.d.ts
├── auth.d.ts
└── dashboard.d.ts
```
