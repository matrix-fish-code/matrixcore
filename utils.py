import json
from datetime import datetime
import boto3
from config import s3_client, S3_BUCKET_NAME

def save_interaction_to_s3(prompt, response):
    # Gerar um ID único para a interação com base no timestamp
    interaction_id = f"interaction_{str(int(datetime.timestamp(datetime.now())))}"
    timestamp = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")

    # Criar a estrutura da interação
    interaction = {
        "interaction_id": interaction_id,
        "timestamp": timestamp,
        "prompt": prompt,
        "response": response
    }

    # Definir o caminho do arquivo no S3
    file_name = f"interactions/{timestamp.split('T')[0]}/interactions_{timestamp.split('T')[0]}.json"

    # Salvar a interação no S3
    s3_client.put_object(
        Bucket=S3_BUCKET_NAME,
        Key=file_name,
        Body=json.dumps(interaction)
    )
    print("Interação salva no S3 com sucesso!")

