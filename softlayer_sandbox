#!/usr/bin/env python

# coolnick
# requires following in order for this script to work
#   + a configuration file called "softlayer_config.json" file under the same directory
#   + a post provision script file accessible via internet

import sys, time, os, json, argparse

try:
    import SoftLayer
except ImportError:
    print('\n[CoOlNiCk] You need [SoftLayer] modules to run this script')
    sys.exit('Terminating the process...')

config_file = './softlayer_config.json'

parser = argparse.ArgumentParser()
parser.add_argument("--unique_id", "-u", action="store", default=False,
                    help="[CoOlNiCk] Unique ID for this demo")
args = parser.parse_args()

epoch_time=time.time()
unique_id = str(int(epoch_time))
current_time=time.strftime("%m%d-%H%M%S", time.gmtime(epoch_time))

current_directory=os.path.dirname(os.path.abspath(__file__))
log_directory=current_directory+'/log/'
if not os.path.exists(log_directory):
    os.mkdir(log_directory)

if args.unique_id != False:
    unique_id = args.unique_id

config = json.loads(open(config_file, "r").read())
client = SoftLayer.Client(username=config['SoftLayer']['UserName'],
                          api_key=config['SoftLayer']['APIKey'])

# print client['Account'].getObject()['officePhone']

data_center = config['SoftLayer']['Environments']['DataCenter']
domain_name = config['SoftLayer']['Environments']['Domain']
linux_instance = config['SoftLayer']['Environments']['Linux']

created_instances = []

def create_cleanup_command():
    print('\n[INFO] Please use following command to cancel all instances created using this script.')
    print('\t./cleanup.py --instances=\'%s\'\n' % (','.join(map(str, created_instances))))

def process_exceptions(inst):
    create_cleanup_command()
    sys.exit('[ERROR] Terminating the process. (%s)' % inst)

vs_manager = SoftLayer.VSManager(client)

# create linux instances
counter = 1
while counter <= linux_instance['NumberOfServer']:
    print ('[INFO] Creating %s-%s%d...' % (unique_id, linux_instance['HostNamePrefix'], counter))
    try:
        instance = vs_manager.create_instance(
            hostname = unique_id + "-" + linux_instance['HostNamePrefix'] + str(counter),
            domain = domain_name,
            cpus = linux_instance['CPUs'],
            memory = linux_instance['Memory'],
            hourly = linux_instance['HourlyBilling'],
            os_code = linux_instance['OSCode'],
            local_disk = linux_instance['LocalDisk'],
            post_uri = linux_instance['PostProvisionScript'],
            ssh_keys = linux_instance['SSHKeys'],
            datacenter = data_center
        )
    except (KeyboardInterrupt, Exception) as inst:
        process_exceptions(inst)

    counter += 1
    print ('[INFO] Created instance(HostName: %s, InstanceID: %s)' % (instance['hostname'], str(instance['id'])))
    created_instances.append(str(instance['id']))
    print ('\t %s' % instance)
    print ('>\n')

print ('[DEBUG] List of instances(IDs) created - %s' % created_instances)
print ('>\n')

create_cleanup_command()
print ('#### DONE ####')
