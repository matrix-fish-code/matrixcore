import os
import boto3

# Configurações da OpenAI
openai_api_key = os.getenv("OPENAI_API_KEY")

# Configurações do AWS (S3)
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_REGION = 'eu-west-2'
S3_BUCKET_NAME = 'matrix.fish'

# Inicializando o cliente S3
s3_client = boto3.client(
    's3',
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name=AWS_REGION
)
