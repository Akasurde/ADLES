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

"""Query information about a vSphere environment and objects within it.

Usage:
    vsphere_info.py [-v] [-f FILE]
    vsphere_info.py --version
    vsphere_info.py (-h | --help)

Options:
    -h, --help          Prints this page
    --version           Prints current version
    -f, --file FILE     Name of JSON file with server connection information
    -v, --verbose       Verbose output of whats going on

"""

import logging

from docopt import docopt

from adles.automation.utils import setup_logging, make_vsphere, warning
from adles.vsphere import *

__version__ = "0.3.0"

args = docopt(__doc__, version=__version__, help=True)
setup_logging(filename='vsphere_info.log', console_level=logging.DEBUG if args["--verbose"] else logging.INFO)

server = make_vsphere(args["--file"])
warning()

# List of possible useful things
#   open_console
#   upload_file
#   get_status    Status of the overall environment (what VMs are on/off/deploys, what phase, etc.)

thing_type = input("What type of thing do you want to get information on? (vm | datastore | vsphere) ")
thing_name = input("What is the name of the thing you want to get information on? ")
if thing_type == "vm":
    vm = server.get_vm(thing_name)
    vm_utils.print_vm_info(vm, print_uuids=True)
elif thing_type == "datastore":
    ds = server.get_datastore(thing_name)
    vsphere_utils.print_datastore_info(ds)
elif thing_type == "vsphere":
    logging.info("%s", str(server.content.about))
else:
    logging.info("Invalid type: ", thing_type)
