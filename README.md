# Sistema de Gestão Operacional de Abrigo de Animais

Projeto final da disciplina de Tópicos e Bancos de Dados (UFSCar - 2026), desenvolvido para centralizar o cadastro de pessoas, animais resgatados e processos de adoção utilizando PostgreSQL e Python.

## Autores
- Lucas Mattos de Oliveira (824580)
- Luiz Henrique Carlson Ferreira (822652)
- Matheus Araújo Lima (822352)

## Ambiente e Versões Utilizadas
- **Sistema Operacional:** Ubuntu 22.04 LTS (WSL2) / Windows 11
- **Docker:** 27.x
- **Docker Compose:** v2.29.x
- **PostgreSQL:** 16 (imagem oficial `postgres:16`)
- **Python:** 3.11 (`psycopg2-binary==2.9.9`)

## Estrutura do Repositório
- `bd/01_ddl.sql`: Criação das tabelas, restrições (`UNIQUE`, `CHECK`, `FOREIGN KEY`), `VIEW` e `TRIGGER`.
- `bd/02_dml.sql`: Carga inicial de dados de teste.
- `app/main.py`: Aplicação CLI em Python integrada ao PostgreSQL.
- `app/Dockerfile`: Definição da imagem da aplicação Python.
- `app/requirements.txt`: Dependências Python do projeto.
- `docker-compose.yml`: Orquestração dos contêineres da aplicação e do banco de dados.

## Como Executar com Docker Compose (Recomendado)

1. **Clone o repositório e acesse a pasta:**
   ```bash
   git clone [https://github.com/matheusalima99/tbdes-projeto-abrigo.git](https://github.com/matheusalima99/tbdes-projeto-abrigo.git)
   cd tbdes-projeto-abrigo