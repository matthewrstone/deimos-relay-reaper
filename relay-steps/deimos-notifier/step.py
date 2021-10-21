#!/usr/bin/python
from datetime import datetime, timezone
import json
import os

from relay_sdk import Interface, Dynamic as D
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

def get_time_left(exp_date):
    return datetime.strptime(exp_date, '%Y-%m-%d %H:%M:%S %z') - datetime.now(timezone.utc)

def main():
    # TODO: The owner is captured in the data so we should be able to notify them
    relay = Interface()
    client = WebClient(token=relay.get(D.slack_token))
    data = json.loads(relay.get(D.data))
    notify_type = relay.get(D.notify_type)
    response = []
    delete_set = []
    healthy_set = []

    for item in data:
        # Retreive the user id from Slack by looking up the user by email.
        user = client.users_lookupByEmail(email=data[item]['owner'])['user']['id']
        # Set a default message. In no way should this get through.
        message = 'If you are seeing this we need to troubleshoot the Relay workflows.'
        # Set the notify message. User id must be written as <@userid> with the gt lt.
        if notify_type == 'expiring' and data[item]['status'] == 'expiring':
            message = 'Hey, <@{}>! Your Deimos environment, **{}**, is expiring soon! ({})'.format(
                user,
                item,
                str(get_time_left(data[item]['exp_date']))
            )
            client.chat_postMessage(
                channel='#proj-deimos-notify',
                text=message
            )
        elif notify_type == 'expired' and data[item]['status'] == 'expired':
            message = 'Times up, <@{}>!, Deimos environment **{}** has expired and will be reaped shortly!'.format(
                user,
                item
            )
            client.chat_postMessage(
                channel='#proj-deimos-notify',
                text=message
            )
            # Create a delete set for reaping Terraform environments in a later step
            delete_set.append(item)

        elif data[item]['status'] == 'healthy':
            healthy_set.append(item)
        
        # Dump the messages to outputs. This is just for easy debug via Relay.
        response.append({item: message})
    relay.outputs.set("data", json.dumps(response, default=str))
    relay.outputs.set("delete_set", json.dumps(delete_set, default=str))
    relay.outputs.set("healthy_set", json.dumps(healthy_set, default=str))

if __name__ == "__main__":
    main()