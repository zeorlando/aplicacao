from selenium import webdriver
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains


import pandas as pd
import streamlit as st
import os

import time


empresas = st.selectbox('Escolha a empresa',
    ('INFANTIL', 'ETAPA 1', 'ETAPA 2'))
meses = st.selectbox('Escolha o mês do holerite',('JANEIRO', 'FEVEREIRO', 'MARÇO', 'ABRIL', 'MAIO', 'JUNHO',
         'JULHO', 'AGOSTO', 'SETEMBRO', 'OUTUBRO', 'NOVEMBRO', 'DEZEMBRO'))
telefone = st.text_input('Celular (DDD + Celular)')
senha = st.text_input('Senha', type='password')

titulo_msg = st.text_input('Informe o título da Msg do ClassApp')
mensagem = st.text_area('Coloque aqui a sua mensagem')
mensagem = mensagem.splitlines()


caminho = '\\\srv-xingu\\RH\\HOLERITES\\' + meses + '_' + empresas + '\\'
arquivos = ''

try:
    arquivos = os.listdir(caminho)
except FileNotFoundError:
    st.warning('Você escolheu um mês que não tem arquivo de holerite :rage:')


st.html('<br><p>Selecione o funcionário que deseja enviar o holerite</p>')

seleciona_tudo = st.checkbox('Seleciona todos')


if seleciona_tudo:
    selecionados = arquivos
else:
    selecionados = []
selecao = st.multiselect('Escolha o funcionário', arquivos, default=selecionados)

enviar = st.button('Enviar')

#dicionário contendo a relação entre nome do arquivo PDF e o usuário do ClassApp
d = pd.read_excel('.\dicionario.xlsx', sheet_name = 'holerite',index_col=0,header=None).transpose().to_dict('records')[0]

###

if enviar:
    #browser = webdriver.Firefox()
    servico = Service(GeckoDriverManager().install())
    browser = webdriver.Firefox(service=servico)
    endereco = 'https://classapp.com.br/entities/1234725272/'
    browser.get(endereco)
    #browser.implicitly_wait(10)

    #tentar implementar 
    wait = WebDriverWait(browser, 10)

    
    celular = wait.until(
        EC.element_to_be_clickable(
            (By.XPATH, '//div[text()[contains(., "ou entre usando o celular")]]')
        )
    )
    celular.click()
    inserir_celular = browser.find_element(By.XPATH, '//input[@placeholder = "DDD + Celular"]')
    inserir_celular.send_keys(telefone)
    
    continuar = wait.until(
    EC.element_to_be_clickable(
            (By.XPATH, '//button[text()[contains(., "Continuar")]]')
        )
    )
    continuar.click()
    
    inserir_senha = wait.until(
    EC.visibility_of_element_located(
            (By.XPATH, '//input[@placeholder = "Digite aqui sua senha"]')
            )
    )
    inserir_senha.send_keys(senha)
    
    entrar = browser.find_element(By.XPATH, '//button[text()[contains(., "Entrar")]]')
    entrar.click()


    if not wait.until(EC.url_to_be('https://classapp.com.br/entities/1234725272/')):

        celular = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, '//div[text()[contains(., "ou entre usando o celular")]]')
            )
        )
        celular.click()
        inserir_celular = browser.find_element(By.XPATH, '//input[@placeholder = "DDD + Celular"]')
        inserir_celular.send_keys(telefone)
        
        continuar = wait.until(
        EC.element_to_be_clickable(
                (By.XPATH, '//button[text()[contains(., "Continuar")]]')
            )
        )
        continuar.click()
        
        inserir_senha = wait.until(
        EC.visibility_of_element_located(
                (By.XPATH, '//input[@placeholder = "Digite aqui sua senha"]')
                )
        )
        inserir_senha.send_keys(senha)
        
        entrar = browser.find_element(By.XPATH, '//button[text()[contains(., "Entrar")]]')
        entrar.click()

    else:
        
    #    fechar_popup = wait.until(
    #        EC.element_to_be_clickable(
    #            (By.CSS_SELECTOR, 'svg[data-testid*="close"]')
    #        )
    #    )
    #    fechar_popup.click()
        for nome in selecao:
            browser.refresh()
            escrever = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, '//span[text()[contains(., "Escrever")]]')
                )
            )
            escrever.click()
            

            escolher_destinatario = wait.until(
                EC.element_to_be_clickable(
                    (By.CSS_SELECTOR, 'div.fluid:nth-child(1) > div:nth-child(3)')
                )
            )
            ActionChains(browser).click(escolher_destinatario).send_keys(d[nome]).perform()
            selecionar_nome = wait.until(
                EC.element_to_be_clickable(
                    (By.CLASS_NAME, 'item.text')
                )
            )
            selecionar_nome.click()

            msg_titulo = wait.until(
                EC.element_to_be_clickable(
                    (By.XPATH, '//input[@placeholder =  "Assunto"]')
                )
            )
            msg_titulo.send_keys(
                titulo_msg
            )

            msg = wait.until(
                EC.element_to_be_clickable(
                    (By.CSS_SELECTOR, '.ql-editor')
                )
            )

            for linha in mensagem:
                msg.send_keys(
                    linha + Keys.ENTER
                )
            caminho_pdf = caminho+nome
            escolher_arquivo = browser.find_element(By.CSS_SELECTOR, 'input[type="file"]')
            escolher_arquivo.send_keys(caminho_pdf)

            time.sleep(5)

            enviar_msg = wait.until(
                EC.element_to_be_clickable(
                    (By.XPATH, '//button[text()[contains(., "Enviar")]]')
                )
            )
            enviar_msg.click()
            time.sleep(5)
    browser.close()