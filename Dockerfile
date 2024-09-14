FROM python:3.10.12-slim AS compile-image

COPY requirements.txt .
RUN pip install --user -r requirements.txt


FROM python:3.10.12-slim AS build-image
COPY --from=compile-image /root/.local /root/.local

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PATH=/root/.local/bin:$PATH
ENV WORKDIR=/

WORKDIR $WORKDIR

COPY ./bot $WORKDIR
