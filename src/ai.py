import re
from langchain_groq import ChatGroq

api_key = "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"

class GroqClient:
    def __init__(self, model_id="llama-3.3-70b-versatile"):
        # Inicializar o modelo de linguagem com o ID especificado
        self.model_id = model_id
        self.client = ChatGroq(model=model_id, api_key=api_key)

    def generate_response(self, prompt):
        # Enviar o prompt ao modelo e obter a resposta
        response = self.client.invoke(prompt)
        return response.content

    def resume_cv(self, cv):
        # Criar o prompt para gerar um resumo do currículo em Markdown
        prompt = f'''
            **Solicitação de Resumo de Currículo em Markdown:**
            
            # Curriculo do candidato para resumir:
            
            {cv}

            Por favor, gere um resumo do currículo fornecido, formatado em Markdown, seguindo rigorosamente o modelo abaixo. **Não adicione seções extras, tabelas ou qualquer outro tipo de formatação diferente da especificada.** Preencha cada seção com as informações relevantes, garantindo que o resumo seja preciso e focado. Nos idiomas tenha atenção porque uma coisa é idioma de programação e outra é idioma de comunicação.

            **Formato de Output Esperado:**

            ```markdown
            ## Nome Completo
            nome_completo aqui

            ## Experiência
            experiencia aqui

            ## Habilidades 
            habilidades aqui

            ## Educação 
            educacao aqui

            ## Idiomas 
            idiomas aqui

            '''

        # Gerar a resposta usando o modelo de linguagem
        result_raw = self.generate_response(prompt=prompt)
        
        # Tentar extrair o conteúdo após o marcador ```markdown
        try:
            result = result_raw.split('```markdown')[1]
        except:
            # Se não conseguir, retornar a resposta bruta
            result = result_raw
        return result

    def generate_score(self, cv, job, max_attempts=10):
        # Criar o prompt para calcular a pontuação do currículo com base na vaga
        prompt = f'''
            **Objetivo:** Avaliar um currículo com base em uma vaga específica e calcular a pontuação final. A nota máxima é 10.0.

            **Instruções:**

            1. **Experiência (Peso: 30%)**: Avalie a relevância da experiência em relação à vaga.
            2. **Habilidades Técnicas (Peso: 25%)**: Verifique o alinhamento das habilidades técnicas com os requisitos da vaga.
            3. **Educação (Peso: 10%)**: Avalie a relevância da formação acadêmica para a vaga.
            4. **Idiomas (Peso: 10%)**: Avalie os idiomas e sua proficiência em relação à vaga.
            5. **Pontos Fortes (Peso: 15%)**: Avalie a relevância dos pontos fortes para a vaga.
            6. **Pontos Fracos (Desconto de até 10%)**: Avalie a gravidade dos pontos fracos em relação à vaga.
            
            Curriculo do candidato
            
            {cv}
            
            Vaga que o candidato está se candidatando
            
            {job}

            **Output Esperado:**
            ```
            Pontuação Final: x.x
            ```
            
            **Atenção:** Seja rigoroso ao atribuir as notas. A nota máxima é 10.0, e o output deve conter apenas "Pontuação Final: x.x".
        
        '''
        
        # Tentar gerar a pontuação em múltiplas tentativas, caso necessário
        for attempt in range(max_attempts):
            # Gerar a resposta usando o modelo de linguagem
            result_raw = self.generate_response(prompt=prompt)
            
            # Extrair a pontuação da resposta gerada
            score = self.extract_score_from_result(result_raw)
        
            # Se a pontuação foi extraída com sucesso, retornar a pontuação
            if score is not None:
                return score
            
            # Se falhar, exibir mensagem de erro e tentar novamente
            print(f"Tentativa {attempt + 1} falhou. Tentando novamente...")
        
        # Lançar um erro se não conseguir gerar a pontuação após várias tentativas
        raise ValueError("Não foi possível gerar a pontuação após várias tentativas.")
    
    def extract_score_from_result(self, result_raw):
        """Extrair a pontuação final da resposta gerada."""
        # Definir o padrão de regex para buscar a pontuação na resposta
        pattern = r"(?i)Pontuação Final[:\s]*([\d,.]+(?:/\d{1,2})?)"
        
        # Procurar pela pontuação na resposta
        match = re.search(pattern, result_raw)
        
        if match:
            # Se encontrado, extrair o valor da pontuação
            score_str = match.group(1)
            if '/' in score_str:
                score_str = score_str.split('/')[0]
            
            # Retornar a pontuação como um número float
            return float(score_str.replace(',', '.'))
        
        # Retornar None se não encontrar a pontuação
        return None

    def generate_opnion(self, cv, job):
        # Criar o prompt para gerar uma opinião crítica sobre o currículo
        prompt = f'''
        Tarefa:
        Gere uma análise detalhada e estruturada do currículo em relação à vaga, formatada em JSON, com os seguintes campos:

        sumario_executivo: Resumo geral da compatibilidade do candidato.
        score: Um número decimal de 0 a 10 indicando o nível de compatibilidade, sendo 5 equivalente a 50% de compatibilidade e 10 um alinhamento perfeito. A pontuação deve ser extremamente rigorosa.
        pontos_alinhamento: Texto único destacando as áreas onde o candidato atende aos requisitos da vaga.
        pontos_desalinhamento: Texto único destacando as áreas onde o candidato não atende aos requisitos da vaga.
        pontos_atencao: Texto único com observações críticas sobre o perfil do candidato.
        Formato esperado: Retorne somente um JSON válido, sem explicações adicionais.

        Currículo Original:
        
        {cv}

        Descrição da Vaga:
        {job}
        '''
        # Gerar a resposta usando o modelo de linguagem
        result_raw = self.generate_response(prompt=prompt)
        result = result_raw
        return result
      
    def extract_cv_data(self, cv):

        # Extrair os dados mais relevantes do currículo e retornar em um formato estruturado de json

        prompt = f'''
            
Você é um especialista em processamento de texto e análise de currículos. Sua tarefa é analisar o currículo fornecido e extrair as seguintes informações em um formato JSON estruturado. Se uma informação não for encontrada no texto, defina o valor como `null`. Retorne **apenas** o JSON, sem explicações adicionais.

### **Campos a serem extraídos**:
- **nome**: Nome completo do candidato.
- **data_nascimento**: Data de nascimento do candidato.
- **nacionalidade**: Nacionalidade do candidato.
- **estado_civil**: Estado civil do candidato.
- **genero**: Gênero do candidato.
- **email**: Lista de e-mails encontrados.
- **telefone**: Lista de números de telefone encontrados.
- **endereco**: Endereço do candidato.
- **descricao**: Um resumo ou descrição profissional do candidato.
- **habilidades**: Lista de habilidades técnicas e interpessoais mencionadas.
- **experiencias**: Lista de experiências profissionais, incluindo cargo, empresa e período.
- **cursos**: Lista de cursos realizados.
- **formacao_academica**: Lista de formações acadêmicas, incluindo instituição, curso e ano.
- **idiomas**: Lista de idiomas falados e seus níveis de proficiência (básico, intermediário, avançado ou fluente).
- **redes_sociais**: Lista de redes sociais profissionais do candidato, so LinkedIn, ou GitHub. Se houver um link, incluir o link; caso contrário, incluir apenas o nome ou arroba.

---

### **Atenção**:
- **Formate o JSON corretamente**.
- **Não adicione informações extras**.
- **Se uma informação não for encontrada, defina o valor como `null`**.

### **Currículo a ser processado**:

            {cv}
        
        '''
        # Gerar a resposta usando o modelo de linguagem
        result_raw = self.generate_response(prompt=prompt)
        result = result_raw
        return result
