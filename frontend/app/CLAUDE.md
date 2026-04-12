# App Folder Rules

## Purpose
Routing and page composition only. No business logic.

## Rules
- Every file in this folder is a React Server Component (RSC).
- No `"use client"` in this folder. Ever.
- No data fetching logic inline. Call `services/` functions from page components.
- No state, no hooks, no event handlers.
- Pages receive data and pass it to `components/features/` components as props.
- `layout.tsx` files handle only structural composition and metadata.
- Route groups `(group)/` for logical organization without affecting URL.

## Allowed
```ts
// page.tsx — allowed pattern
import { UserService } from "@/services/UserService";
import { UserProfile } from "@/components/features/UserProfile";

export default async function UserPage({ params }: { params: { id: string } }) {
  const user = await UserService.getById(params.id);
  return <UserProfile user={user} />;
}
```

## Forbidden
- useState, useEffect, useCallback, or any hook
- Event handlers (onClick, onChange, etc.)
- Conditional rendering based on client state
- Direct fetch() calls or database queries
