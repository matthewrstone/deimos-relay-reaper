import urllib3
from collector import Collector
#urllib3.disable_warnings()
#expired = [z for z in x.generate_reaper_manifest() if environments[z]['status'] == 'expired']
#expiring = [z for z in x.generate_reaper_manifest() if environments[z]['status'] == 'expiring']


# #Notify Slack for expiring nodes
# for environment in environments:
#     if environments[environment]['status'] == 'expiring':
#         # Had to pop the ID back in to send to Relay. Not ideal.
#         environments[environment].update({'prefix': environment})
#         time_left = datetime.strptime(environments[environment]['exp_date'], '%Y-%m-%d %H:%M:%S %z') - datetime.now(timezone.utc)
#         url = get_webhook_from_relay
#         headers = {'Content-Type': 'application/json'}
#         body = {
#                    'prefix': environment,
#                    'time_left': time_left,
#                    'owner': environments[environment]['owner']
#                }
#         requests.post(url=url, headers=headers, data=json.dumps(body, default=str), verify=False)
#     if environments[environment]['status'] == 'expired':
#         print('I WILL PURGE {}'.format(environment))
# #print(json.dumps(x.generate_reaper_manifest(), indent=2, default=str))
# #print(json.dumps(x.collect_instances(), indent=2, default=str))