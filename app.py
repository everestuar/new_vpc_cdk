#!/usr/bin/env python3
import os
# from aws_cdk import core as cdk
from aws_cdk import core
# from apache_new_vpc_cdk.apache_new_vpc_cdk_stack import ApacheNewVpcCdkStack
from stacks.vpc_stack import VpcStack

## START of Parameters Definition
parms = {}

parms["nat_provider"] = "GATEWAY"
parms["nat_count"] = 1

## END of Parameters Definition

env = core.Environment(account=os.environ.get("DEPLOY_ACCOUNT", os.environ["DEFAULT_ACCOUNT"]),
    region=os.environ.get("DEPLOY_REGION", os.environ["DEFAULT_REGION"]))

app = core.App()

main_stack = core.Stack(app, 'MainStack', env=env)
vpc_stack = VpcStack(main_stack, "Vpc", parms=parms)

app.synth()

