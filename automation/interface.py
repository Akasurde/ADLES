#!/usr/bin/env python3
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


class Interface:
    """ Generic interface used to uniformly interact with platform-specific interface implementations. """

    def __init__(self, spec):
        """ :param spec: Full specification """
        from sys import exit
        self.metadata = spec["metadata"]

        if not self.metadata["infrastructure-config-file"]:
            logging.error("No infrastructure configuration file specified!")
            exit("Unable to load Model: no infra conf file")

        # Load infrastructure information
        from automation.parser import parse_file
        # infrastructure = parse_file(metadata["infrastructure-config-file"])
        infrastructure = parse_file("vsphere.yaml")  # TODO: testing only, either make this a CMD arg or remove

        # Load login information
        from json import load
        try:
            logging.debug("Loading login information...")
            with open(infrastructure["login-file"], "r") as login_file:
                logins = load(fp=login_file)
        except Exception as e:
            logging.error("Could not open login file %s. Error: %s", infrastructure["login-file"], str(e))
            exit("Unable to load Model: couldn't open login file")

        # Select the Interface to use for the platform
        if infrastructure["platform"] == "vmware vsphere":
            from automation.vsphere_interface import VsphereInterface
            self.interface = VsphereInterface(infrastructure, logins, spec)  # Create interface
        else:
            logging.error("Invalid platform {}".format(infrastructure["platform"]))
            exit("Unable to load Model: Invalid Platform")

    def create_masters(self):
        """ Master creation phase """
        logging.info("Creating Master instances for %s", self.metadata["name"])
        self.interface.create_masters()

    def deploy_environment(self):
        """ Environment deployment phase """
        logging.info("Deploying environment for %s", self.metadata["name"])
        self.interface.deploy_environment()

    def cleanup_masters(self, network_cleanup=False):
        """
        Cleans up master instances
        :param network_cleanup: If networks should be cleaned up [default: False]
        """
        logging.info("Cleaning up Master instances for %s", self.metadata["name"])
        self.interface.cleanup_masters(network_cleanup=network_cleanup)

    def cleanup_environment(self, network_cleanup=False):
        """
        Cleans up a deployed environment
        :param network_cleanup: If networks should be cleaned up [default: False]
        """
        logging.info("Cleaning up environment for %s", self.metadata["name"])
        self.interface.cleanup_masters(network_cleanup=network_cleanup)

    # List of possible useful things
    #   open_console
    #   upload_file
    #   get_status    Status of the overall environment (what VMs are on/off/deploys, what phase, etc.)
