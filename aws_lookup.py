#!/usr/bin/env python
from ansible.module_utils.basic import *
import aws_lib

def main():
    module = AnsibleModule(
            argument_spec = dict(
                name = dict(required = True, default = None),
                ),
            supports_check_mode = True
            )
    vpc_dict = aws_lib.AWSLookup().get_vpc_description(module.params['name'])
    module.exit_json(changed = False, ansible_facts = vpc_dict)

main()
