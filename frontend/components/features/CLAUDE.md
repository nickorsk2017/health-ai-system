# Features Components Rules

## Purpose
Domain-specific UI components tied to business concepts.

## Rules
- One subfolder per domain (e.g. `auth/`, `user/`, `dashboard/`).
- May read from Zustand stores via hooks.
- Must not call `services/` directly — trigger store actions instead.
- May be client components (`"use client"`) when user interaction is needed.
- Receive initial/server data via props from `app/` pages.

## Folder Per Feature
```
features/
├── auth/
│   ├── LoginForm.tsx
│   └── RegisterForm.tsx
├── user/
│   ├── UserProfile.tsx
│   └── UserList.tsx
└── dashboard/
    └── DashboardStats.tsx
```

## Data Flow Pattern
```
app/page.tsx         → fetches via service, passes as props
  └── features/X.tsx → reads store, dispatches store actions
        └── common/Y → pure UI, no state
```

## Allowed Imports
- `@/components/common/*`
- `@/stores/*`
- `@/types` (via Entity namespace)
- `@/utils/*`

## Forbidden
- Direct `fetch()` or service calls
- Imports from `layout/` or other feature subfolders
