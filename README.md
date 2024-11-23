# Projeto Final - Data Prep & Transformation

## Sobre o Projeto

Este projeto teve como objetivo a criação de um pipeline de dados para transformar uma base transacional em um Star Schema e uma Wide Table, proporcionando uma estrutura otimizada para análises e consultas.

Foi utilizado o dataset da Olist (https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce?resource=download&select=olist_customers_dataset.csv), que contém 9 arquivos em formato CSV.

## Stack utilizada

Banco de dados Star Schema e Wide Table: PostgreSQL 

Carregamento dos dados: Python

Processamento (DataPrep):

## Arquitetura Star Schema

Foi utilizado o Power Architect para modelar e organizar os relacionamentos necessários para a construção do Star Schema. A arquitetura ficou dividida pelas seguintes dimensões e fato:

Dimensões:
- Customers;
- Reviews;
- Products;
- Geolocation;
- Sellers;
- Data.

Fato:
- Orders.

### Star Schema final:
<img src="starschema_olist.png" width="80%">



Essa estrutura foi pensada para garantir flexibilidade e eficiência em análises de dados.





