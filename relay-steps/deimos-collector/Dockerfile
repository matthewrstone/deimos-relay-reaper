from python:3.10.0-alpine
RUN set -eux ; \
    mkdir -p /tmp/ni && \
    cd /tmp/ni && \
    wget https://packages.nebula.puppet.net/sdk/ni/v1/ni-v1-linux-amd64.tar.xz && \
    wget https://packages.nebula.puppet.net/sdk/ni/v1/ni-v1-linux-amd64.tar.xz.sha256 && \
    echo "$( cat ni-v1-linux-amd64.tar.xz.sha256 )  ni-v1-linux-amd64.tar.xz" | sha256sum -c - && \
    tar -xvJf ni-v1-linux-amd64.tar.xz && \
    mv ni-v1*-linux-amd64 /usr/local/bin/ni && \
    cd - && \
    rm -fr /tmp/ni

COPY "./step.sh" "/step.sh"
ENTRYPOINT "/step.sh"

LABEL "org.opencontainers.image.title"="Relay Python Container"
LABEL "org.opencontainers.image.description"="An Alpine Linux image that executes a Python script."
LABEL "com.puppet.nebula.sdk.version"="v1"