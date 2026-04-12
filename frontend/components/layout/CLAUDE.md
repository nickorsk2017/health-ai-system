# Layout Components Rules

## Purpose
Structural page scaffolding. No domain logic.

## Rules
- Layout components define page structure only: Header, Footer, Sidebar, Nav, PageWrapper.
- No domain data fetching. Receive everything via props or slots.
- No imports from `features/` or `stores/`.
- May import from `common/`.
- Typically server components unless navigation state requires client.

## Naming
- Describe structural role: `Header`, `Sidebar`, `PageContainer`, `NavBar`.
- Not domain names: not `UserDashboardLayout`.

## Example Structure
```
layout/
├── Header/
│   └── Header.tsx
├── Sidebar/
│   └── Sidebar.tsx
├── Footer/
│   └── Footer.tsx
└── PageContainer/
    └── PageContainer.tsx
```

## Allowed Imports
- `@/components/common/*`
- `@/utils/*`
- `@/types` (via Entity namespace — navigation items, etc.)

## Forbidden
- `@/stores/*`
- `@/services/*`
- `@/components/features/*`
