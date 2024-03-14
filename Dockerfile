FROM python:3.10.4-slim as python

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN apt-get update && apt-get install --no-install-recommends -y \
    libpq-dev \
    netcat  \
    && apt-get clean

# install dependencies
RUN pip install --upgrade pip
RUN pip install "psycopg[binary, pool]"
COPY ./requirements .
RUN pip install  -r local.txt

# upload scripts
COPY ./scripts/entrypoint.sh ./scripts/start.sh /

# Fix windows docker bug, convert CRLF to LF
RUN sed -i 's/\r$//g' /start.sh && chmod +x /start.sh && \
    sed -i 's/\r$//g' /entrypoint.sh && chmod +x /entrypoint.sh

# set work directory
WORKDIR /app