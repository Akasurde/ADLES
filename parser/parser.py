#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import yaml


def main():
    """ For testing of the parser """

    # Reference: http://pyyaml.org/wiki/PyYAMLDocumentation
    filename = 'test_example.yaml'
    with open(filename, 'r') as f:
        try:
            doc = yaml.safe_load(f)  # Parses the YAML file and creates a python object with it's structure and contents
        except yaml.YAMLError as exc:
            print("Error parsing config file %s" % filename)
            if hasattr(exc, 'problem_mark'):
                mark = exc.problem_mark
                print("Error position: (%s:%s)" % (mark.line + 1, mark.column + 1))
            else:
                print("Error: ", exc)
            exit()  # If there was an error, then there ain't gonna be any markup, so we exit

    print(doc["name"])


if __name__ == '__main__':
    main()
