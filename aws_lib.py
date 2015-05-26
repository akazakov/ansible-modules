#!/usr/bin/env python
from boto import vpc
from boto import ec2


class AWSLookup:
    """ A Class to do simple lookups in AWS """

    def __init__(self):
        self.vpc_conn = vpc.VPCConnection()
        self.ec2_conn = ec2.EC2Connection()
        
    def __get_vpc_by_name(self, vpcname):
        filters = {}
        if (vpcname != 'all'):
            filters = {'tag:Name' : vpcname}
        vpcs = self.vpc_conn.get_all_vpcs(filters=filters)
        if len(vpcs) != 1 and vpcname != 'all':
            raise Exception("Expected 1 VPC Defined with name '{0}' but found {1}".format(vpcname,len(vpcs)))
        return vpcs[0]

    def __convert_primitive_dict(self, aws_dict):
        primitive_dict = dict()
        for key,value in aws_dict.iteritems():
            if isinstance(value, unicode) or isinstance(value, bool) or isinstance(value, int):
                primitive_dict[key] = str(value)
            if isinstance(value, vpc.RegionInfo):
                primitive_dict[key] = value.name
            if isinstance(value, ec2.tag.TagSet):
                primitive_tags = dict()
                for tag_key, tag_value in value.iteritems():
                    primitive_tags[str(tag_key)] = str(tag_value)
                primitive_dict[key] = primitive_tags
        return primitive_dict

    def get_vpc_description(self, vpcname):
        vpc = self.__get_vpc_by_name(vpcname)
        subnets = self.vpc_conn.get_all_subnets(filters={'vpcId' : vpc.id})
        vpc_dict =  self.__convert_primitive_dict(vpc.__dict__)
        vpc_dict['name'] = vpcname
        vpc_dict['subnets'] = [self.__convert_primitive_dict(x.__dict__) for x in subnets]
        return vpc_dict

    def get_security_group(self, vpcname, groupname):
        vpc = self.__get_vpc_by_name(vpcname)
        security_groups = self.ec2_conn.get_all_security_groups(filters= {'vpc-id' : vpc.id, 'group-name' : groupname})
        if len(security_groups) > 1:
            raise Exception("Expected 0 or 1 Security groups for vpc {0} groupname {1} but found {3}".format(vpcname, groupname, len(security_groups)))

        return security_groups[0] if len(security_groups) == 1 else None

    def find_instance(self, vpcname, filters):
        vpc = self.__get_vpc_by_name(vpcname)
        filters['vpc-id'] = vpc.id
        return self.ec2_conn.get_only_instances(filters=filters)
        



