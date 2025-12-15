Author: [vincentporte](https://github.com/vincentporte/)

# INSTALL

## step 1: env vars

`make setup-env` ✅

## step 2: bootstrap

`docker compose build` ❌

```bash
10.15 error: Failed to install: jupyterlab_widgets-3.0.16-py3-none-any.whl (jupyterlab-widgets==3.0.16)
10.15   Caused by: failed to hardlink file from /home/notebook/.cache/uv/archive-v0/YwuTMX-LE8MxaIKs558Bq/jupyterlab_widgets-3.0.16.data/data/share/jupyter/labextensions/@jupyter-widgets/jupyterlab-manager/static/packages_base_lib_index_js-webpack_sharing_consume_default_jquery_jquery.5dd13f8e980fa3c50bfe.js to /home/notebook/kernels/pipelines_opik/.venv/lib/python3.12/site-packages/jupyterlab_widgets-3.0.16.data/data/share/jupyter/labextensions/@jupyter-widgets/jupyterlab-manager/static/packages_base_lib_index_js-webpack_sharing_consume_default_jquery_jquery.5dd13f8e980fa3c50bfe.js: Cross-device link (os error 18)
------
failed to solve: process "/bin/sh -c for kernel in $(python list-kernels.py); do       KERNEL_PATH=\"${KERNELS_PATH}/${kernel}\";       VIRTUAL_ENV=\"${KERNEL_PATH}/.venv\";       mkdir -p \"${KERNEL_PATH}\" &&       cp pyproject.toml uv.lock \"${KERNEL_PATH}\" &&       cd \"${KERNEL_PATH}\" &&       uv sync --frozen --only-group \"${kernel}\" &&       VIRTUAL_ENV=\"${VIRTUAL_ENV}\" uv run         ipython kernel install           --user           --env VIRTUAL_ENV \"${VIRTUAL_ENV}\"           --name=\"csplab-${kernel}\"           --display-name=\"CSPLab ${kernel}\";     done" did not complete successfully: exit code: 2
```

💡FIX: `src/notebook/Dockerfile`

* added: `ENV UV_LINK_MODE=copy` to force copying instead of hardlinking
* does build after dropping docker images, without fix, work on your local env?

## step 3: notebook

❔ tell the kernel to use on top of the notebook? IE, `CSPLab Concours` in `legifrance.ipynb`

## step 4: elasticsearch x notebook

1. first try: ERROR: Elasticsearch exited unexpectedly, with exit code 137
2. second try ✅

## step 5: tycho

1. add `make run-tycho` in `/README.md` for homogeneity 😸

## step 6: lint-fix

1. `ruff check` found 107 errors (16 fixed, 91 remaining), in `*.ipynb` files > ignore them?

# NOTES

## monorepo

1. What are the purposes of `notebook` container?
2. It does not seem to access PG.

## `/bin`

1. seems to be strongly linked to usage of docker

## docker usage

✅ postgresql & elasticsearch
⚠️ notebook & tycho > will try to use `uv` only
❓ dev & bin > I don't feel comfortable with them right now 😸
