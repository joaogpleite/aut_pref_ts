import time
import pandas as pd
import gspread
import getpass 
import requests

from oauth2client.service_account import ServiceAccountCredentials
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

nome_json = '/content/insperautomacao-joao-2f50fd8a490f.json'
conta = ServiceAccountCredentials.from_json_keyfile_name(nome_json)
token = TELEGRAM_API_KEY

api = gspread.authorize(conta) # sheets.new
planilha = api.open_by_key("1bmLZIrWU1GG_ikJKRcZNtmmFELcYrBK2dMYqFQIV0Gs")
sheet = planilha.worksheet("lic1")

# URL da página a ser acessada
url = "https://leideacesso.etransparencia.com.br/taboaodaserra.prefeitura.sp/TDAPortalClient.aspx?417"

# Opções do navegador
options = Options()
options.add_argument("--headless")
options.add_argument("--no-sandbox")

# Inicialização do driver
driver = webdriver.Chrome("chromedriver", options=options)

# Navegação para a página
driver.get(url)

# Espera para carregar a página
time.sleep(4)

# Clique no botão desejado
botao = '/html/body/form/div[2]/div[2]/div[1]/div/div[2]/div/section/div/div/div/div/div[3]/div[2]/div/div/div/div[3]/div/table/tbody/tr[3]/td[5]/div/div[1]'
driver.find_element(By.XPATH, botao).click()

# Espera para carregar a página
time.sleep(4)

# Obtenção do conteúdo da tabela
get_url = driver.find_element(By.XPATH, '/html/body/form/div[2]/div[2]/div[1]/div/div[2]/div/section/div[2]/div[1]/div/div/div[3]/div[1]/div[3]/div[2]/div/div/div/div[3]')
conteudo_tabela = get_url.get_attribute("outerHTML")
lista = pd.read_html(conteudo_tabela, thousands=',')

# Clique no próximo botão
botao2 = '/html/body/form/div[2]/div[2]/div[1]/div/div[2]/div/section/div[2]/div[1]/div/div/div[3]/div[1]/div[3]/div[2]/div/div/div/div[3]/div/table/tbody/tr[3]/td[2]/a'
driver.find_element(By.XPATH, botao2).click()

# Espera para carregar a página
time.sleep(4)

# Obtenção do conteúdo da segunda tabela
get_url1= driver.find_element(By.XPATH, '/html/body/form/div[2]/div[2]/div[1]/div/div[2]/div/section/div[2]/div[1]/div/div/div[3]/div[3]/div[3]/div[2]/div/div/div/div[3]/div/table')
conteudo_tabela1 = get_url1.get_attribute("outerHTML")
lista_licitacoes1 = pd.read_html(conteudo_tabela1, thousands=',')

# Tratamento dos dados
df1 = pd.DataFrame(lista[0])
df1.columns = df1.iloc[0]
df1.drop(1, inplace=True)
df1['Modalidade'] = df1['Modalidade'].astype(str)
df1['Número/Processo'] = df1['Número/Processo'].astype(str)
df1['Situação'] = df1['Situação'].astype(str)
df1['Total registro de preço'] = df1['Total registro de preço'].astype(str)
df1['Valor estimado'] = df1['Valor estimado'].str.replace('\.', '', regex=True).str.replace(',', '.', regex=False)
df1['Valor estimado'] = df1['Valor estimado'].replace('000', '0')
df1['Valor comprado'] = df1['Valor comprado'].str.replace('\.', '', regex=True).str.replace(',', '.', regex=False)
df1['Valor comprado'] = df1['Valor estimado'].replace('000', '0')
df1 = df1.reset_index(drop=True)


df2 = pd.DataFrame(lista_licitacoes1[0])
df2.columns = df2.iloc[0]
df2 = df2.drop(0)
df2['Qtd Solicitada'] = df2['Qtd Solicitada'].str.replace(',', '.').replace('\.', '', regex=True).astype(float) / 100
df2['Valor Unitário'] = df2['Valor Unitário'].str.replace('\.', '', regex=True).str.replace(',', '.', regex=False).astype(float)
df2['Valor Total'] = df2['Valor Total'].str.replace('\.', '', regex=True).str.replace(',', '.', regex=False).astype(float)
df2['Descrição'] = df2['Descrição'].astype(str)
df2['Unidade'] = df2['Unidade'].astype(str)
df2['Vencedor'] = df2['Vencedor'].astype(str)
df2 = df2.reset_index(drop=True)

