#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging


class Spec:
    def __init__(self, metadata):
        """
        :param metadata: Dict containing metadata for the specification
        """
        self.metadata = metadata

        # Load infrastructure information
        if metadata["infrastructure-config-file"]:
            import automation.parser as parser
            self.infra = parser.parse_file(metadata["infrastructure-config-file"])
        else:
            logging.error("No infrastructure configuration file specified!")
            return

        # Load login information
        from json import load
        with open("logins.json", "r") as login_file:
            logins = load(fp=login_file)

        # Select an API to use
        if self.infra["platform"] == "vmware vsphere":
            from automation.vsphere.vsphere import vSphere
            self.api = vSphere(datacenter=self.infra["datacenter"],
                               username=logins["user"],
                               password=logins["pass"],
                               hostname=logins["host"],
                               port=int(logins["port"]),
                               datastore=self.infra["datastore"])
        else:
            logging.error("Invalid platform {}".format(self.infra.platform))
            return

    def main(self):
        pass


if __name__ == '__main__':
    pass  # RUN TESTS
