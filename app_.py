import time
import pandas as pd
import gspread
import getpass 
import requests

from oauth2client.service_account import ServiceAccountCredentials
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

TELEGRAM_API_KEY = os.environ["TELEGRAM_API_KEY"]
TELEGRAM_ADMIN_ID = os.environ["TELEGRAM_ADMIN_ID"]
GOOGLE_SHEETS_CREDENTIALS = os.environ["GOOGLE_SHEETS_CREDENTIALS"]
GOOGLE_CREDENTIALS_JSON = os.environ["GOOGLE_CREDENTIALS_JSON"]

nome_json = GOOGLE_CREDENTIALS_JSON
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

def adiciona_secretaria(df_teste, dici):
    secretarias = []
    for descricao in df_teste["Finalidade/Objeto/Serviço"]:
        for chave, valor in dici.items():
            if chave in descricao:
                secretarias.append(valor)
                break
        else:
            secretarias.append(None)
    df_teste["Secretaria"] = secretarias
    return df_teste
 
df_list = []

dici = {"Sma" : "Secretaria Municipal de Administração e Tecnologia",
        "Sas": "Secretaria Municipal de Assistência Social e Cidadania",
        "Sj" : "Secretaria Municipal de Assuntos Jurídicos",
        "Secom": "Secretaria Municipal de Comunicação",
        "Sec": "Secretaria Municipal de Cultura e Turismo",
        "Sde": "Secretaria Municipal de Desenvolvimento Econômico e Trabalho",
        "Sehab": "Secretaria Municipal de Desenvolvimento Urbano, Habitação e Meio Ambiente",
        "Seduc": "Secretaria Municipal de Educação",
        "Semel": "Secretaria Municipal de Esportes e Lazer",
        "Sefaz" : "Secretaria Municipal de Finanças e Planejamento",
        "Sgp": "Secretaria Municipal de Gestão de Pessoas",
        "Semugov": "Secretaria Municipal de Governo",
        "Sema": "Secretaria Municipal de Serviços Urbanos e Manutenção",
        "Smo": "Secretaria Municipal de Obras e Infraestrutura",
        "Seplan": "Secretaria Municipal de Gestão Estratégica",
        "Sms": "Secretaria Municipal de Saúde",
        "Sds": "Secretaria Municipal de Segurança e Defesa Social",
        "Setram": "Secretaria Municipal de Transportes e Mobilidade Urbana",
        "" : "Secretaria não especificada"}


for i in range (0, 233):
    
    # clica no link correspondente à tabela desejada
    link_xpath = f'/html/body/form/div[2]/div[2]/div[1]/div/div[2]/div/section/div[2]/div[1]/div/div/div[3]/div[1]/div[3]/div[2]/div/div/div/div[3]/div/table/tbody/tr[{3+i}]/td[2]/a'
    time.sleep(2)
    driver.find_element(By.XPATH, link_xpath).click()
    
    # espera 5 segundos para a tabela carregar
    time.sleep(3)
    
    # extrai o conteúdo da tabela
    tabela_xpath = '/html/body/form/div[2]/div[2]/div[1]/div/div[2]/div/section/div[2]/div[1]/div/div/div[3]/div[3]/div[3]/div[2]/div/div/div/div[3]/div/table'
    tabela_element = driver.find_element(By.XPATH, tabela_xpath)
    tabela_html = tabela_element.get_attribute("outerHTML")
    
    # converte a tabela em DataFrame
    tabela_df = pd.read_html(tabela_html, decimal=',', thousands='.')[0]

    # Cria uma nova coluna em tabela_df chamada 'Número/Processo'
    tabela_df['Número/Processo'] = df1['Número/Processo'].iloc[i+1]
    tabela_df['Modalidade'] = df1['Modalidade'].iloc[i+1]
    tabela_df['Situação'] = df1['Situação'].iloc[i+1]
    tabela_df.drop(0, inplace=True)
    
    # adiciona o DataFrame à lista
    df_list.append(tabela_df)
    
# concatena todos os DataFrames em um único DataFrame
dflicitacoes = pd.concat(df_list)
dflicitacoes.columns = ["Descrição", "Unidade", "Qtd Solicitada", "Valor Unitário", "Valor Total", "Vencedor", "Número/Processo", 'Modalidade', 'Situação']

#Faz o merge com o df1 para gerar o df_lic_final
dfs_merge = pd.merge(df1, dflicitacoes, on=['Número/Processo', 'Modalidade', 'Situação'])
dfs_merge.columns

#Limpeza e reestruturação de dados para o formato mais conveniente
df_qfinal = dfs_merge[['Número/Processo', 'Modalidade', 'Situação', 'Data', 'Finalidade/Objeto/Serviço', 'Descrição', 'Vencedor', 'Qtd Solicitada', 'Unidade', 'Valor Unitário', 'Valor Total', 'Total registro de preço', 'Valor comprado', 'Valor estimado']]
df_qfinal['Qtd Solicitada'] = df_qfinal['Qtd Solicitada'].astype(float)
df_qfinal['Valor Unitário'] = df_qfinal['Valor Unitário'].astype(float)
df_qfinal['Valor Total'] = df_qfinal['Valor Total'].astype(float)
df_qfinal['Total registro de preço'] = df_qfinal['Total registro de preço'].replace('000', '0')
df_qfinal['Valor comprado'] = df_qfinal['Valor comprado'].astype(float)
df_qfinal['Valor estimado'] = df_qfinal['Valor estimado'].astype(float)

df_final = adiciona_secretaria(df_qfinal, dici)
df_final[['Número/Processo', 'Secretaria', 'Modalidade', 'Situação', 'Data', 'Finalidade/Objeto/Serviço', 'Descrição', 'Vencedor', 'Qtd Solicitada', 'Unidade', 'Valor Unitário', 'Valor Total', 'Total registro de preço', 'Valor comprado', 'Valor estimado']]
print(df_final.columns)

# Converter o dataframe em uma lista de dicionários para inserir na planilha
dados = df_final.to_dict(orient='records')

# Obter os nomes das colunas do dataframe
nomes_colunas = list(df_final.columns)

# Criar um dicionário com as chaves sendo os nomes das colunas e os valores sendo os mesmos nomes das colunas
cabecalho = {coluna: coluna for coluna in nomes_colunas}

# Adicionar o cabeçalho como o primeiro item na lista de dados
dados.insert(0, cabecalho)

# Definir o intervalo de células que deseja atualizar com os dados
intervalo_celulas = f'A1:{chr(ord("A") + len(df_final.columns) - 1)}{len(df_final.index) + 1}'

# Atualizar as células na planilha com os dados do dataframe
sheet.clear()
sheet.update(intervalo_celulas, [list(d.values()) for d in dados])

