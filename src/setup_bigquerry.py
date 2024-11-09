from google.cloud import bigquery
from google.oauth2 import service_account


credentials = service_account.Credentials.from_service_account_file(
    'config/credentials.json'
)


client = bigquery.Client(credentials=credentials)


dataset_id = f"{client.project}.steam_sales"
dataset = bigquery.Dataset(dataset_id)
dataset.location = "US"
dataset = client.create_dataset(dataset, exists_ok=True)
print(f"Dataset {dataset_id} criado com sucesso.")


table_id = f"{dataset_id}.sales"
table = bigquery.Table(table_id)
table.schema = [
    bigquery.SchemaField("App_ID", "STRING"),
    bigquery.SchemaField("Image_URL", "STRING"),
    bigquery.SchemaField("Name", "STRING"),
    bigquery.SchemaField("Discount", "STRING"),
    bigquery.SchemaField("Price", "STRING"),
    bigquery.SchemaField("Rating", "STRING"),
    bigquery.SchemaField("Release_Date", "STRING"),
    bigquery.SchemaField("Ends", "STRING"),
    bigquery.SchemaField("Starts", "STRING")
]
table = client.create_table(table, exists_ok=True)
print(f"Tabela {table_id} criada com sucesso.")
