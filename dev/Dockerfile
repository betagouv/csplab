FROM python:3.12-slim

# Install system dependencies
RUN apt-get update && \
    apt-get install -y \
      git \
      make && \
    rm -rf /var/lib/apt/lists/*

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Create dev user with configurable UID/GID
ARG DOCKER_UID=1000
ARG DOCKER_GID=1000

# Create group and user
RUN groupadd -g ${DOCKER_GID} dev || true
RUN useradd -m -u ${DOCKER_UID} -g ${DOCKER_GID} -s /bin/bash dev

# Set working directory for installation
WORKDIR /workspace

# Copy dependency files
COPY dev/pyproject.toml dev/uv.lock ./

# Install Python dependencies
RUN uv sync --frozen

# Switch to dev user
USER dev

# Set working directory for runtime
WORKDIR /workspace

# Default command
CMD ["bash"]
