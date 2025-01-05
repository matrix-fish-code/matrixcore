from flask import Flask, request, jsonify, render_template
import openai
import os
import json
from config import openai_api_key, s3_client, S3_BUCKET_NAME
from utils import save_interaction_to_s3

# Configurar a aplicação Flask
app = Flask(__name__)

# Definir chave API do OpenAI
openai.api_key = openai_api_key

# Página inicial do Flask (exibe o formulário)
@app.route('/')
def index():
    return render_template('index.html')

# Rota para interação com a OpenAI
@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_input = data.get('message')

    # Enviar o prompt para a OpenAI
    response = get_openai_response(user_input)

    # Salvar a interação no S3
    save_interaction_to_s3(user_input, response)

    return jsonify({"response": response})

def get_openai_response(prompt):
    response = openai.Completion.create(
        engine="gpt-3.5-turbo",  # Escolher o modelo desejado
        prompt=prompt,
        max_tokens=150
    )
    return response.choices[0].text.strip()

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)  # Acessível externamente
