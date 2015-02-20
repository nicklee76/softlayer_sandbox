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

parser = argparse.ArgumentParser()
parser.add_argument("--unique_id", "-u", action="store", default=False,
                    help="[CoOlNiCk] Unique ID for this demo")
parser.add_argument("--debug", "-d", action="store_true", default=False,
                    help="[CoOlNiCk] Enable debug mode")
parser.add_argument("--input", "-i", action="store", default="softlayer_config.json",
                    help="[CoOlNiCk] Name of the input file.  Default is [cp-config.json]")
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

config = json.loads(open(args.input, "r").read())
client = SoftLayer.Client(username=config['SoftLayer']['UserName'],
                          api_key=config['SoftLayer']['APIKey'])

created_instances = []

def create_cleanup_command():
    print('\n[INFO] Please use following command to cancel all instances created using this script.')
    print('\t./softlayer_cleanup.py --instances=\'%s\'\n' % (','.join(map(str, created_instances))))


def process_exceptions(inst):
    create_cleanup_command()
    sys.exit('[ERROR] Terminating the process. (%s)' % inst)


def create_instance(instance):
    counter = 1
    while counter <= instance['NumberOfServer']:
        print ('[INFO] Creating %s-%s%d...' % (unique_id, instance['HostNamePrefix'], counter))
        try:
            instance_created = vs_manager.create_instance(
                hostname = unique_id + "-" + instance['HostNamePrefix'] + str(counter),
                domain = instance['Domain'],
                cpus = instance['CPUs'],
                memory = instance['Memory'],
                hourly = instance['HourlyBilling'],
                os_code = instance['OSCode'],
                local_disk = instance['LocalDisk'],
                post_uri = instance['PostProvisionScript'],
                ssh_keys = instance['SSHKeys'],
                datacenter = instance['DataCenter']
            )
        except (KeyboardInterrupt, Exception) as inst:
            process_exceptions(inst)

        print ('[INFO] Created instance(HostName: %s, InstanceID: %s)'
               % (instance_created['hostname'], str(instance_created['id'])))
        created_instances.append(str(instance_created['id']))
        print ('>\n')
        counter += 1

vs_manager = SoftLayer.VSManager(client)

for instance in config['SoftLayer']['Environments']['Instances']:
    create_instance(instance)

if args.debug:
    print ('[DEBUG] List of instances(IDs) created - %s' % created_instances)
    print ('>\n')

create_cleanup_command()

print ('#### DONE ####')
