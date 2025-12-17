#!/usr/bin/env bash

set -eo pipefail

# Paths
KERNELS_PATH="$HOME/.local/share/jupyter/kernels"
NOTEBOOK_DIR="src/notebook"

echo "Setting up Jupyter kernels..."

# Change to notebook directory
cd "${NOTEBOOK_DIR}"

# Install base dependencies
echo "Installing base dependencies..."
uv sync --frozen

# Create the base kernel
echo "Creating base kernel..."
uv run ipython kernel install \
  --user \
  --name=csplab-base \
  --display-name="CSPLab Base (pandas, numpy, matplotlib)"

# Create specific kernels for each dependency group
echo "Creating specific kernels..."
for kernel in $(uv run python list-kernels.py); do
  echo "Creating kernel: $kernel"

  KERNEL_PATH="${KERNELS_PATH}/csplab-${kernel}"
  VENV_PATH="$(pwd)/.venv-${kernel}"

  # Create separate virtual environment for this kernel
  # TODO - use  .python-version file to specify python version
  uv venv "${VENV_PATH}" --python 3.12

  # Install base dependencies first
  VIRTUAL_ENV="${VENV_PATH}" uv sync --frozen

  # Install additional dependencies for this kernel group
  VIRTUAL_ENV="${VENV_PATH}" uv sync --frozen --only-group "${kernel}"

  # Install ipykernel in this environment
  VIRTUAL_ENV="${VENV_PATH}" uv add ipykernel

  # Create kernel spec
  VIRTUAL_ENV="${VENV_PATH}" uv run ipython kernel install \
    --user \
    --name="csplab-${kernel}" \
    --display-name="CSPLab ${kernel}"

  # Update kernel.json to use the correct virtual environment
  KERNEL_JSON="${KERNELS_PATH}/csplab-${kernel}/kernel.json"
  if [ -f "$KERNEL_JSON" ]; then
    # Update the Python path to use the specific virtual environment
    sed -i "s|\"python\"|\"${VENV_PATH}/bin/python\"|g" "$KERNEL_JSON"
  fi
done

echo "✅ All kernels created successfully!"
echo "Available kernels:"
direnv exec . uv run jupyter kernelspec list
