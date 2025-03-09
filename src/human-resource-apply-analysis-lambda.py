import json
import re
import human_resource_api
import helper
from ai import GroqClient


def lambda_handler(event, context):
    
    print("Event received:", event)
    
    for record in event['Records']:
        data = json.loads(record['body'])
        analysis_application(data)

    return True

def analysis_application(data):
    
    print("Analysis a job application:", data)
    
    # Inicializar o cliente de IA para processar os currículos
    ai = GroqClient()
    fileName = data["fileName"]
    job = human_resource_api.get_job_by_id(data["jobId"])
    pdf_url = human_resource_api.get_file_url(job_id=job["data"]["id"], file_id=data["fileName"])
    pdf = helper.download_file(pdf_url)
    texto_curriculo = helper.extract_text_from_pdf(pdf)

    job_description = f''' Vaga: {job["data"]["title"]} {job["data"]["mainActivitie"]} {job["data"]["prerequisite"]} {job["data"]["differential"]}'''

    # Gerar uma opinião sobre o currículo com base na vaga de emprego
    opnion = ai.generate_opnion(texto_curriculo, job_description)

    # Remover a formatação de código (```)
    data = opnion.strip().replace("```", "").replace("json", "").strip()
    opnion_data = json.loads(data)

    # Obter os dados do CV
    cv_data = ai.extract_cv_data(texto_curriculo)

    # Converter string JSON para dicionário Python
    json_match = re.search(r'{.*}', cv_data, re.DOTALL)

    json_data = json_match.group(0)  # Extrai a string JSON
    source_data = json.loads(json_data)    # Converte a string JSON para um dicionário Python

    response = human_resource_api.create_job_analysis(source_data, opnion_data, job["data"]["id"], fileName)
    print(response)
    
    print("Analysis a job application completed.")
