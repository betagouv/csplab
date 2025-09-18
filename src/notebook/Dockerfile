FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim

# Create notebook user with configurable UID/GID
ARG DOCKER_UID=1000

# GID 20 already exists in docker image
RUN useradd -m -u ${DOCKER_UID} -s /bin/bash notebook

# Switch to the notebook user
USER notebook

# Set working directory
WORKDIR /home/notebook/app

# Create directory structure for app and thematic kernels
RUN mkdir -p /home/notebook/app && \
    mkdir -p /home/notebook/kernels/nlp

# Copy dependency files
COPY pyproject.toml uv.lock ./

# Install Python dependencies
RUN uv sync --frozen

# Create NLP kernel
RUN cd /home/notebook/kernels/nlp && \
    uv init --name csplab-nlp && \
    uv add pandas numpy matplotlib ipykernel spacy transformers

# Now create all kernels as the notebook user with specific environment variables
RUN uv run \
      ipython kernel install \
        --user \
        --name=csplab-base \
        --display-name="CSPLab Base (pandas, numpy, matplotlib)"

RUN cd /home/notebook/kernels/nlp && \
    uv run \
      ipython kernel install \
        --user \
        --env VIRTUAL_ENV $(pwd)/.venv \
        --name=csplab-nlp \
        --display-name="CSPLab NLP (spacy, transformers)"

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
