from datetime import datetime, timedelta, timezone

import json
import boto3

class Collector:
    def __init__(self):
        self.regions = json.load(open('regions.json', 'r'))
        self.instances=self.collect_instances()

    def collect_instances(self):
        response = []
        for region in self.regions:
          # Create a client connection
            ec2 = boto3.resource('ec2', region_name=region)      
            # Get the EC2 Instances
            for instance in ec2.instances.all():
                owner = None
                exp_date = None
                prefix = None
                cname = None
                # AZ breaks if none available
                az = [i.subnet.availability_zone for i in instance.network_interfaces][0]
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

    def scan_route_53(self):
        # response = []
        r53 = boto3.client('route53')
        # Get the Route 53 DNS records
        zone_id = [zone['Id'] for zone in r53.list_hosted_zones_by_name()['HostedZones'] if zone['Name'] == 'se.automationdemos.com'][0]
        dns_records = [item for item in r53.list_resource_record_sets(HostedZoneId=zone_id)['ResourceRecordSets'] if item['Type'] == 'CNAME']
        return dns_records

    def get_status(self, exp_date):
        # We will return the state of a single sample instance, healthy, expiring or expired.
        # HEALTHY (>48 hours days left), EXPIRING (<48 hours left), EXPIRED (<0 hours left)
        response = None
        instance_date = datetime.strptime(exp_date, '%Y-%m-%d %H:%M:%S %z')
        current_date = instance_date - datetime.now(timezone.utc)
        if current_date <= timedelta(days=0):
            response = 'expired'
        elif current_date <= timedelta(days=2):
            response = 'expiring'
        else:
            response = 'healthy'
        return response

    def generate_reaper_manifest(self):
        # Generate a dict of projects (prefix -> owner)
        prefixes = {}
        # Add only unique entries
        for instance in self.instances:
            prefix = instance['prefix']
            # If prefix doesn't exist, create a stub record
            if prefix not in prefixes:
                prefixes.update(
                    {
                        prefix: {
                            'owner': instance['owner'],
                            'exp_date': instance['exp_date'],
                            'status': self.get_status(instance['exp_date']),
                            #'az': instance['az'],
                            'instances': [],
                            'cnames': []
                        }
                    }
                )
            # Else/Afterwards populate the rest of the record
            prefixes[prefix]['instances'].append(instance['id'])
            prefixes[prefix]['cnames'].append(instance['cname'])
        return prefixes

x = Collector()
environments = x.generate_reaper_manifest()
print(json.dumps(environments, default=str))
