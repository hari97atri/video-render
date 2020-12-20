FROM python:3.7.6-alpine3.10

# Create the config directory
RUN mkdir /config

RUN echo "https://dl-4.alpinelinux.org/alpine/v3.10/main" > /etc/apk/repositories
RUN echo "https://dl-4.alpinelinux.org/alpine/v3.10/community" >> /etc/apk/repositories

COPY config/ /config/

RUN apk add --no-cache --virtual .build-deps \
            python3-dev \
            jpeg-dev \
            zlib-dev \
            gcc \
            make \
            libc-dev \
            musl-dev \
            linux-headers \
            pcre-dev \
            ffmpeg

RUN pip3 install -r /config/requirements.txt
