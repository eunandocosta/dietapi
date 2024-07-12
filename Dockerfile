# Use uma imagem base oficial do Python
FROM python:3.10-slim

# Instalar dependências necessárias
RUN apt-get update && apt-get install -y \
    libmariadb-dev-compat \
    build-essential \
    curl \
    pkg-config

# Copiar e instalar dependências do projeto
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir --default-timeout=180 -r requirements.txt

# Copiar o código da aplicação e o script wait-for-it
COPY . .
COPY wait-for-it.sh /wait-for-it.sh

# Dar permissão de execução ao script wait-for-it
RUN chmod +x /wait-for-it.sh

# Comando para rodar a aplicação
CMD ["./wait-for-it.sh", "db:3306", "--", "python", "app.py"]
