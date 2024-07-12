# Alimento API

Esta aplicação é uma API RESTful construída com Flask para gerenciar dietas, refeições e alimentos. A API permite criar, listar, atualizar e deletar dietas e alimentos em um banco de dados. A aplicação utiliza SQLAlchemy para interação com o banco de dados e Pydantic para validação de dados.

## Estrutura do Projeto

- `app.py`: Contém as rotas e lógica principal da API.
- `models/model.py`: Define os modelos Dieta, Refeicao e Alimento.
- `database.py`: Configura a conexão com o banco de dados.
- `schemas/schema.py`: Define os schemas de validação usando Pydantic.
- `logs/log_config.py`: Configuração de logs para a aplicação.
- `Dockerfile`: Define a imagem Docker para a aplicação.
- `docker-compose.yml`: Define os serviços Docker para a aplicação.
- `README.md`: Documentação do projeto.

## Requisitos

- Python 3.x
- Flask
- SQLAlchemy
- Pydantic
- Docker (opcional)
- Docker Compose (opcional)

## Instalação

### Manualmente

1. Clone o repositório:

```bash
git clone https://github.com/eunandocosta/db_taco.git
cd db_taco
```

2. Crie e ative um ambiente virtual:

```bash
python -m venv venv
source venv/bin/activate  # No Windows, use `venv\Scripts\activate`
```

3. Instale as dependências:

```bash
pip install -r requirements.txt
```

4. Configure o banco de dados em `database.py`:

```python
DATABASE_URL = "mysql+pymysql://root:chuck@db:3306/dietas"  # Exemplo de banco de dados SQLite
```

5. Crie o banco de dados:

```bash
python
>>> from database import Base, engine
>>> Base.metadata.create_all(bind=engine)
>>> exit()
```

### Usando Docker

1. Clone o repositório:

```bash
git clone https://github.com/eunandocosta/db_taco.git
cd db_taco
```

2. Construa e inicie os containers Docker:

```bash
docker-compose up --build
```

A API estará disponível em `http://127.0.0.1:5001`.

## Uso

### Iniciar o Servidor

Inicie o servidor Flask:

```bash
flask run
```

A API estará disponível em `http://127.0.0.1:5001`.

### Endpoints

#### Criar Dieta

Adiciona uma nova dieta ao banco de dados.

- **URL**: `/dietas`
- **Método**: `POST`
- **Corpo da Requisição**: JSON

```json
{
  "firebase_uuid": "user-123",
  "refeicoes": [
    {
      "tipo": "café da manhã",
      "alimentos": [
        {
          "nome": "banana",
          "quantidade": "1 unidade"
        }
      ]
    }
  ]
}
```

- **Resposta de Sucesso**: `201 Created`
- **Resposta de Erro**: `400 Bad Request` se houver erro de validação.

#### Deletar Dietas

Deleta todas as dietas associadas a um UUID do Firebase.

- **URL**: `/delete_dietas`
- **Método**: `DELETE`
- **Corpo da Requisição**: JSON

```json
{
  "firebase_uuid": "user-123"
}
```

- **Resposta de Sucesso**: `200 OK`
- **Resposta de Erro**: `404 Not Found` se nenhuma dieta for encontrada.

#### Buscar Dieta

Busca uma dieta pelo UUID do Firebase.

- **URL**: `/dieta`
- **Método**: `GET`
- **Parâmetro de Consulta**: `firebase_uuid` (string)

- **Exemplo**:

  `GET /dieta?firebase_uuid=user-123`

- **Resposta de Sucesso**: `200 OK`
- **Resposta de Erro**: `404 Not Found` se nenhuma dieta for encontrada.

#### Deletar Dieta por ID

Deleta uma dieta pelo ID.

- **URL**: `/dietas/<int:id>`
- **Método**: `DELETE`

- **Exemplo**:

  `DELETE /dietas/1`

- **Resposta de Sucesso**: `200 OK`
- **Resposta de Erro**: `404 Not Found` se a dieta não for encontrada.

#### Atualizar Quantidade de Alimento

Atualiza a quantidade de um alimento.

- **URL**: `/update_quantidade`
- **Método**: `PUT`
- **Corpo da Requisição**: JSON

```json
{
  "alimento_id": 1,
  "nova_quantidade": "2 unidades"
}
```

- **Resposta de Sucesso**: `200 OK`
- **Resposta de Erro**: `404 Not Found` se o alimento não for encontrado.

#### Deletar Alimento

Deleta um alimento pelo ID.

- **URL**: `/delete_alimento`
- **Método**: `DELETE`
- **Corpo da Requisição**: JSON

```json
{
  "alimento_id": 1
}
```

- **Resposta de Sucesso**: `200 OK`
- **Resposta de Erro**: `404 Not Found` se o alimento não for encontrado.

## Modelo de Dados

O modelo de dados inclui três principais entidades: `Dieta`, `Refeicao` e `Alimento`, definidos em `models/model.py`.

## Logging

A aplicação utiliza um módulo de configuração de logs em `logs/log_config.py` para registrar informações sobre as operações executadas.

## Docker

A aplicação inclui suporte para Docker, permitindo fácil configuração e implantação.

### Dockerfile

O `Dockerfile` define a imagem Docker para a aplicação:

```dockerfile
# Use uma imagem base oficial do Python como base
FROM python:3.9-slim

# Defina o diretório de trabalho
WORKDIR /app

# Copie o requirements.txt e instale as dependências
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copie o restante do código da aplicação
COPY . .

# Defina a variável de ambiente para a aplicação Flask
ENV FLASK_APP=app.py

# Exponha a porta que o Flask está rodando
EXPOSE 5001

# Comando para rodar a aplicação
CMD ["flask", "run", "--host=0.0.0.0", "--port=5001"]
```

### docker-compose.yml

O `docker-compose.yml` define os serviços Docker para a aplicação:

```yaml
version: '3.8'

services:
  web:
    build: .
    ports:
      - "5001:5001"
    volumes:
      - .:/app
    environment:
      - FLASK_ENV=development
```

### Contribuições

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues e pull requests.

### Licença

Este projeto está licenciado sob a MIT License. Veja o arquivo `LICENSE` para mais detalhes.
