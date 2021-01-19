#FROM continuumio/miniconda3:4.5.12
FROM python:3.8.0-slim-buster

ENV DEBIAN_FRONTEND=noninteractive

RUN pip install \
    minio

WORKDIR /bin/downloader

CMD python download.py