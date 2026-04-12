# Utils Rules

## Purpose
Pure, stateless utility functions. No side effects.

## Rules
- Every util is a pure function. Same input → same output. No side effects.
- No imports from `components/`, `services/`, `stores/`, or `app/`.
- One concern per file. Do not group unrelated utils.
- All functions exported as named or default exports (not bundled objects).

## Included Utilities

### cx.ts — Class Name Composer
```ts
type Cx = (...a: Array<undefined | null | string | boolean>) => string;

const cx: Cx = (...args) =>
  args
    .flat()
    .filter((x) => x !== null && x !== undefined && typeof x !== "boolean")
    .join(" ");

export default cx;
```

Usage:
```ts
import cx from "@/utils/cx";
<div className={cx("base-class", isActive && "active", disabled && "opacity-50")} />
```

## Adding New Utils
- File name describes the operation: `formatDate.ts`, `truncate.ts`, `slugify.ts`.
- If a util grows beyond 30 lines, reconsider scope — it may not be a util.
- No async utils. Async logic belongs in `services/`.

## Forbidden
- Importing from anywhere except other pure `utils/` files
- State mutations
- DOM access
- `console.log`
