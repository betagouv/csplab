# Frontend Icons

## Why a registry

Icons are referenced by name (`<CspIcon name="ri:user-add-line" />`), so Iconify needs
every name registered at startup. An unregistered name used to render nothing — no error,
just a blank space — and Iconify would silently fetch it from its public API.

`src/app/icons.generated.ts` holds that registry. It is generated from the names actually
used in `src/`, so it never drifts from what the app renders.

## When to regenerate it

Whenever you add or remove a `ri:` name in a component. CI fails when the registry is out
of sync with the codebase.

```bash
pnpm icons          # from src/web
```

`pnpm lint` runs the same script with `--check`: it regenerates nothing and exits 1 when
the file is stale.

## What the generator does

It scans `src/**/*.{vue,ts}` for `ri:*` names, then writes one import and one `addIcon`
call per name. A name that does not exist in `@iconify-icons/ri` fails the run with the
files that use it, so a typo is caught before it reaches the browser.

Names must be **string literals**: the scan is static, and a name built at runtime
(`` `ri:${kind}-line` ``) would be missed and render blank.

## Icons missing from the package

A few icons are not published in `@iconify-icons/ri`. Declare them by hand in
`src/app/icons.custom.ts`, with their SVG body; the generator leaves that file alone and
counts its icons as already registered.

## Runtime safety net

`src/app/icons.ts` loads both files and registers a custom loader for the `ri` prefix, so
an unregistered name logs an explicit error instead of reaching the Iconify API.
