# Components Rules

## Subfolders
```
components/
├── common/    # Reusable, domain-agnostic UI (Button, Input, Modal)
├── features/  # Domain components tied to a business concept
└── layout/    # Structural containers (Header, Sidebar, Footer)
```

## Rules

### All Components
- One component per file. Filename matches export name.
- Props typed via `Entity` namespace or local inline type for simple cases.
- No API calls. No store reads/writes. Receive data via props.
- Use `cx()` from `@/utils/cx` for conditional class composition.
- Client components use `"use client"` at the top. Minimize their scope.

### common/
- Zero domain knowledge. No imports from `features/` or `stores/`.
- Fully controlled via props. No internal state except UI state (open/closed).

### features/
- One folder per domain concept (e.g. `features/auth/`, `features/user/`).
- May read from `stores/`. Must not write to `services/` directly — delegate to store actions.
- May be client components when interactivity is required.

### layout/
- Structural only. No domain logic.
- May import from `common/`. Must not import from `features/`.

## Forbidden in All Components
- Direct `fetch()` or `axios` calls
- Business logic or data transformation
- Hardcoded strings for user-facing text (use constants or i18n)
