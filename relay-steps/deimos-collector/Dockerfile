#from python:3.10.0-alpine
from ubuntu:latest
ENV TZ=America/Chicago
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone && \
    apt-get update -y && \
    apt-get upgrade -y && \
    apt-get install -y git cmake python3.9 python3-pip wget jq && \
    update-alternatives --install /usr/bin/python python /usr/bin/python3.9 1 && \
    python -m pip install boto3[crt] requests 
RUN set -eux ; \
    mkdir -p /tmp/ni && \
    cd /tmp/ni && \
    wget https://packages.nebula.puppet.net/sdk/ni/v1/ni-v1-linux-amd64.tar.xz && \
    wget https://packages.nebula.puppet.net/sdk/ni/v1/ni-v1-linux-amd64.tar.xz.sha256 && \
    echo "$( cat ni-v1-linux-amd64.tar.xz.sha256 )  ni-v1-linux-amd64.tar.xz" | sha256sum -c - && \
    tar -xvJf ni-v1-linux-amd64.tar.xz && \
    mv ni-v1*-linux-amd64 /usr/local/bin/ni && \
    cd - && \
    rm -fr /tmp/ni && \
    mkdir /relay
COPY step.sh /relay/step.sh
RUN chmod 755 /relay/step.sh

ENTRYPOINT /relay/step.sh

LABEL "org.opencontainers.image.title"="Relay Python Container"
LABEL "org.opencontainers.image.description"="An Alpine Linux image that executes a Python script."
LABEL "com.puppet.nebula.sdk.version"="v1"