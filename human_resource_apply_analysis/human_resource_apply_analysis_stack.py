from aws_cdk import (
    Duration,
    Stack,
    aws_sqs as sqs,
    aws_lambda_event_sources as event_sources
)
from constructs import Construct
import aws_cdk.aws_lambda_python_alpha as python
import aws_cdk.aws_lambda as lambda_
from aws_cdk.aws_lambda import Runtime
from aws_cdk.aws_lambda_python_alpha import PythonFunction

class HumanResourceApplyAnalysisStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

       # Importar a fila SQS existente pelo ARN
        huma_resource_apply_queue = sqs.Queue.from_queue_arn(self, "human-resource-job-apply-queue",
            queue_arn="arn:aws:sqs:us-east-2:468125870510:Human-Resource-Job-Apply"
        )
        
        # Importar a fila SQS existente pelo ARN
        huma_resource_apply_queue_dlq = sqs.Queue.from_queue_arn(self, "human-resource-job-apply-queue-dlq",
            queue_arn="arn:aws:sqs:us-east-2:468125870510:Human-Resource-Job-Apply-DLQ"
        )

        analysis_application_lambda = PythonFunction(
            self, "Applicationanalysisjobapply",
            function_name = "Application-Analysis-Job-Apply",
            description ="Lambda responsável por analinar dados de candidatos a vagas de emprego e gerar uma opinião crítica sobre o currículo",
            entry="src/",
            architecture=lambda_.Architecture.X86_64,
            index="human_resource_apply_analysis_lambda.py",
            handler="lambda_handler",
            runtime=Runtime.PYTHON_3_12,
            timeout=Duration.seconds(120),
             bundling=python.BundlingOptions(
        # Garante que as dependências do requirements.txt sejam instaladas
        command=[
            "bash", "-c",
            "pip install -r requirements.txt -t /asset-output && cp -au . /asset-output"
        ],
        asset_excludes=[".venv", "__pycache__", "*.pyc"],
        install_dependencies=True,
        output_type=python.BundlingOutput.ARCHIVED,
    )
        )

        huma_resource_apply_queue.grant_consume_messages(analysis_application_lambda)

        analysis_application_lambda.add_event_source(
            event_sources.SqsEventSource(huma_resource_apply_queue)
        )
