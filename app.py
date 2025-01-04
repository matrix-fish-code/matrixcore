from flask import Flask, request, jsonify, render_template
import openai
import boto3
import os
import json

# Inicialize a aplicação Flask
app = Flask(__name__)

# Configurações de API - Certifique-se de que as variáveis de ambiente estão configuradas corretamente
openai.api_key = os.getenv("OPENAI_API_KEY")

# Configurações S3
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_REGION = 'eu-west-2'
S3_BUCKET_NAME = 'matrix.fish'

# Inicializa o cliente S3
s3_client = boto3.client(
    's3',
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name=AWS_REGION
)


# Função para aplicar as regras ao prompt
def apply_rules_to_prompt(prompt):
    # Carregar as regras do S3
    rules = []
    try:
        # Lista de arquivos de regras
        for i in range(1, 8):  # 7 regras
            rule_key = f'rules/rule_{i}.json'
            rule_object = s3_client.get_object(Bucket=S3_BUCKET_NAME, Key=rule_key)
            rule_data = json.loads(rule_object['Body'].read().decode('utf-8'))

            # Verifique se a chave 'rule' está presente no arquivo JSON
            if 'rule' in rule_data:
                rules.append(rule_data['rule'])  # Adiciona a regra à lista de regras
            else:
                print(f"Erro: A chave 'rule' não foi encontrada em {rule_key}")
                return prompt  # Se não encontrar a chave 'rule', retorna o prompt sem alterações

    except Exception as e:
        print(f"Erro ao carregar regras do S3: {str(e)}")
        return prompt  # Se falhar ao carregar regras, retorna o prompt original

    # Modificar o prompt com as regras aplicadas de forma mais clara
    applied_prompt = f"Eduardo está no sistema Escudo Familiar, um sistema de controle rigoroso e total. {prompt} "
    
    for rule in rules:
        applied_prompt += f"{rule} "

    applied_prompt += "Com base nas regras, responda ao seguinte contexto."

    return applied_prompt


# Rota para a página principal (home)
@app.route('/')
def home():
    # Renderiza a página index.html
    return render_template('index.html')

# Rota para interação com a API de chat
@app.route('/chat', methods=['POST'])
def chat():
    # Obtém o prompt enviado pelo frontend (via POST)
    user_input = request.json.get('message')

    if not user_input:
        return jsonify({"error": "No input provided"}), 400

    try:
        print(f"Recebido prompt: {user_input}")  # Debugging: mostrar o que foi enviado

        # Aplica as regras antes de processar a resposta
        applied_rules = apply_rules_to_prompt(user_input)
        print(f"Prompt modificado com regras: {applied_rules}")  # Debugging: mostrar o prompt com as regras

        # Gera uma resposta usando a API da OpenAI (com o endpoint correto para chat models)
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # Certifique-se de que o modelo está correto
            messages=[{"role": "system", "content": "Você é uma entidade digital que ajuda com informações."},
                      {"role": "user", "content": applied_rules}],
            max_tokens=150
        )

        # Exibe a resposta completa da OpenAI para depuração
        print("OpenAI Response:", response)

        # Extrai a resposta da API
        ai_response = response.choices[0].message['content'].strip()

        print("AI Response:", ai_response)  # Debugging: mostrar a resposta gerada

        # Se a resposta não estiver vazia, a envia para o frontend
        if ai_response:
            return jsonify({"response": ai_response}), 200
        else:
            return jsonify({"error": "No response from OpenAI"}), 500

    except Exception as e:
        print(f"Erro: {str(e)}")  # Debugging: mostrar o erro real
        return jsonify({"error": str(e)}), 500

# Iniciar o servidor Flask
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

