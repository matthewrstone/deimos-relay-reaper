#!/bin/bash
set -euo pipefail

# ???
JQ="${JQ:-jq}"
NI="${NI:-ni}"

# Get the python script name and subdirectory in the git project
SCRIPT_NAME="$(ni get -p {.script_name})"
DIRECTORY="$(ni get -p {.directory})"


# Create the AWS credentials
AWS=$(ni get -p {.aws})
if [ -n "${AWS}" ]; then
  ni aws config
  export AWS_SHARED_CREDENTIALS_FILE=/workspace/.aws/credentials
fi

# Export the default AWS region
export AWS_DEFAULT_REGION="$(ni get -p {.aws.region})"

# Clone the git repository
GIT=$(ni get -p {.git})
if [ -n "${GIT}" ]; then
  ni git clone
  NAME=$(ni get -p {.git.name})
fi

# Change to the project directiory
cd /workspace/${NAME}/${DIRECTORY}

# Execute script
python $SCRIPT_NAME > output.json

# Convert output for Relay
ni output set --key data --json --value "$(jq output.json)"
