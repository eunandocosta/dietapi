import logging
from logging.handlers import RotatingFileHandler
import os

# Define a função de configuração de logging
def setup_logging():
    # Cria o diretório de logs se não existir
    if not os.path.exists('logs'):
        os.makedirs('logs')

    # Configura o handler de arquivo com rotação
    file_handler = RotatingFileHandler('logs/app.log', maxBytes=10240, backupCount=10)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
    ))

    # Define o nível de logging
    file_handler.setLevel(logging.INFO)

    # Adiciona o handler ao logger global
    app_logger = logging.getLogger()
    app_logger.addHandler(file_handler)
    app_logger.setLevel(logging.INFO)

    app_logger.info('Logging setup complete')

    return app_logger
