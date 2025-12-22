FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim

# Paths
ENV KERNELS_PATH=/home/notebook/kernels
ENV WORKDIR=/home/notebook/app

# Create notebook user with configurable UID/GID
# Note hat GID 20 already exists in docker image
ARG DOCKER_UID=1000
RUN useradd -m -u ${DOCKER_UID} -s /bin/bash notebook

# Switch to the notebook user
USER notebook

# Set UV cache directory
ENV UV_CACHE_DIR=/home/notebook/.cache/uv
RUN mkdir -p /home/notebook/.cache/uv

# Set working directory
WORKDIR ${WORKDIR}

# Create directory for thematic kernels
RUN mkdir -p "${KERNELS_PATH}"

# Copy dependency files
COPY --chown=notebook:notebook pyproject.toml uv.lock list-kernels.py ./

# Install Python dependencies
RUN uv sync --frozen

# Create the base kernel
RUN uv run \
      ipython kernel install \
        --user \
        --name=csplab-base \
        --display-name="CSPLab Base (pandas, numpy, matplotlib)"

# Now create all specific kernels
RUN for kernel in $(python list-kernels.py); do \
      KERNEL_PATH="${KERNELS_PATH}/${kernel}"; \
      VIRTUAL_ENV="${KERNEL_PATH}/.venv"; \
      mkdir -p "${KERNEL_PATH}" && \
      cp pyproject.toml uv.lock "${KERNEL_PATH}" && \
      cd "${KERNEL_PATH}" && \
      uv sync --frozen --only-group "${kernel}" && \
      VIRTUAL_ENV="${VIRTUAL_ENV}" uv run \
        ipython kernel install \
          --user \
          --env VIRTUAL_ENV "${VIRTUAL_ENV}" \
          --name="csplab-${kernel}" \
          --display-name="CSPLab ${kernel}"; \
    done

CMD [ \
  "uv", \
  "run", \
  "jupyter", \
  "lab", \
  "--ip=0.0.0.0", \
  "--port=8888", \
  "--no-browser", \
  "--notebook-dir=/home/notebook/app" \
]
