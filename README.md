# Roof Imoveis - Housing Price Analysis

Projeto de análise e modelagem preditiva com dados imobiliários de King County. O notebook organiza etapas de entendimento do negócio, análise exploratória, tratamento de dados e comparação de modelos para estimar preços de imóveis.

## Objetivo

Avaliar quais características mais influenciam o preço de venda de imóveis e construir uma base analítica para apoiar decisões de precificação.

## O que o projeto demonstra

- Leitura e exploração de um dataset tabular real (`kc_house_data.csv`).
- Verificação de qualidade: nulos, duplicados, tipos de dados e outliers.
- Análise exploratória com correlações, distribuições e variáveis categóricas.
- Preparação de atributos para modelagem supervisionada.
- Teste de modelos de regressão, incluindo árvores, modelos lineares, SVM, Random Forest e XGBoost.
- Uso de métricas para comparar desempenho dos modelos.

## Stack

- Python
- Pandas e NumPy
- Plotly, Matplotlib e Seaborn
- Scikit-learn
- XGBoost
- Jupyter Notebook / Google Colab

## Arquivos

| Arquivo | Descrição |
| --- | --- |
| `Roof_Imóveis_2.ipynb` | Notebook principal com EDA, tratamento e modelagem. |
| `kc_house_data.csv` | Base utilizada no estudo. |

## Como executar

1. Abra o notebook `Roof_Imóveis_2.ipynb` no Jupyter ou Google Colab.
2. Garanta que `kc_house_data.csv` esteja no mesmo diretório do notebook.
3. Execute as células em ordem, começando pela seção de importação das bibliotecas.

## Pontos fortes para portfólio

Este é um dos projetos mais completos do portfólio por combinar análise de negócio, preparação de dados e modelagem preditiva. Para uma vaga júnior de Engenharia de Dados, ele mostra familiaridade com dados tabulares, validação básica de qualidade e raciocínio analítico antes da modelagem.

## Limitações atuais

- O fluxo ainda está concentrado em um notebook único.
- Não há `requirements.txt`, ambiente versionado ou testes automatizados.
- Os caminhos de leitura misturam referências locais e Colab.
- O projeto ainda não tem uma camada de pipeline reutilizável para ingestão, tratamento e treino.

## Próximas melhorias recomendadas

- Separar o notebook em módulos: `src/data`, `src/features` e `src/models`.
- Criar `requirements.txt` ou `pyproject.toml`.
- Adicionar validações de qualidade com Great Expectations, Pandera ou testes unitários simples.
- Criar um pipeline reproduzível com Makefile, CLI ou notebook parametrizado.
- Registrar métricas de modelos em uma tabela comparativa final.
