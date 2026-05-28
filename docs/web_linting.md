# Web linting

The web app uses different tools depending on the source type:

- ESLint for the frontend app, Django app SCSS, and candidate app JS
- Ruff for Python
- djlint for Django templates
- mypy for Python type checking

## ESLint setup

There are two ESLint configs, and both are needed:

- [src/web/presentation/frontend/eslint.config.js](src/web/presentation/frontend/eslint.config.js) for the Vite frontend
- [src/web/eslint.config.mjs](src/web/eslint.config.mjs) for Django app SCSS and candidate app JS

## In the editor

- CSS, SCSS, and Vue are formatted through ESLint
- TypeScript, JavaScript, JSON, and JSONC use ESLint code actions instead of format-on-save

## Main commands

```bash
make lint-web
make lint
```

`make lint-fix` also recompiles the committed Django app CSS after SCSS autofixes.

```bash
cd src/web && pnpm run lint:styles:fix
cd src/web && pnpm run lint:candidate-js:fix
cd src/web/presentation/frontend && pnpm exec eslint "src/styles/**/*.{css,scss}" --fix
```
