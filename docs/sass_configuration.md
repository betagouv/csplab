# Sass/SCSS Configuration

This project uses the npm `sass` package from the `src/web` workspace for compiling Sass/SCSS files.

## Usage

Compile once:
```bash
mise run web:build:styles
```

The task skips the compilation when no SCSS source changed since the last run. `bootstrap` and the tasks that serve the Django pages run it first.

Watch mode (auto-compile on save), started by `mise run web:dev:cv`:
```bash
cd src/web && pnpm run watch:styles
```

## File Structure

```
assets/styles/
├── main.scss           # Entry point
├── abstracts/          # Variables, mixins, tokens
├── utilities/          # Helper classes
├── layouts/            # Grid and layout patches
├── components/         # Reusable UI components
└── pages/              # Page-specific styles
```

The sources are in `src/web/presentation/assets/styles/`. Sass compiles them into `src/web/presentation/static/css/main.css`, which git ignores.

On Scalingo, the `build` script of `src/web/package.json` compiles the styles with the frontend.

## DSFR Integration

DSFR CSS is loaded via django-dsfr (`{% dsfr_css %}`). Our SCSS uses DSFR CSS custom properties (design tokens) directly:

```scss
.my-component {
  background-color: var(--background-default-grey);
  color: var(--text-title-grey);
}
```

## Naming Conventions

- **BEM**: `.csplab-{block}__{element}--{modifier}`
- **Utilities**: `.csplab-{property}-{value}`
- **Partials**: Prefixed with `_` (SCSS convention)
