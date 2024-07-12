# DietApp - Gerenciador de Dietas

## Descrição

DietApp é uma API desenvolvida para ajudar os usuários a gerenciarem suas dietas de maneira eficiente. Com ela, é possível criar, visualizar, editar e deletar refeições e alimentos, utilizando o Flask para o backend, SQLAlchemy para ORM e MySQL como banco de dados.

## Tecnologias Utilizadas

- **Flask**: Microframework para construção de APIs em Python.
- **SQLAlchemy**: ORM para interação com o banco de dados.
- **MySQL**: Banco de dados relacional.
- **Pydantic**: Validação de dados.
- **Docker**: Para containerização da aplicação.
- **Docker Compose**: Para orquestração dos containers.

## Estrutura do Projeto

- `app.py`: Arquivo principal da aplicação Flask.
- `config.py`: Configurações da aplicação.
- `database.py`: Configuração do banco de dados e inicialização do SQLAlchemy.
- `models`: Contém os modelos do SQLAlchemy.
- `schemas`: Contém os schemas do Pydantic para validação de dados.
- `logs`: Diretório para arquivos de log.
- `Dockerfile`: Arquivo para construir a imagem Docker da aplicação.
- `docker-compose.yml`: Arquivo de configuração do Docker Compose.
- `requirements.txt`: Arquivo com as dependências do projeto.
- `wait-for-it.sh`: Script para garantir que o MySQL esteja disponível antes de iniciar a aplicação Flask.

## Instalação

### Pré-requisitos

- Docker e Docker Compose instalados na sua máquina.

### Passos para Configuração

1. Clone o repositório:

    ```bash
    git clone https://github.com/eunandocosta/dietapi.git
    cd dietapi
    ```

2. Configure as variáveis de ambiente no arquivo `docker-compose.yml` se necessário.

3. Inicie os containers Docker:

    ```bash
    docker-compose up --build
    ```

4. A aplicação estará disponível em `http://localhost:5001`.

## Endpoints

### Criar Dieta

- **URL**: `/dietas`
- **Método**: `POST`
- **Descrição**: Cria uma nova dieta.
- **Corpo da Requisição**:
    ```json
    {
        "firebase_uuid": "string",
        "refeicoes": [
            {
                "tipo": "string",
                "alimentos": [
                    {
                        "nome": "string",
                        "quantidade": "string"
                    }
                ]
            }
        ]
    }
    ```

### Buscar Dieta

- **URL**: `/dieta`
- **Método**: `GET`
- **Descrição**: Busca uma dieta pelo UUID do Firebase.
- **Parâmetros**:
    - `firebase_uuid`: UUID do Firebase do usuário.

### Deletar Dieta

- **URL**: `/dietas/<int:id>`
- **Método**: `DELETE`
- **Descrição**: Deleta uma dieta pelo ID.

### Atualizar Quantidade de Alimento

- **URL**: `/update_quantidade`
- **Método**: `PUT`
- **Descrição**: Atualiza a quantidade de um alimento.
- **Corpo da Requisição**:
    ```json
    {
        "alimento_id": "int",
        "nova_quantidade": "string"
    }
    ```

### Deletar Alimento

- **URL**: `/delete_alimento`
- **Método**: `DELETE`
- **Descrição**: Deleta um alimento pelo ID.
- **Corpo da Requisição**:
    ```json
    {
        "alimento_id": "int"
    }
    ```

## Licença

Este projeto está licenciado sob a MIT License - veja o arquivo LICENSE para mais detalhes.
