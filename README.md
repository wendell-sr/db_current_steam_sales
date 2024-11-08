# Steam Sales ETL Pipeline

Este projeto implementa um pipeline ETL (Extract, Transform, Load) para coletar dados de promoções da Steam e armazená-los no Google BigQuery.

## Estrutura do Projeto

```
steam-sales-etl/
├── README.md           # Este arquivo
├── requirements.txt    # Dependências do projeto
├── src/               # Código fonte
│   ├── setup_bigquery.py    # Script para configuração inicial do BigQuery
│   └── steam_sales_etl.py   # Pipeline ETL principal
├── config/            # Arquivos de configuração
│   └── credentials.json      # Credenciais do Google Cloud (não versionado)
└── .gitignore        # Arquivos ignorados pelo Git
```

## Pré-requisitos

- Python 3.8+
- Conta no Google Cloud Platform
- Credenciais do GCP com acesso ao BigQuery

## Instalação

1. Clone o repositório:
```bash
git clone https://github.com/seu-usuario/steam-sales-etl.git
cd steam-sales-etl
```

2. Instale as dependências:
```bash
pip install -r requirements.txt
```

3. Configure as credenciais:
- Coloque seu arquivo `credentials.json` do Google Cloud na pasta `config/`

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

Os dados coletados incluem:
- Nome do jogo
- Desconto
- Preço
- Avaliação
- Tempo restante da promoção
- Data/hora da extração

## Contribuição

1. Faça o fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/nova-feature`)
3. Commit suas mudanças (`git commit -m 'Adiciona nova feature'`)
4. Push para a branch (`git push origin feature/nova-feature`)
5. Abra um Pull Request
