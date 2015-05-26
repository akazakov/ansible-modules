#!/usr/bin/env python
from ansible.module_utils.basic import *
def main():
    module = AnsibleModule(
            argument_spec = dict(
                name = dict(required = True, default = None),
                ),
            supports_check_mode = True
            )
    args = "aws ec2 describe-vpcs --filters Name=tag:Name,Values=%s --query 'Vpcs[0]'" % module.params['name']
    rc, stdout, stderr = module.run_command(args, check_rc = True)
    vpcs_dict = {}
    vpcs_dict[module.params['name']] = stdout
    module.exit_json(
            changed = False,
            rc = rc,
            ansible_facts = dict(vpcs = vpcs_dict)
            )

main()
