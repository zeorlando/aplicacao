from datetime import datetime
from string import Template
import requests
import pandas as pd
import streamlit as st
import os
import json

# === CONFIGURAÇÕES INICIAIS === #
ano_vigente = datetime.now().year
ano_anterior = ano_vigente - 1
hora = datetime.now().hour
saudacao = ['Bom dia', 'Boa tarde']

# === CAMINHOS DE CONFIGURAÇÃO === #
caminho_srv = os.path.join('config', 'path.txt')
token_path = os.path.join('config', 'token.txt')
caminho_msg = os.path.join('config', 'mensagem.txt')
caminho_dic = os.path.join('.', 'dicionario.xlsx')
url_com_anexo = "https://api.classapp.com.br/v1/message-file"

# === LÊ CAMINHO DO SERVIDOR === #
with open(caminho_srv, 'r') as file:
    path_server = file.read().strip()

holerites_base = os.path.join(path_server, 'RH', 'HOLERITES')

# === LÊ TOKEN DE AUTENTICAÇÃO === #
try:
    with open(token_path, 'r') as token_file:
        ler_token = token_file.read().strip()
except IOError:
    st.warning('Arquivo de token não encontrado!')
    st.stop()

headers_com_anexo = {
    "Authorization": f"Bearer {ler_token}"
}

# === DICIONÁRIO DE MESES === #
dic_meses = {
    'JANEIRO': '01', 'FEVEREIRO': '02', 'MARÇO': '03', 'ABRIL': '04',
    'MAIO': '05', 'JUNHO': '06', 'JULHO': '07', 'AGOSTO': '08',
    'SETEMBRO': '09', 'OUTUBRO': '10', 'NOVEMBRO': '11', 'DEZEMBRO': '12'
}

# === INTERFACE STREAMLIT === #
empresa = st.selectbox('Escolha a empresa', ('INFANTIL', 'ETAPA 1', 'ETAPA 2'))
mes = st.selectbox('Escolha o mês do holerite', tuple(dic_meses.keys()))

# === MONTAGEM DO CAMINHO DOS HOLERITES === #
caminho = os.path.join(holerites_base, f"{mes}_{empresa}")
arquivos = []

try:
    arquivos = os.listdir(caminho)
except FileNotFoundError:
    st.warning('Você escolheu um mês que não tem arquivo de holerite. 😠')
    st.stop()

# === TÍTULO DA MENSAGEM === #
ano_do_titulo = ano_anterior if dic_meses[mes] == '12' else ano_vigente
titulo = f"Holerite {dic_meses[mes]}/{ano_do_titulo}"

# === CORPO DA MENSAGEM === #
with open(caminho_msg, 'r', encoding='utf-8') as msg_corpo:
    ler_msg_corpo = msg_corpo.read()

def gera_mensagem(horario):
    expressao = saudacao[1] if horario > 12 else saudacao[0]
    return Template(ler_msg_corpo).substitute(mes=mes, expressao=expressao)

st.markdown('<br><p>Selecione o funcionário que deseja enviar o holerite</p>', unsafe_allow_html=True)

# === SELEÇÃO DE FUNCIONÁRIOS === #
seleciona_tudo = st.checkbox('Selecionar todos')
selecionados = arquivos if seleciona_tudo else []
selecao = st.multiselect('Escolha o(s) funcionário(s)', arquivos, default=selecionados)
enviar = st.button('Enviar')

# === DICIONÁRIO DE EIDs === #
d = pd.read_excel(caminho_dic, sheet_name='holerite', index_col=0, header=None).transpose().to_dict('records')[0]
dicionario_filtrado = {nome: eid for nome, eid in d.items() if nome in selecao}

# === FUNÇÕES AUXILIARES === #
def anexo(arquivo_nome):
    return [("files", (arquivo_nome, open(os.path.join(caminho, arquivo_nome), "rb"), "application/pdf"))]

def gera_metadata(arquivo_nome):
    return {
        "metadata": json.dumps({
            "messageData": {
                "subject": titulo,
                "content": gera_mensagem(hora),
                "type": "comunicado",
                "noReply": True,
                "recipients": {
                    "eids": [dicionario_filtrado[arquivo_nome]]
                }
            }
        })
    }

def envia_msg(arquivo_nome):
    st.write(f"Enviando: {arquivo_nome}")
    try:
        resposta = requests.post(
            url_com_anexo,
            headers=headers_com_anexo,
            data=gera_metadata(arquivo_nome),
            files=anexo(arquivo_nome)
        )
        st.write(f"Status: {resposta.status_code}")
    except Exception as e:
        st.error(f"Erro ao enviar {arquivo_nome}: {e}")

# === ENVIO === #
if enviar:
    for funcionario in selecao:
        if funcionario not in dicionario_filtrado:
            st.warning(f"EID não encontrado para {funcionario}")
            continue
        envia_msg(funcionario)
