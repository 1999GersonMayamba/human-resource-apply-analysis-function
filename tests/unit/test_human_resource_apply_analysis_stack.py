import aws_cdk as core
import aws_cdk.assertions as assertions

from human_resource_apply_analysis.human_resource_apply_analysis_stack import HumanResourceApplyAnalysisStack

# example tests. To run these tests, uncomment this file along with the example
# resource in human_resource_apply_analysis/human_resource_apply_analysis_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = HumanResourceApplyAnalysisStack(app, "human-resource-apply-analysis")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
