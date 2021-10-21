#!/usr/bin/python
from datetime import datetime, timezone
import json
import os

from relay_sdk import Interface, Dynamic as D
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

def reap(item):
  print('Terraform logic will go here')

def notify(item):
  print('Slack notify will go here')

def main():
    relay = Interface()
    client = WebClient(token=relay.get(D.slack_token))
    delete_set = json.loads(relay.get(D.delete_set))
    response = []

    if delete_set == []:
      relay.outputs.set("response", "No environment's to reap! Back to bed.")
    else:
      for item in delete_set:
        reap(item)
        notify(item)

if __name__ == "__main__":
    main()