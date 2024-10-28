##
# docker pull ghcr.io/lreis2415/autofuzslppos:latest
# or
# docker pull registry.cn-hangzhou.aliyuncs.com/ljzhu-geomodels/autofuzslppos:latest
#
# Build by yourself (DO NOT MISSING the dot at the end of the line):
#   > cd AutoFuzSlpPos
#   > docker build -t autofuzslppos:dev-latest -f docker/Dockerfile .
#
# Copyright 2024 Liang-Jun Zhu <zlj@lreis.ac.cn>
#

## Create pyslppos environment
# References:
#  https://pythonspeed.com/articles/activate-conda-dockerfile/
#  https://medium.com/@rvaid.29/reduce-the-size-of-conda-based-docker-images-3f7f713d3a8f
FROM continuumio/miniconda3:24.7.1-0 AS pybuilder

# Copy source directory
WORKDIR /slppos
COPY . .

# 1. Install conda-pack
# 2. Create new conda environment for pyslppos
# 3. Package the environment as tar using conda-pack
# 4. Unpack the environment in /venv using conda-unpack
RUN conda install -c conda-forge conda-pack && \
    conda env create -f ./pyAutoFuzSlpPos_env.yml && \
    conda-pack -n pyslppos -o /tmp/env.tar && \
    mkdir /venv && \
    cd /venv && \
    tar -xf /tmp/env.tar && \
    rm /tmp/env.tar && \
    /venv/bin/conda-unpack

# Use taudem_ext:debian as base image for the runner
# https://github.com/lreis2415/TauDEM_ext/pkgs/container/taudem_ext
FROM ghcr.io/lreis2415/taudem_ext:debian AS runner

# Copy the environment directory /venv from the pybuilder stage
COPY --from=pybuilder /venv /venv

# These ENV variables have been set in taudem_ext:debian
#ENV OMPI_ALLOW_RUN_AS_ROOT=1
#ENV OMPI_ALLOW_RUN_AS_ROOT_CONFIRM=1

COPY docker/pyslppos.sh /
# Copy source directory
WORKDIR /slppos
COPY autofuzslppos autofuzslppos
COPY demo demo
COPY data data

SHELL ["/bin/bash", "-c"]
# The taudem_ext:debian already set the /docker-entrypoint.sh
#COPY docker/docker-entrypoint.sh /
#ENTRYPOINT ["/usr/bin/tini", "--", "/docker-entrypoint.sh"]
