# Storybook on GitHub Pages

The `Storybook Pages` workflow (`.github/workflows/storybook_pages.yml`) publishes
Storybook to the `gh-pages` branch.

## Layout

Each source gets its own isolated folder under `storybook/`:

| Path | Source | Trigger |
| --- | --- | --- |
| `storybook/main/` | `main` branch | push to `main`, or manual dispatch `deploy_type: main` |
| `storybook/branch/<name>/` | any branch | manual dispatch `deploy_type: branch-preview` |
| `storybook/pr/<number>/` | a pull request | PR labelled `storybook` |
| `storybook/index.html` | — | redirects to `storybook/main/` |

## Deploy a branch preview without a PR

Run the workflow manually (Actions → Storybook Pages → Run workflow) from the
branch, keeping `deploy_type: branch-preview`. The run summary prints the URL.
A branch preview stays up until its branch is deleted; merges to `main` and other
previews never remove it.

## Why isolated folders

`JamesIves/github-pages-deploy-action` cleans with `rsync --delete` scoped to its
`target-folder`. Giving each source its own folder means a deploy can only delete
its own files.

**Invariant:** no job deploys to the `storybook/` root with `clean: true`. The
root only receives `.nojekyll` and the redirect `index.html`, written with
`clean: false`.

## Cleanup

- Closing a PR removes `storybook/pr/<number>/`.
- Deleting a branch removes `storybook/branch/<name>/`.

Cleanup jobs push directly to `gh-pages` and retry with `git pull --rebase` because
a concurrent `main` deploy can move the branch under them.
