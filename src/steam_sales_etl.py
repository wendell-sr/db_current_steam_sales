import pandas as pd
from google.cloud import bigquery
from google.oauth2 import service_account
import requests
from bs4 import BeautifulSoup
import time
from datetime import datetime

class SteamSalesETL:
    def __init__(self, credentials_path):
        """
        Inicializa o pipeline ETL com as credenciais do Google Cloud
        
        Args:
            credentials_path (str): Caminho para o arquivo de credenciais JSON
        """
        self.credentials = service_account.Credentials.from_service_account_file(
            credentials_path,
            scopes=["https://www.googleapis.com/auth/cloud-platform"]
        )
        self.client = bigquery.Client(credentials=self.credentials)
        
    def extract_steam_data(self):
        """
        Extrai dados da página de promoções do Steam
        
        Returns:
            pandas.DataFrame: DataFrame com os dados extraídos
        """
        url = "https://steamdb.info/sales/"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        # Adiciona delay para respeitar limites de rate
        time.sleep(2)
        
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            table = soup.find('table', {'id': 'DataTables_Table_0'})
            
            data = []
            for row in table.find_all('tr')[1:]:  # Skip header row
                cols = row.find_all('td')
                if cols:
                    game_data = {
                        'name': cols[2].text.strip(),
                        'discount': cols[3].text.strip(),
                        'price': cols[4].text.strip(),
                        'rating': cols[5].text.strip(),
                        'ends_in': cols[6].text.strip(),
                        'extracted_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    }
                    data.append(game_data)
                    
            return pd.DataFrame(data)
            
        except Exception as e:
            print(f"Erro na extração: {str(e)}")
            return pd.DataFrame()
            
    def load_to_bigquery(self, df, table_id):
        """
        Carrega os dados para o BigQuery
        
        Args:
            df (pandas.DataFrame): DataFrame com os dados
            table_id (str): ID da tabela no formato 'projeto.dataset.tabela'
        """
        job_config = bigquery.LoadJobConfig(
            write_disposition="WRITE_TRUNCATE",
        )
        
        try:
            job = self.client.load_table_from_dataframe(
                df, table_id, job_config=job_config
            )
            job.result()  # Aguarda conclusão do job
            
            print(f"Carregados {len(df)} registros para {table_id}")
            
        except Exception as e:
            print(f"Erro no carregamento para BigQuery: {str(e)}")
            
    def run_pipeline(self, table_id):
        """
        Executa o pipeline completo
        
        Args:
            table_id (str): ID da tabela do BigQuery
        """
        print("Iniciando extração dos dados...")
        df = self.extract_steam_data()
        
        if not df.empty:
            print("Carregando dados para o BigQuery...")
            self.load_to_bigquery(df, table_id)
            print("Pipeline concluído com sucesso!")
        else:
            print("Não foram encontrados dados para processar.")

# Exemplo de uso
if __name__ == "__main__":
    CREDENTIALS_PATH = "path/to/your/credentials.json"
    TABLE_ID = "seu-projeto.seu_dataset.steam_sales"
    
    etl = SteamSalesETL(CREDENTIALS_PATH)
    etl.run_pipeline(TABLE_ID)