#!/usr/bin/env python

# coolnick

import argparse, json, sys

try:
    import SoftLayer
except ImportError:
    print('\n[CoOlNiCk] You need [SoftLayer] modules to run this script')
    sys.exit('Terminating the process...')


parser = argparse.ArgumentParser()
parser.add_argument('--instances', '-i', required = True,
                    help="[CoOlNiCk] Comma separated instance IDs within single quotation")
parser.add_argument("--debug", "-d", action="store", default=False,
                    help="[CoOlNiCk] Enable debug mode")
args = parser.parse_args()

instance_list = args.instances.split(',')

print ('List of instances to be cancelled - %s' % instance_list)

config_file = './softlayer_config.json'
config = json.loads(open(config_file, "r").read())
client = SoftLayer.Client(username=config['SoftLayer']['UserName'],
                          api_key=config['SoftLayer']['APIKey'])

def check_power_state(instance_list):
    for instance in instance_list:
        power_status=client['SoftLayer_Virtual_Guest'].getPowerState(id=instance)
        print power_status

vs_manager = SoftLayer.VSManager(client)


for instance in instance_list:
    cancel_result = False
    power_off_result = False
    while not cancel_result:
        print ('[INFO] Soft Power Off instance(ID:%s)...' % str(instance))
        while not power_off_result:
            try:
                power_off_result = client['SoftLayer_Virtual_Guest'].powerOffSoft(id=instance)
                print ('[DEBUG] Result for SoftPowerOff for instance(ID:%s) %s' % (str(instance), power_off_result))
            except SoftLayer.SoftLayerAPIError as e:
                print('[ERROR] FaultCode= %s, FaultString= %s' % (e.faultCode, e.faultString))
                if e.faultCode == "SoftLayer_Exception_ObjectNotFound":
                    print ('[DEBUG] Instance not found. Skipping the PowerOff request for the instance(%s)' % instance)
                    power_off_result = True
                    cancel_result = True
                else:
                    exit(1)

        print ('[INFO] Cancelling instance(ID:%s)...' % str(instance))
        while not cancel_result:
            try:
                cancel_result = client['SoftLayer_Virtual_Guest'].deleteObject(id=instance)
                #cancel_result = True
            except SoftLayer.SoftLayerAPIError as e:
                print('[ERROR] FaultCode= %s, FaultString= %s' % (e.faultCode, e.faultString))
                exit(1)
            print ('[DEBUG] Result for cancelling instance(ID:%s) is %s' % (str(instance), cancel_result))

    print ('>\n')






