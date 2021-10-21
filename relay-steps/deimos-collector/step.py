#!/usr/bin/python
from datetime import datetime, timedelta, timezone
from relay_sdk import Interface, Dynamic as D

import json
import boto3

def collect_instances(regions, access_key, secret_access_key):
    response = []
    for region in regions:
      # Create a client connection
        ec2 = boto3.resource('ec2',
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_access_key,
            region_name=region
        )      
        # Get the EC2 Instances
        for instance in ec2.instances.all():
            owner = None
            exp_date = None
            prefix = None
            cname = None
            for tag in instance.tags:
                if tag['Key'] == 'expiration_date':
                    exp_date = tag['Value']
                elif tag['Key'] == 'owner':
                    owner = tag['Value']
                elif tag['Key'] == 'event_id':
                    prefix = tag['Value']
                elif tag['Key'] == 'cname':
                    cname = tag['Value']
            # Skips checking if prefix is missing (currently just NOMAD servers)
            if prefix is not None:
                response.append({
                    'id': instance.id,
                    'owner': owner,
                    'exp_date': exp_date,
                    'prefix': prefix,
                    'cname': cname,
                    #'az': az
                })
    return response

def get_status(exp_date):
    # We will return the state of a single sample instance, healthy, expiring or expired.
    # HEALTHY (>48 hours days left), EXPIRING (<48 hours left), EXPIRED (<0 hours left)
    response = None
    instance_date = datetime.strptime(exp_date, '%Y-%m-%d %H:%M:%S %z')
    current_date = instance_date - datetime.now(timezone.utc)
    if current_date <= timedelta(seconds=0):
        response = 'expired'
    elif current_date <= timedelta(days=2) and current_date > timedelta(seconds=0):
        response = 'expiring'
    else:
        response = 'healthy'
    return response

def generate_reaper_manifest(instances):
    # Generate a dict of projects (prefix -> owner)
    prefixes = {}
    # Add only unique entries
    for instance in instances:
        prefix = instance['prefix']
        # If prefix doesn't exist, create a stub record
        if prefix not in prefixes:
            prefixes.update(
                {
                    prefix: {
                        'owner': instance['owner'],
                        'exp_date': instance['exp_date'],
                        'status': get_status(instance['exp_date']),
                        'instances': [],
                        'cnames': []
                    }
                }
            )
        # Else/Afterwards populate the rest of the record
        prefixes[prefix]['instances'].append(instance['id'])
        prefixes[prefix]['cnames'].append(instance['cname'])
    return prefixes

def main():
    relay = Interface()
    regions = [
        "us-east-1",
        "us-west-2",
        "eu-west-2",
        "eu-central-1",
        "ap-southeast-1",
        "ap-southeast-2",
        "ap-northeast-1",
        "ap-south-1"
    ]
    access_key = relay.get(D.aws.connection.accessKeyID)
    secret_access_key = relay.get(D.aws.connection.secretAccessKey)
    instances=collect_instances(regions, access_key, secret_access_key)
    relay.outputs.set("data",json.dumps(generate_reaper_manifest(instances), default=str))

if __name__ == "__main__":
    main()