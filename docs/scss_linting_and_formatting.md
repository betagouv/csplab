# Styles linting & formatting

VS Code extensions for editor-based styles linting and formatting, following no node dependencies philosophy in repository.

## Recommended extensions

- **Prettier** (`esbenp.prettier-vscode`) - Formatting
- **Stylelint** (`stylelint.vscode-stylelint`) - Linting

## Configuration

- [.vscode/settings.json](.vscode/settings.json) - Editor behavior (format on save, auto-fix)
- [.prettierrc.json](.prettierrc.json) - Formatting rules (indentation, line length, quotes)
- [.stylelintrc.json](.stylelintrc.json) - Linting rules (errors, best practices)

## Behavior

Format on save, inline errors, auto-fix. Extensions handle their own Node.js runtime.

## CLI alternative (npx)

For CI or command-line usage without installing extensions:

```bash
# Lint (requires postcss-scss for SCSS syntax support)
npx --yes -p stylelint -p postcss-scss stylelint --custom-syntax postcss-scss "src/tycho/presentation/assets/**/*.scss"

# Format
npx --yes prettier --write "src/tycho/presentation/assets/**/*.scss"
```

No `package.json` required. Node.js downloads tools ephemerally.
