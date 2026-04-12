# Frontend Rules

## Stack
- Next.js (App Router), TypeScript, Tailwind CSS, Zustand

## Folder Map
```
frontend/
├── app/         # Server components, routing, layouts
├── components/  # UI building blocks
│   ├── common/  # Shared, generic components
│   ├── features/# Domain-specific components
│   └── layout/  # Page structure components
├── services/    # API communication layer
├── stores/      # Global client state (Zustand)
├── types/       # All TypeScript types (*.d.ts)
└── utils/       # Pure utility functions
```

## Rules

### General
- TypeScript strict mode. No `any`. No type assertions without justification.
- All types live in `types/`. Never inline complex types in component files.
- Tailwind only for styling. No inline styles. No CSS modules.
- No logic in `app/`. No logic in `components/`. Logic lives in `services/` or `stores/`.

### Imports Order
1. React / Next.js
2. Third-party libraries
3. Internal absolute imports (`@/services`, `@/stores`, `@/types`)
4. Relative imports

### Naming
- Components: PascalCase files and exports.
- Services: PascalCase class name + `Service` suffix (e.g. `AuthService`).
- Stores: camelCase with `use` prefix (e.g. `useAuthStore`).
- Types: PascalCase within `Entity` namespace.
- Utils: camelCase.
