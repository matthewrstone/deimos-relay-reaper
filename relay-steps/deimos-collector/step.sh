#!/bin/bash
set -euo pipefail

JQ="${JQ:-jq}"
NI="${NI:-ni}"
# The name of the python script
SCRIPT_NAME="$(ni get -p {.script_name})"

# Dump generic credentials, AWS, Azure, or GCP credential sets onto the step container.
CREDENTIALS=$(ni get -p {.credentials})
if [ -n "${CREDENTIALS}" ]; then
  ni credentials config
  export GOOGLE_APPLICATION_CREDENTIALS=/workspace/credentials.json
fi

GOOGLE=$(ni get -p {.google})
if [ -n "${GOOGLE}" ]; then
  ni gcp config -d "/workspace/.gcp"
  export GOOGLE_APPLICATION_CREDENTIALS=/workspace/.gcp/credentials.json
fi

AWS=$(ni get -p {.aws})
if [ -n "${AWS}" ]; then
  ni aws config
  export AWS_SHARED_CREDENTIALS_FILE=/workspace/.aws/credentials
fi

AZURE=$(ni get -p {.azure})
if [ -n "${AZURE}" ]; then
  eval "$( ni azure arm env )"
fi

# Clone the git repository
GIT=$(ni get -p {.git})
if [ -n "${GIT}" ]; then
  ni git clone
  NAME=$(ni get -p {.git.name})
  DIRECTORY="/workspace/${NAME}/${DIRECTORY}"
  # Resolve requirements.txt
  if [ -n "/workspace/${NAME}/${DIRECTORY}/requirements.txt" ]; then
    pip -r /workspace/${NAME}/${DIRECTORY}/requirements.txt
  fi

fi

python $SCRIPT_NAME > output.json
ni output set --key data --json --value "$(jq output.json)"

# ni set output from the step
# ni output set --key KEY --json --value VALUE 