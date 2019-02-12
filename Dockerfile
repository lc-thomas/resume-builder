FROM alpine:latest

RUN apk update
RUN apk add build-base zlib-dev jpeg-dev python3 python3-dev

WORKDIR /tmp
COPY sources/requirements.txt .
RUN python3 -m pip install --no-cache-dir -r requirements.txt

