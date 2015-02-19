# softlayer_sandbox
Create (and remove) cloud instances on SoftLayer via Python Script

You will need to edit the softlayer_config.json file as following.
  + UserName: Your SoftLayer login ID
  + APIKey: Your SoftLayer APIKey
  + DataCenter: SoftLayer datacenter you want to use.  
  + Domain: Domain name to use.
  + NumberOfServer: Number of server(s) you want to spin up
  + CPUs: Number of CPU(s) to use for the server
  + Memory: Amount of memory to have
  + OSCode: OS to use
  + HostNamePrefix: Prefix to be used when creating hostname for the server(s)
  + SSHKeys: ID of SSH key to be used
  + HourlyBilling: True if you want the server to be billed for hourly
  + LocalDisk: True if you want to use local disk
  + PostProvisionScript: URL of script that will run after the server has been provisioned
