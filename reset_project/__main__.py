# __main__.py
import logging
import os
from datetime import datetime
from reset_project.sheets_management.read_sheet import main
from logging.handlers import RotatingFileHandler


def setup_logging():
    # Criar uma pasta 'logs' se não existir
    log_directory = 'logs'
    if not os.path.exists(log_directory):
        os.makedirs(log_directory)

    # Adicionar um carimbo de data e hora ao nome do arquivo de log
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    log_file = f'reset_senhas_{timestamp}.log'
    log_path = os.path.abspath(os.path.join(log_directory, log_file))

    # Configuração do logger com RotatingFileHandler
    handler = RotatingFileHandler(log_path, maxBytes=10*1024*1024, backupCount=5)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)

    logger = logging.getLogger()
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)

def run_main():
    try:
        main()
        logging.info('Execução finalizada. Todas as senhas foram atualizadas com sucesso.')
    except Exception as e:
        logging.error(f'Tivemos uma falha durante a redefinição de senha: {e}', exc_info=True)

if __name__ == '__main__':
    setup_logging()
    logging.info('Início da execução do script. Vamos resetar a senha de todos os owners da planilha')

    try:
        run_main()
    except Exception as e:
        logging.error(f'Ocorreu um erro ao abrir ou processar a planilha: {e}')