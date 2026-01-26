# SCSS style guide

Guidelines for writing maintainable SCSS in this project.

## Structure

Use `@use`/`@forward` module system. Every partial imports abstracts:

```scss
@use "../abstracts" as *;
```

## Nesting

- **States/pseudo-classes**: Use `&`
- **BEM elements**: Use full selector for searchability

```scss
.csplab-card {
  // base styles

  &:hover { ... }
  &[data-active="true"] { ... }

  .csplab-card__title { ... }
  .csplab-card__content { ... }
}
```

## Variables

| Type | Source | Example |
|------|--------|---------|
| DSFR colors | CSS custom properties | `var(--text-title-blue-france)` |
| Custom colors | `_colors.scss` | `$hero-gradient` |
| Spacing | `_spacing.scss` | `$sp-2w` (1rem) |
| Breakpoints | `_breakpoints.scss` | `$md` (48em) |

## Spacing Tokens

DSFR units: `v` = 0.25rem, `w` = 0.5rem

| Token | Value |
|-------|-------|
| `$sp-1v` | 0.25rem |
| `$sp-1w` | 0.5rem |
| `$sp-2w` | 1rem |
| `$sp-3w` | 1.5rem |
| `$sp-4w` | 2rem |

## Breakpoints

```scss
@include md { ... }     // ≥ 48em
@include lt-md { ... }  // < 48em
```

## Utilities

Use vendored DSFR utilities for layout gaps:

```html
<div class="fr-stack-3w">  <!-- vertical spacing -->
<div class="fr-gap-2w">    <!-- flex/grid gap -->
```

## Naming

- Components: `.csplab-{component}__{element}`
- Keyframes: `csplab-{animation-name}`
