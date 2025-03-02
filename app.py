#!/usr/bin/env python3
import os

import aws_cdk as cdk

from human_resource_apply_analysis.human_resource_apply_analysis_stack import HumanResourceApplyAnalysisStack


app = cdk.App()
HumanResourceApplyAnalysisStack(app, "HumanResourceApplyAnalysisStack",
                                
    env=cdk.Environment(
        account=os.getenv('CDK_DEFAULT_ACCOUNT', '468125870510'),
        region=os.getenv('CDK_DEFAULT_REGION', 'us-east-2')
    )
    
    )

app.synth()
