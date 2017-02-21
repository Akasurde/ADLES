# -*- coding: utf-8 -*-

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import logging

from automation.vsphere.vsphere import Vsphere
from automation.vsphere.network_utils import *
from automation.vsphere.vsphere_utils import *
from automation.vsphere.vm_utils import *


class VsphereInterface:
    """ Generic interface for the VMware vSphere platform """

    # Switches to tweak (these are global to ALL instances of this class)
    master_prefix = "(MASTER) "
    master_folder_name = "MASTER_FOLDERS"
    warn_threshold = 100            # Point at which to warn if many instances are being created

    def __init__(self, infrastructure, logins, spec):
        logging.debug("Initializing VsphereInterface...")
        self.spec = spec
        self.metadata = spec["metadata"]
        self.groups = spec["groups"]
        self.services = spec["services"]
        # TODO: how do resources fit in here? Ignoring for now...
        self.networks = spec["networks"]
        self.folders = spec["folders"]

        # Create the vSphere object to interact with
        self.server = Vsphere(datacenter=infrastructure["datacenter"],
                              username=logins["user"],
                              password=logins["pass"],
                              hostname=logins["host"],
                              port=int(logins["port"]),
                              datastore=infrastructure["datastore"])

        # Create root folder for the exercise
        server_root = "script_testing"  # TODO: put this in infra-spec, default to server root.vmFolder or whatever
        self.root_path = self.metadata["root-path"]
        self.root_name = self.metadata["name"]
        parent = traverse_path(self.server.get_folder(server_root), self.root_path)
        self.root_folder = self.server.create_folder(folder_name=self.root_name, create_in=parent)

    def create_masters(self):
        """ Master creation phase """

        # TODO: for the time being, just doing a flat "MASTER_FOLDERS" folder with all the masters, regardless of depth
        #   Will eventually do hierarchically based on folders and not just the services
        #   Will write a function to do this, so we can recursively descend for complex environments

        # Create master folder to hold base service instances
        master_folder = self.server.create_folder(folder_name=self.master_folder_name, create_in=self.root_folder)
        logging.info("Created master folder %s under folder %s", self.master_folder_name, self.root_folder.name)

        # Create portgroups for networks
        for net_type in self.networks:
            self._create_master_networks(net_type)

        # Create base service instances (Docker containers and compose will be implemented here)
        for service_name, service_config in self.services.items():
            if "template" in service_config:         # Virtual Machine template
                logging.info("Creating master for service %s from template %s",
                             service_name, service_config["template"])
                vm_name = self.master_prefix + service_name
                template = self.server.get_vm(service_config["template"])  # TODO: traverse path
                clone_vm(vm=template, folder=master_folder, name=vm_name,
                         clone_spec=self.server.generate_clone_spec())

                # Snapshot and configure base instance post-clone
                new_vm = self.server.get_vm(vm_name=vm_name)  # (TODO: traverse path)
                if not new_vm:
                    logging.error("Did not successfully clone VM %s", vm_name)
                    continue

                # TODO: add NICs to VMs and attach to portgroups
                # Check if number of networks in spec is same as what's on the VM
                # NOTE: management interfaces matter here!
                # TODO: distributed
                if len(service_config["networks"]) == len(list(new_vm.network)):
                    # TODO: put this in a function?
                    for net, i in zip(service_config["networks"], len(service_config["networks"])):
                        edit_nic(new_vm, nic_number=i, port_group=self.server.get_portgroup(net), summary=net)
                else:  # Create missing interfaces or remove excess
                    # TODO: add missing
                    # TODO: remove excess
                    pass

                if "note" in service_config:
                    set_note(vm=new_vm, note=service_config["note"])

                create_snapshot(new_vm, "post-clone", "Clean snapshot taken after cloning and configuration.")

        # Apply master-group permissions [default: group permissions]

    def _create_master_networks(self, net_type):
        host = self.server.get_host()
        host.configManager.networkSystem.RefreshNetworkSystem()  # Pick up any changes that might have occurred

        for name, config in self.networks[net_type].items():
            if "vlan" in config:
                vlan = config["vlan"]
            else:
                vlan = 0
            create_portgroup(name, host, config["vswitch"], vlan=vlan)

    def deploy_environment(self):
        """ Environment deployment phase """

        # Verify and convert to templates
        logging.info("Verifying masters and converting to templates...")
        for service_name, service_config in self.services.items():
            if "template" in service_config:
                vm = self.server.get_vm(self.master_prefix + service_name)  # TODO: traverse path
                if vm:  # Verify all masters exist
                    logging.debug("Verified master %s exists. Converting to template...", service_name)
                    convert_to_template(vm)  # Convert all masters to templates
                    logging.debug("Converted master %s to template. Verifying...", service_name)
                    if not is_template(vm):  # Verify converted successfully
                        logging.error("Master %s did not convert to template!", service_name)
                else:
                    logging.error("Could not find master %s", service_name)

        # NOTE: use fill_zeros when appending instance number!
        # Create folder to hold portgroups (for easy deletion later)
        # Create portgroup instances
        #   Create generic-networks
        #   Create base-networks

        # Clone instances (use function for numbering)(use prefix if specified)

    def cleanup_masters(self, network_cleanup=False):
        """ Cleans up any master instances"""

        # Get the folder to cleanup in
        master_folder = find_in_folder(self.root_folder, self.master_folder_name)
        logging.info("Found master folder %s under folder %s, proceeding with cleanup...",
                     master_folder.name, self.root_folder.name)

        # Recursively descend from master folder, destroying anything with the prefix

        # Cleanup networks (TODO: use network folders to aid in this, during creation phase)
        if network_cleanup:
            pass

    def cleanup_environment(self, network_cleanup=False):
        """ Cleans up a deployed environment """

        # Cleanup networks (TODO: use network folders to aid in this, during creation phase)
        if network_cleanup:
            pass
