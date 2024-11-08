from google.cloud import bigquery
from google.oauth2 import service_account

credentials = service_account.Credentials.from_service_account_file(
    'config/credentials.json'
)

client = bigquery.Client(credentials=credentials)

# Cria o dataset
dataset_id = f"{client.project}.steam_sales"
dataset = bigquery.Dataset(dataset_id)
dataset.location = "US"  # Especifica a localização do dataset
dataset = client.create_dataset(dataset, exists_ok=True)

print(f"Dataset {dataset_id} criado com sucesso.")