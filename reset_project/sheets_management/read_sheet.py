import json
import logging
import os
from dotenv import load_dotenv
from selenium.common.exceptions import WebDriverException
from retrying import retry      
from reset_project.password_reset.platform_access import rpa_reset, webdriver_instance, login_master
from .autentication import load_credentials, authorize_client

# Configuração de Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Constantes
CREDENTIALS_FILE_PATH = '***'
ENV_FILE_PATH = '***'
SHEET_ID_VARIABLE_NAME = '***'
SHEET_COLUMNS = {
    'URL': 1,
    'ID Owner': 2,
    'Owner': 3,
    'Senha': 4,
}

def setup():
    # Carregar variáveis de ambiente
    load_dotenv(ENV_FILE_PATH)
    sheet_id = os.getenv(SHEET_ID_VARIABLE_NAME)

    # Carregar credenciais
    with open(CREDENTIALS_FILE_PATH, 'r') as file:
        credentials_data = json.load(file)

    return sheet_id, credentials_data

def main():
    try:
        sheet_id, credentials_data = setup()

        credential = load_credentials(credentials_data)

        if credential:
            # Autorizar cliente
            client = authorize_client(credential)

            if client:
                get_sheet_by_id_with_retry(client, sheet_id)

    except Exception as e:
        logger.error(f'Erro no processo de autenticação: {e}')

@retry(stop_max_attempt_number=3, wait_exponential_multiplier=1000, wait_exponential_max=10000)
def get_sheet_by_id_with_retry(client, sheet_id):
    try:
        get_sheet_by_id(client, sheet_id)
    except Exception as e:
        logger.error(f'Ocorreu um erro: {e}')
        raise

def get_sheet_by_id(client, sheet_id):
    driver_instance = None

    try:
        # Inicialize o navegador fora do loop de usuários
        driver_instance = webdriver_instance(browser='Chrome')

        # Abrir a planilha pelo ID
        sheet = client.open_by_key(sheet_id).sheet1

        # Obtém todos os valores da planilha
        all_values = sheet.get_all_values()

        # Certifique-se de que há pelo menos uma linha e uma coluna
        if not all_values or not all_values[0]:
            logging.error('A planilha está vazia ou não contém colunas.')
            return None

        # Encontra as colunas desejadas
        header_row = all_values[0]

        required_columns = ["URL", "ID Owner", "Owner", "Senha"]
        column_indices = {column: header_row.index(column) + 1 for column in required_columns}

        # Verifica se todas as colunas necessárias foram encontradas
        if None in column_indices.values():
            logging.error('Alguma coluna necessária não foi encontrada na planilha.')
            return None

        id_owner_column = column_indices["ID Owner"]
        owner_column = column_indices["Owner"]
        senha_column = column_indices["Senha"]

        # Lista para armazenar exceções ocorridas
        exceptions = []
        iteration = 1
        # Pula a primeira linha, que é geralmente o cabeçalho
        for i, row in enumerate(all_values[1:], start=2):
            id_owner = row[id_owner_column - 1]
            owner = row[owner_column - 1]
            try:
                if iteration == 1:
                    login_master(driver_instance)
                    iteration = 2
                new_password = rpa_reset(driver_instance, id_owner, owner,)
                
                if new_password:
                    # Atualizar a planilha com a nova senha
                    sheet.update_cell(i, senha_column, new_password)
                    logging.info(f"Nova senha para {owner} foi atualizada na planilha.")
                
            except Exception as user_exception:
                exceptions.append((owner, user_exception))

        # Se houver exceções, você pode tratá-las ou registrar conforme necessário
        if exceptions:
            logging.warning(f'Exceções ocorreram para os seguintes usuários: {exceptions}')

    except Exception as e:
        logging.error(f'Ocorreu um erro ao abrir ou processar a planilha: {e}')
        raise
    finally:
        # Feche a instância do driver aqui para garantir que seja fechado corretamente
        if driver_instance:
            driver_instance.quit()