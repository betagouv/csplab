# Web linting

The web app uses different tools depending on the source type:

- ESLint for the frontend app, Django app SCSS, and candidate app JS
- Ruff for Python
- djlint for Django templates
- mypy for Python type checking

## ESLint setup

One ESLint config, [src/web/eslint.config.mjs](src/web/eslint.config.mjs), covers the Vite frontend, the Django app SCSS and the candidate app JS.

## In the editor

- CSS, SCSS, and Vue are formatted through ESLint
- TypeScript, JavaScript, JSON, and JSONC use ESLint code actions instead of format-on-save

## Main commands

```bash
mise run web:lint
mise run lint
```

`mise run lint:fix` also recompiles the committed Django app CSS after SCSS autofixes.

```bash
cd src/web && pnpm run lint:styles:fix
cd src/web && pnpm run lint:candidate-js:fix
cd src/web && pnpm exec eslint "frontend/src/styles/**/*.{css,scss}" --fix
```
