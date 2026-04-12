# Common Components Rules

## Purpose
Generic, reusable UI components with zero domain knowledge.

## Rules
- No imports from `features/`, `stores/`, or `services/`.
- No hardcoded text or domain-specific labels.
- Props are the only interface. Fully controlled externally.
- Internal state permitted only for pure UI behavior (tooltip visibility, dropdown open state).
- Every component must be usable in isolation (Storybook-ready mentally).

## Naming
- Describe the UI element, not the domain concept.
- `Button` not `SubmitUserButton`.
- `Modal` not `DeleteConfirmModal`.
- `Avatar` not `UserAvatar`.

## Example Structure
```
common/
├── Button/
│   └── Button.tsx
├── Input/
│   └── Input.tsx
├── Modal/
│   └── Modal.tsx
└── Avatar/
    └── Avatar.tsx
```

## Props Pattern
```ts
type Props = {
  variant?: "primary" | "secondary" | "ghost";
  size?: "sm" | "md" | "lg";
  disabled?: boolean;
  onClick?: () => void;
  children: React.ReactNode;
};
```
