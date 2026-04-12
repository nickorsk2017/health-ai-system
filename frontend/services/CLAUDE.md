# Services Rules

## Purpose
All HTTP communication with the backend. The only place `fetch` is called.

## Rules
- One class per domain resource (e.g. `AuthService`, `UserService`).
- All methods are `static async`.
- Return typed values using `Entity` namespace types.
- Throw typed errors on failure. Never swallow errors silently.
- No UI logic, no store writes. Pure data-fetching layer.
- Base URL from environment variable only (`process.env.NEXT_PUBLIC_API_URL`).

## Naming
- File: `{Domain}Service.ts` (e.g. `AuthService.ts`).
- Methods: verb + noun (e.g. `getById`, `createUser`, `deleteSession`).

## Pattern
```ts
export class UserService {
  private static base = `${process.env.NEXT_PUBLIC_API_URL}/users`;

  static async getById(id: string): Promise<Entity.User> {
    const res = await fetch(`${this.base}/${id}`);
    if (!res.ok) throw new Error(`UserService.getById failed: ${res.status}`);
    return res.json();
  }

  static async getAll(): Promise<Entity.User[]> {
    const res = await fetch(this.base);
    if (!res.ok) throw new Error(`UserService.getAll failed: ${res.status}`);
    return res.json();
  }
}
```

## Forbidden
- Importing from `stores/`, `components/`, or `app/`
- Calling other services directly
- Hardcoded URLs
