from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from .generator import PasswordGenerator
import pyautogui
import logging
from time import sleep	

logger = logging.getLogger(__name__)

def login_master(driver):
    url_login  = 'https://domain.com.br/auth/signin?scflogin=1'
    driver.get(url_login)
    # Inserindo os dados do usuário
    enter_input(driver, By.ID, 'inputUsername', '***')
    enter_input(driver, By.ID, 'inputPassword', '***')
    pyautogui.press('enter')
    sleep(8)

def rpa_reset(driver, id_owner, owner):
    url_user_detail = f'https://domain.com.br/users/{id_owner}/edit'
    
    try:
        driver.get(url_user_detail)        
        # Aguarde até que algum elemento na página seja visível
        element_present = EC.presence_of_element_located((By.CLASS_NAME, 'user-menu pull-left'))
        WebDriverWait(driver, timeout=30).until(element_present)
        
    except Exception as e:
        logging.error(f'Erro ao acessar a página ou aguardar sua carga: {e}')

    generated_password = generate_and_set_password(driver)

    logger.info(f'Nova senha do owner {owner} é {generated_password}')
    return generated_password

def webdriver_instance(browser):
    if browser.lower() == 'firefox':
        return webdriver.Firefox()
    elif browser.lower() == 'chrome':
        return webdriver.Chrome()
    else:
        raise ValueError(f'Navegador não suportado: {browser}')

def enter_input(driver, by, identifier, value):
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((by, identifier))).send_keys(value)

def click_button(driver, by, identifier):
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((by, identifier))).click()

def generate_and_set_password(driver):
    password_generator = PasswordGenerator()
    generated_password = password_generator.random_password()

    enter_input(driver, By.ID, 'password', generated_password)
    enter_input(driver, By.ID, 'password-confirm', generated_password)
    pyautogui.press('Enter')

    return generated_password