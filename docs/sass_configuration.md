# Sass/SCSS Configuration

This project uses **Dart Sass CLI** (standalone binary) for compiling Sass/SCSS files.

## Prerequisites

[Install Dart Sass](https://sass-lang.com/install/#command-line)

## Usage

Compile once:
```bash
make sass-compile
```

Watch mode (auto-compile on save):
```bash
make sass-watch
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

- **Sources**: `src/tycho/presentation/assets/styles/`
- **Compiled**: `src/tycho/presentation/static/css/main.css`

The compiled CSS is committed to the repository.

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
