import streamlit as st
import PyPDF2
import os

from PyPDF2 import PdfReader, PdfFileWriter

caminho_srv = os.path.join('config','path.txt')

with open (caminho_srv) as file:
    path_server = file.read()

destino = os.path.join(path_server, 'RH', 'HOLERITES','')

empresas = st.selectbox('Escolha a empresa',
    ('INFANTIL', 'ETAPA 1', 'ETAPA 2'))
meses = st.selectbox('Escolha o mês do holerite',('JANEIRO', 'FEVEREIRO', 'MARÇO', 'ABRIL', 'MAIO', 'JUNHO',
         'JULHO', 'AGOSTO', 'SETEMBRO', 'OUTUBRO', 'NOVEMBRO', 'DEZEMBRO'))


filepdf = st.file_uploader('Escolha o arquivo', type='pdf')

destino_holerites = destino + meses + "_" + empresas

if filepdf:
    pdf_reader = PyPDF2.PdfReader(filepdf)
    os.mkdir(destino_holerites)
    for page_num in range(pdf_reader.numPages):
        pdfWriter = PdfFileWriter()
        pdfWriter.addPage(pdf_reader.getPage(page_num))

        reader = PyPDF2.PdfFileReader(filepdf)
        page = reader.getPage(page_num)
        conteudo = page.extractText()
        comeco = conteudo.find('FUNCIONÁRIO')
        fim = conteudo.find('RECIBO')
        fim2 = conteudo.find('DEMONSTRATIVO')
        if conteudo[fim] ==  'R':
            nome_funcionario = (conteudo[comeco:fim])
            nome_do_funcionario_corrigido = nome_funcionario[13:]
        else:
            nome_funcionario = (conteudo[comeco:fim2])
            nome_do_funcionario_corrigido = nome_funcionario[13:]
        with open(os.path.join(destino_holerites, '{0}.pdf'.format(nome_do_funcionario_corrigido)), 'wb') as f:
            pdfWriter.write(f)
            f.close()