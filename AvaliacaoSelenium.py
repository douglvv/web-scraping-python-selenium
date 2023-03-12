# Avaliação Prática
# Utilizando a ferramenta Selenium com Python:

# Escolher um site para entrar, fazer busca e capturar texto

# Entrar no site
# Executar 4 ações (Navegação em menus, busca, ordenação)
# Capturar conteúdo e salvar em arquivo csv.


#---------------------------- IMPORTS ------------------------------
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup #pip install bs4
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC #importa e cria o objeto EC
from selenium.webdriver.common.action_chains import ActionChains
import time
from csv import writer
#-------------------------------------------------------------------

#Define as opções do driver
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
options.add_argument("--incognito")
options.add_argument("--log-level=3")

driver = webdriver.Chrome(options=options) #Cria o objeto do driver

url = 'https://ge.globo.com/' #url inicial

print('Passo 1: Acessar o site do Globo Esporte')
try:
    driver.get(url) #acessa a url
    driver.implicitly_wait(10)
    driver.save_screenshot('tela01.png')
    time.sleep(2)
except:
    driver.quit()
    print('Erro ao acessar o site da do Globo Esporte')
    quit()

print('Passo 2: Navega pelo menu e acessa a página de Estatísticas Brasileirão 2022')
try:
    action = ActionChains(driver) #Cria o objeto action chains
    #Clica em menu
    try:
        menu = WebDriverWait(driver,20).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="header-produto"]/div[2]/div/div/div[1]/div')))
        action.move_to_element(menu).click().perform()
    except:
        print("Erro ao acessar o menu")

    #Clica em tabelas
    try:
        menu = WebDriverWait(driver,5).until(EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT,'tabelas')))
        action.move_to_element(menu).click().perform()
    except:
        print("Erro ao acessar tabelas")

    #Clica em nacionais
    try:
        menu = WebDriverWait(driver,5).until(EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT,'nacionais')))
        action.move_to_element(menu).click().perform()
    except:
        print("Erro ao acessar nacionais")
    
    #Clica em Brasileirao serie a
    try:
        menu = WebDriverWait(driver,5).until(EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT,'brasileirão série a')))
        action.move_to_element(menu).click().perform()
    except:
        print("Erro ao cessar brasileirão série a")

    #Clica em Brasileirao estatisticas
    try:
        menu = WebDriverWait(driver,5).until(EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT,'estatísticas')))
        action.move_to_element(menu).click().perform()
    except:
        print("Erro ao acessar estatísticas")
    
    #clica em mostrar mais
    try:
        menu = WebDriverWait(driver,5).until(EC.element_to_be_clickable((By.XPATH,'/html/body/main/div[3]/div/section[1]/ul/li[1]/section/button')))
        action.move_to_element(menu).click().perform()
    except:
        print("Erro ao clicar em mostrar mais")

    driver.save_screenshot('tela02.png')

    time.sleep(2)
except:
    driver.quit()
    print('Erro ao acessar a página de estatísticas')
    quit()

print('Passo 3: Capturar dados da tabela de artilheiros')
try:
    tabela = WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH,'/html/body/main/div[3]/div/section[1]/ul/li[1]/section/div[2]/div[2]/div')))
    conteudo_html = tabela.get_attribute('outerHTML') #salva apenas o outerHTML da tabela
    lista = BeautifulSoup(conteudo_html,'html.parser') #converte lista para HTML

    #Cria o arquivo csv com a lista de artilheiros
    with open('lista_artilheiros.csv','w') as arquivo:
        for dados in lista.find_all('figcaption',{'class':'ranking__celula ranking__celula--figure'}):
            linha = ''
            for nome in dados.find_all('div',{'class':'ranking__nome'}): #encontra o jogador
                linha=nome.text.replace('\n',"")
            for posicao in dados.find_all('div',{'class':'ranking__posicao'}):#encontra a posicao
                linha +='\t'+posicao.text.replace('\n',"")
            for jogos in dados.find_all('div',{'class':'ranking__results--item ranking__results--jogos'}): #encontra o nº de jogos
                linha +='\t'+jogos.text.replace('Jogos:',"")
            for gols in dados.find_all('div',{'class':'ranking__results--item ranking__results--total'}): #encontra o nº de gols
                linha += '\t'+gols.text
            print(linha)
            arquivo.write(linha+'\n') #escreve os dados armazenados em linha e pula para a próxima linha
    arquivo.close()

except:
    driver.quit()
    print('Erro ao capturar dados da tabela')
    quit()

print('Teste realizado com sucesso')
driver.quit()