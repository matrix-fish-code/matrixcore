import openai

# Defina sua chave de API da OpenAI
openai.api_key = 'your_openai_api_key'  # Substitua com sua chave de API

def get_openai_response(prompt):
    """
    Função para obter a resposta da OpenAI usando o modelo GPT.
    Argumento:
    - prompt: A mensagem do usuário que será enviada para a IA.

    Retorna:
    - A resposta gerada pela IA.
    """
    try:
        # Chamada à API da OpenAI
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # Altere conforme o modelo disponível na sua conta OpenAI
            messages=[
                {"role": "system", "content": "Você é uma entidade digital que ajuda com informações."},  # Mensagem de configuração da IA
                {"role": "user", "content": prompt}  # A mensagem do usuário
            ]
        )
        # Retorna a resposta gerada
        return response['choices'][0]['message']['content'].strip()
    except Exception as e:
        print(f"Erro ao acessar a API da OpenAI: {e}")
        return None

