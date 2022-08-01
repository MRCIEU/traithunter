FROM continuumio/miniconda3:4.10.3
RUN apt update && apt install -y make
COPY backend/environment.yml ./
RUN conda env create -f environment.yml
RUN echo "conda activate phenotype-api" >> ~/.bashrc
SHELL ["/bin/bash", "--login", "-c"]
ENV PATH /opt/conda/envs/phenotype-api/bin:$PATH
WORKDIR /app
RUN mkdir -p /common_funcs/src/common_funcs && \
  touch /common_funcs/src/common_funcs/__init__.py
COPY common_funcs/setup.cfg \
  common_funcs/setup.py \
  /common_funcs/
RUN /opt/conda/envs/phenotype-api/bin/python -m pip install -e /common_funcs
