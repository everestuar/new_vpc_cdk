from aws_cdk import core
import aws_cdk.aws_ec2 as ec2

class VpcStack(core.NestedStack):

    def __init__(self, scope: core.Construct, id: str, parms=dict, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Nat Instance
        if(parms["nat_provider"] == 'GATEWAY'):
            nat_provider = ec2.NatProvider.gateway()
        else:
            nat_provider = ec2.NatProvider.instance(
                instance_type=ec2.InstanceType("t3a.micro"))

        self.vpc = ec2.Vpc(self, "apache-vpc",
                           max_azs=2,
                           enable_dns_hostnames=True,
                           enable_dns_support=True,
                           cidr="172.17.0.0/16",
                           # configuration will create 3 groups in 2 AZs = 6 subnets.
                           subnet_configuration=[ec2.SubnetConfiguration(
                               subnet_type=ec2.SubnetType.PUBLIC,
                               name="Public",
                               cidr_mask=22
                           ), ec2.SubnetConfiguration(
                               subnet_type=ec2.SubnetType.PRIVATE,
                               name="Private",
                               cidr_mask=22
                           ), ec2.SubnetConfiguration(
                               subnet_type=ec2.SubnetType.ISOLATED,
                               name="DB",
                               cidr_mask=22
                           )
                           ],
                           nat_gateway_provider=nat_provider,
                           nat_gateways=parms["nat_count"],
                           )

        core.CfnOutput(self, "Output", value=self.vpc.vpc_id)


