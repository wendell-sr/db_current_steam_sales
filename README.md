# Pipeline ETL de Vendas da Steam

Este projeto implementa um pipeline ETL (Extração, Transformação e Carregamento) para coletar dados de promoções da Steam e armazená-los no Google BigQuery.

## Estrutura do Projeto

```
db_current_steam_sales/
├── README.md           # Este arquivo
├── requirements.txt    # Dependências do projeto
├── msedgedriver.exe    # Driver do navegador Microsoft Edge para utilização com o Selenium
├── src/               # Código fonte
│   ├── setup_bigquery.py    # Script para configuração inicial do BigQuery
│   └── steam_sales_etl.py   # Pipeline ETL principal
├── config/            # Arquivos de configuração
│   └── credentials.json      # Credenciais do Google Cloud (não versionado)
└── .gitignore        # Arquivos ignorados pelo Git
```

## Pré-requisitos

- Python 3.8+
- Microsoft Edge WebDriver
- Conta no Google Cloud Platform com BigQuery habilitado
- Credenciais do Google Cloud configuradas

## Instalação

1. Clone o repositório:
```bash
git clone https://github.com/wendell-sr/db_current_steam_sales.git
cd db_current_steam_sales
```
2. Instale as dependências:
```bash
pip install -r requirements.txt
```
3. Configure as credenciais:
   - Coloque seu arquivo `credentials.json` do Google Cloud na pasta `config/`.

## Configuração

1. Execute o script de setup para criar o dataset e a tabela no BigQuery:
```bash
python src/setup_bigquery.py
```

## Uso

Execute o pipeline ETL:
```bash
python src/steam_sales_etl.py
```

## Estrutura dos Dados

Os dados coletados e armazenados no BigQuery incluem:

- App_ID (ID do aplicativo)
- Image_URL (URL da imagem do jogo)
- Name (Nome do jogo)
- Discount (Desconto)
- Price (Preço)
- Rating (Avaliação)
- Release_Date (Data de lançamento)
- Ends (Fim da promoção)
- Starts (Início da promoção)

## Dependências Principais

- selenium: Web scraping
- beautifulsoup4: Parsing HTML
- google-cloud-bigquery: Integração com BigQuery
- pandas: Manipulação de dados

## Contribuição

1. Faça um Fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## Autores

- Wendell Pereira Marques - Desenvolvimento inicial

