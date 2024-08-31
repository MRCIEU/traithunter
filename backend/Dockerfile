FROM mambaorg/micromamba:latest
USER root
RUN apt update && apt install -y make
COPY backend/environment.yml /tmp/environment.yml
RUN micromamba install -y -n base -f /tmp/environment.yml && \
  micromamba clean --all --yes
ARG MAMBA_DOCKERFILE_ACTIVATE=1
WORKDIR /app
RUN mkdir -p /common_funcs/src/common_funcs && \
  touch /common_funcs/src/common_funcs/__init__.py
COPY common_funcs/setup.cfg \
  common_funcs/setup.py \
  /common_funcs/
RUN python -m pip install -e /common_funcs
