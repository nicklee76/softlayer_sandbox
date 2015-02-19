# softlayer_sandbox

This Python scripts will create (and/or remove) cloud instances on SoftLayer.

You will need to edit the softlayer_config.json file as following.
  + UserName: Your SoftLayer login ID. (For example, "JohnDoe")
  + APIKey: Your SoftLayer APIKey. (For example, "123mknoi290S789390430952")
  + DataCenter: SoftLayer datacenter you want to use.  (For example, "sjc01")
  + Domain: Domain name to use.  (For example, "acme_cloud.com")
  + NumberOfServer: Number of server(s) you want to spin up.  (For example, 2)
  + CPUs: Number of CPU(s) to use for the server.  (For example, 1)
  + Memory: Amount of memory to have.  (For example, 1024)
  + OSCode: OS to use.  (For example, "CENTOS_6_64")
  + HostNamePrefix: Prefix to be used when creating hostname for the server(s).  (For example, "ACME_WWW-")
  + SSHKeys: List of ID(s) of SSH key(s) to be used.  (For example, [12345, 23345])
  + HourlyBilling: True if you want the server to be billed for hourly. (For example, "True")
  + LocalDisk: True if you want to use local disk.  (For example, "True")
  + PostProvisionScript: URL of script that will run after the server has been provisioned.  (For example, "https://web_storage.acme_cloud.com/PostProvisionScript.sh")

### softlayer_sandbox.py
  + Creates cloud instances on SoftLayer.
  + It uses "PostProvisonScript" to perform required installations and configurations.  Refer to http://knowledgelayer.softlayer.com/procedure/add-provisioning-script for more information on PostProvisionScript.
  + After the script is completed it will provide complete command line to use to clean up (terminate) the instances created by this script. 

### cleanup.py
  + Cleans up (terminate) instances created by the "softlayer_sandbox.py" script.

