from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from bs4 import BeautifulSoup
import pandas as pd
from google.cloud import bigquery
from google.oauth2 import service_account
import time

class SteamSalesETL:
    def __init__(self, credentials_path):
        self.credentials = service_account.Credentials.from_service_account_file(
            credentials_path,
            scopes=[
                'https://www.googleapis.com/auth/bigquery',
            ]
        )
        self.bq_client = bigquery.Client(credentials=self.credentials)
        self.driver_path = 'C:/Users/Wendell/Desktop/teste_engenheiro_dados/msedgedriver.exe'
        self.service = Service(self.driver_path)
        
    def extract_data(self):
        driver = webdriver.Edge(service=self.service)
        driver.get("https://steamdb.info/sales/")
        WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.ID, "dt-length-0")))
        
        select_element = driver.find_element(By.ID, "dt-length-0")
        select = Select(select_element)
        select.select_by_value("-1")
        
        WebDriverWait(driver, 15).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "timeago")))
        time.sleep(5)
        
        soup = BeautifulSoup(driver.page_source, "html.parser")
        games = soup.find_all("tr", class_="app")
        
        games_data = []
        for game in games:
            try:
                app_id = game.get('data-appid')
                img_url = game.find('td', class_='applogo').find('img').get('src', '/static/img/applogo.svg')
                name = game.find('a', class_='b').text.strip()
                cells = game.find_all('td')
                discount = cells[3].text.strip() if len(cells) > 3 else '0%'
                price = cells[4].text.strip() if len(cells) > 4 else 'Free'
                
                games_data.append({
                    "App_ID": app_id,
                    "Image_URL": img_url,
                    "Name": name,
                    "Discount": discount,
                    "Price": price
                })
            except Exception as e:
                print(f"Erro ao processar jogo: {e}")
        
        driver.quit()
        return pd.DataFrame(games_data)
    
    def load_to_bigquery(self, df, table_id):
        schema = [
            bigquery.SchemaField("App_ID", "STRING"),
            bigquery.SchemaField("Image_URL", "STRING"),
            bigquery.SchemaField("Name", "STRING"),
            bigquery.SchemaField("Discount", "STRING"),
            bigquery.SchemaField("Price", "STRING")
        ]
        
        job_config = bigquery.LoadJobConfig(
            schema=schema,
            write_disposition="WRITE_TRUNCATE"
        )
        
        job = self.bq_client.load_table_from_dataframe(df, table_id, job_config=job_config)
        job.result()
        print(f"Carregados {len(df)} registros para {table_id}")

if __name__ == "__main__":
    CREDENTIALS_PATH = "config/credentials.json"
    PROJECT_ID = "sales-steam"
    DATASET_ID = "sales-steam.steam_sales"
    TABLE_ID = "sales-steam.steam_sales.sales"

    etl = SteamSalesETL(CREDENTIALS_PATH)
    df = etl.extract_data()
    if not df.empty:
        etl.load_to_bigquery(df, TABLE_ID)
