# Importando bibliotecas e pacotes
import csv
import time
from time import sleep
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

print('- Finalizado a importação de pacotes')

# Tarefa 1: Login to Linkedin

# Tarefa 1.1: Abrir o chrome e acessar a área de login
Path = 'C:\CHROME DRIVER\chromedriver.exe'
driver = webdriver.Chrome(Path)
sleep(0.2)
url = 'https://www.linkedin.com/login'
driver.get(url)
print('- Driver inicializado')
sleep(0.2)

# Tarefa 1.2: Importar username e password
# notar que o nome da pasta só ENCONTROU O DIRETÓRIO porque foi escrito separadamente "WebScrapping Linkedin"
credential = open('C:/Users/AlexLopes/PycharmProjects/WebScrapping Linkedin/login_credentials.txt')
line = credential.readlines()
username = line[0]
password = line[1]
print('- Finalizado importação de credenciais')
sleep(0.2)

# Tarefa 1.2: Digite as credenciais de login
# email_field = driver.find_element('username')
email_field = driver.find_element(By.XPATH, '//*[@id="username"]')
email_field.send_keys(username)
print('- Email colocado')
sleep(0.2)

# password_field = driver.find_element('session_password')
password_field = driver.find_element(By.XPATH, '//*[@id="password"]')
password_field.send_keys(password)
print('- Senha colocada')
sleep(0.2)

# Tarefa 1.2: Click no botão de login
# signin_field = driver.find_element('//*[@id="organic-div"]/form/div[3]/button')
signin_field = driver.find_element(By.XPATH, '//*[@id="organic-div"]/form/div[3]/button')
signin_field.click()
sleep(0.2)

print('- Login realizado')

# Tarefa 2: Procure o perfil que deseja consultar
# Tarefa 2.1: Localize o elemento da barra de pesquisa
search_field = driver.find_element(By.XPATH, '//*[@id="global-nav-typeahead"]/input')
time.sleep(0.2)
# Insira a consulta de pesquisa na barra de pesquisa(No Terminal)
# search_query = input('Qual perfil você deseja extrair? ')
# pyautogui.typewrite('Qualquer coisa que você queira digitar')
search_query = input('Qual skill deseja fazer o scrape?:')
search_field.send_keys(search_query)

# Tarefa 2.3: Pesquisar
search_field.send_keys(Keys.RETURN)
time.sleep(2)
# driver.find_element_by_link_text('Pessoas').click()
# button = driver.find_element(By.LINK_TEXT, 'Pessoas')
# button.click()
# time.sleep(2)

print('- Pronto para iniciar busca')


# Task 3: Extrair os URL's dos perfis
# Task 3.1: Função para extrair os URL's de uma página
def GetURL():
    page_source = BeautifulSoup(driver.page_source, "html.parser")

    # profiles = page_source.find_all(By.XPATH, "//a[contains('/in/')]")
    # By.linkText("click here")).click()

    profiles = page_source.find_all('a', class_ ='app-aware-link')
    # 'app-aware-link') #('a', class_ = 'search-result__result-link ember-view')
    # driver.find_element(By.XPATH
    all_profile_URL = []
    for profile in profiles:
        profile_ID = profile.get('href')
        profile_URL = "https://www.linkedin.com" + profile_ID
        profile_URL = profile.get('href')
        if profile_URL not in all_profile_URL:
            all_profile_URL.append(profile_URL)
    return all_profile_URL


# Tarefa 3.2: Navegar através de várias páginas, e extrair o perfil URL de cada página
input_page = int(input('Quantas páginas quer extrair: '))
URLs_all_page = []
for page in range(input_page):
    URLs_one_page = GetURL()
    sleep(2)
    driver.execute_script('window.scrollTo(0, document.body.scrollHeight);') #Desce até o fim da página
    sleep(3)
    next_button = driver.find_element(By.CLASS_NAME, 'artdeco-pagination__button--next')
    # 'artdeco-pagination__button--next artdeco-button artdeco-button--muted artdeco-button--icon-right artdeco-button--1 artdeco-button--tertiary ember-view')
    next_button.click()
    # driver.execute_script("arguments[0].click();", next_button)
    URLs_all_page = URLs_all_page + URLs_one_page
    sleep(3)

print('- URLs Extraídas')

# Tarefa 4: Raspe os dados de 1 perfil do Linkedin e grave os dados em um arquivo .CSV
with open('output.csv', 'w',  newline = '') as file_output:
    headers = ['Name', 'Job Title', 'Location', 'URL']
    writer = csv.DictWriter(file_output, delimiter=',', lineterminator='\n',fieldnames=headers)
    writer.writeheader()
    for linkedin_URL in URLs_all_page:
        driver.get(linkedin_URL)
        print('- Perfil Acessado: ', linkedin_URL)
        sleep(3)
        page_source = BeautifulSoup(driver.page_source, "html.parser")
        info_div = page_source.find('div',{'class':'flex-1 mr5'})
        try:
            name = info_div.find('li', class_='inline t-24 t-black t-normal break-words').get_text().strip() #Remove os caracteres desnecessários
            print('--- Nome do perfil é: ', name)
            location = info_div.find('li', class_='t-16 t-black t-normal inline-block').get_text().strip() #Remove os caracteres desnecessários
            print('--- Localização do perfil: ', location)
            title = info_div.find('h2', class_='mt1 t-18 t-black t-normal break-words').get_text().strip()
            print('--- Título do perfil é: ', title)
            writer.writerow({headers[0]:name, headers[1]:location, headers[2]:title, headers[3]:linkedin_URL})
            print('\n')
        except:
            pass

print('Finalizado!')
