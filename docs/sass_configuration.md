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

- **Sources**: `src/tycho/presentation/assets/styles/`
- **Compiled**: `src/tycho/presentation/static/css/`

Both SCSS and generated CSS files are committed.
