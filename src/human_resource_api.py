import json
import requests

API_URL = "https://ypjkbbt6hgjcoi46mdpv5hkjzi0ttivo.lambda-url.us-east-2.on.aws"


def get_file_url(job_id, file_id):
    
    response = requests.get(f"{API_URL}/api/v1/document/{job_id}?documentId={file_id}", verify=False)
    response.raise_for_status()
    return response.json()

def get_job_by_id(job_id):
    
    response = requests.get(f"{API_URL}/api/v1/job/{job_id}", verify=False)
    response.raise_for_status()
    return response.json()


def create_job_analysis(source_data, opnion_data, job_id):
    
    # Mapeando os dados para o formato da API
    api_payload = {
        "name": source_data["nome"],
        "document": "09986134102",  # Sem informação fornecida
        "birthday": source_data["data_nascimento"] or "",
        "gender": source_data["genero"] or "",
        "civilStatus": source_data["estado_civil"] or "",
        "nationality": source_data["nacionalidade"] or "",
        "description": source_data["descricao"],
        "location": source_data["endereco"],
        "fileUrl": "",  # Sem informação fornecida
        "skills": source_data["habilidades"],
        "experiences": [
            {
                "position": exp["cargo"],
                "company": exp["empresa"],
                "period": exp["periodo"]
            } for exp in source_data["experiencias"]
        ],
        "education": [
            {
                "course": edu["curso"],
                "institute": edu["instituicao"],
                "level": "",  # Sem informação sobre nível
                "location": "",  # Sem informação sobre localização
                "period": edu["ano"]
            } for edu in source_data["formacao_academica"]
        ],
        "languages": [],  # Nenhum idioma informado
        "emails": source_data["email"],
        "phoneNumbers": source_data["telefone"],
        "courses": source_data["cursos"] or [],
        "score": opnion_data["score"],
        "alignmentPoints": opnion_data["pontos_alinhamento"],
        "misalignmentPoints": opnion_data["pontos_desalinhamento"],
        "pointsOfAttention": opnion_data["pontos_atencao"],
        "summary": opnion_data["sumario_executivo"]
    }

    headers = {"Content-Type": "application/json"}

    # Fazendo a requisição POST
    response = requests.post(f"{API_URL}/api/v1/analysis/{job_id}/create", data=json.dumps(api_payload), headers=headers, verify=False)
    return response.json()