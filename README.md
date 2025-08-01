
# 💼 Envio Automatizado de Holerites via ClassApp

Este projeto desenvolvido com **Python** e **Streamlit** automatiza **duas etapas fundamentais** do processo de envio de holerites digitais:

1. **Separação automática dos holerites individuais a partir de um único PDF** (enviado pela contabilidade);
2. **Envio individual dos holerites via API da ClassApp**, com autenticação por token e mensagem personalizada.

---

## 🚀 Funcionalidades

### 1. Separação dos Holerites por Funcionário

- Interface interativa para o envio de **um único arquivo PDF** contendo todos os holerites do mês.
- O script analisa o conteúdo de cada página, extrai o **nome do funcionário** e salva cada holerite individualmente.
- Os arquivos são salvos automaticamente em uma pasta nomeada com o padrão:  
  **RH/HOLERITES/[MÊS]_[EMPRESA]/**

### 2. Envio Automatizado via API ClassApp

- Interface intuitiva com seleção de **empresa**, **mês** e **funcionários** a serem enviados.
- Leitura do holerite correspondente e envio com título personalizado (ex: `Holerite 07/2025`) e saudação (Bom dia / Boa tarde).
- Envio de mensagens via **API da ClassApp**, com metadados estruturados e autenticação via token.
- Permite o envio em lote ou individual, com exibição do status de cada envio.

---

## Estrutura

```
aplicacao/
├── config/
│   ├── path.txt         # Caminho base dos holerites
│   ├── token.txt        # Token de autenticação da API
│   └── mensagem.txt     # Corpo da mensagem com placeholders ($mes, $expressao)
├── pages/
│   ├── 1 - Separar.py   # Página onde há as funcionalidades para separar os holerites
│   └── 2 - Enviar.py    # Página responsável pelo envio dos holerites
├── dicionario.xlsx      # Dicionário com os nomes e respectivos EIDs
├── home.py              # Página inicial
```

---

## Lógica de Funcionamento

### Etapa 1 – Separação dos PDFs
1. O usuário seleciona o mês e a empresa;
2. Faz o upload do arquivo PDF enviado pela contabilidade;
3. Cada página é analisada para localizar o nome do funcionário;
4. Cada holerite é salvo com nome correto em PDF individual.

### Etapa 2 – Envio dos Holerites
1. O usuário escolhe a empresa e o mês desejado;
2. A aplicação lista os holerites disponíveis para seleção;
3. O dicionário de EIDs é carregado a partir de um arquivo Excel;
4. O sistema gera mensagens personalizadas e realiza o envio via API ClassApp.

---

## Tecnologias Utilizadas

- Python 3
- Streamlit
- PyPDF2
- Pandas
- Requests
- API ClassApp

---

## Pré-requisitos

- Python 3.8+
- Token de acesso válido da ClassApp (`token.txt`)
- Acesso ao diretório de rede onde os holerites serão armazenados
- Arquivo Excel (`dicionario.xlsx`) contendo os nomes dos funcionários e seus respectivos EIDs
- Modelo de mensagem (`mensagem.txt`) com os placeholders `$mes` e `$expressao`

---

## Observações

- O nome do funcionário é extraído automaticamente a partir do conteúdo de cada página do PDF, com base na ocorrência das palavras **"FUNCIONÁRIO"**, **"RECIBO"** ou **"DEMONSTRATIVO"**.
- Se o mês selecionado for **dezembro**, o ano exibido no título será ajustado para o ano anterior.
- Em caso de erro na extração ou envio, o sistema alerta o usuário diretamente na interface.

## Autor
Este projeto foi desenvolvido por José Orlando de Queiroz.