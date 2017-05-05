List of tasks and TODOs for ADLES.
These range from minor tweaks, fixes, and improvements to major tasks and feature additions.


# Code

## Main Application
### Parser
* Make the parser a class to enable passing of state between methods
* Add type checking to _checker()
* Check if networks, services, groups, and resources are properly configured and matched.
* Verify group existance

### Utils
* Add Splunk logging handler to setup_logging() (https://github.com/zach-taylor/splunk_handler)

## Interface
* Subprocess the API calls by the Interface to its composite interfaces (e.g vSphere, Docker, etc).
That way they can run independantly and improve usage of network resources.
* Support multiple VsphereInterface instances (e.g for remote labs)
* Fix _instances_handler() workaround for AD-groups once they're implemented.
* Is method of loading login information for platform secure?

### VsphereInterface
* Apply group permissions
* Apply master-group permissions
* _create_service(): Validate the configuration of an existing service template to a reasonable degree
* Implement configuration of "network-interface" for services in the "services" top-level section
* _get_net(): could use this to do network lookups on the server as well
* cleanup_masters(): finish implementing, look at getorphanedvms in pyvmomi-community-samples for how to do this
* cleanup_environment(): implement, ensure master-folder is skipped
* Use Network folders to aid in network cleanup for both phases
* init(): Better vSwitch default
* Finish implementing hosts (since there's self.host and self.hosts currently)
* Deal with potential naming conflicts in self.masters cache of Master instances
* Make "template" and other platform identifiers global keywords per-interface

## Vsphere
* Evaluate using WaitForTask from pyVim in pyvmomi instead of wait_for_task() in vsphere_utils
* Another possible method: (https://github.com/vmware/pyvmomi-tools/blob/master/pyvmomi_tools/extensions/task.py)
* Profile performance of current task waiting method
* Multi-thread or multi-process task waiting

### VM
* Implement get_all_snapshots_info()
* Configure guest IP address if statically assigned for add_nic()
* execute_program(): listprocesses/terminate process in guest, make helper func for guest authentication

### Host
* Use this class elsewhere in code
* Implement get_info() to get host information much like VM's get_info()
* Add edit_vswitch()
* Add edit_portgroup()


## Scripts

# Additions

## Specs
* Add network folder(s) to vsphere infrastructrure specification

## Examples


# Features

