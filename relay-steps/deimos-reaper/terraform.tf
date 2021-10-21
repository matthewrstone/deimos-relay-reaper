# DUMMY TERRAFORM
# Used to supply backend configs via Relay to destroy Deimos environments.
# Please see the corresponding relay-workflows/the-reaper.yaml workflow.

terraform {
  backend "s3" {}
}

provider "aws" {
  region = "us-west-2"
}