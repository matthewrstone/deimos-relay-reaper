#from python:3.10.0-alpine
from ubuntu:latest
ENV TZ=America/Chicago
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone && \
    apt-get update -y && \
    apt-get upgrade -y && \    
    apt-get install -y git curl apt-utils unzip cmake python3.9 python3-pip wget jq && \
    update-alternatives --install /usr/bin/python python /usr/bin/python3.9 1 && \
    python -m pip install boto3[crt] requests slack_sdk relay_sdk && \
    wget https://releases.hashicorp.com/terraform/1.0.9/terraform_1.0.9_linux_amd64.zip && \
    unzip terraform_1.0.9_linux_amd64.zip && \
    rm -f terraform_1.0.9_linux_amd64.zip && \
    chmod a+x terraform && \
    mv terraform /usr/bin/terraform
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
COPY terraform.tf /relay/terraform.tf
COPY step.py /relay/step.py
RUN chmod 755 /relay/step.py

ENTRYPOINT /relay/step.py

LABEL "org.opencontainers.image.title"="Relay Python Container"
LABEL "org.opencontainers.image.description"="An Alpine Linux image that executes a Python script."
LABEL "com.puppet.nebula.sdk.version"="v1"