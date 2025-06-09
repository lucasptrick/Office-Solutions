# 📊 Script de Extração de Contas Coletivas (JAN/2025) - Energia Elétrica

## 📝 Descrição

Este script tem como objetivo **extrair automaticamente informações de contas de energia elétrica contidas em arquivos PDF** e gerar uma planilha Excel organizada, pronta para análise e controle. O sistema foi desenvolvido com foco em facilitar o tratamento de faturas agrupadas (conta coletiva) de múltiplas unidades consumidoras.

A aplicação lê o PDF com as contas individuais anexadas à conta coletiva, extrai apenas os dados solicitados, filtra endereços repetidos e salva o resultado em uma **planilha Excel organizada em duas abas**:

- `Contas Únicas`: registros válidos com endereços únicos.
- `Descartadas (endereços)`: registros com **endereços duplicados**, que foram ignorados da aba principal.

---

## ✅ Informações extraídas por conta

Cada conta extraída conterá as seguintes colunas:

- **Município**
- **Código da Instalação**
- **Código do Cliente**
- **Nome do Cliente**
- **CNPJ**
- **Endereço** (logradouro + número)
- **Bairro** (sem o município)
- **CEP** (ex: `00000-000`)
- **Total a Pagar (Mês/Ano)** (valor monetário da conta individual)

---

## ⚙️ Pré-requisitos

Antes de rodar o script, certifique-se de:

1. Ter o Python 3 instalado.
2. Instalar as bibliotecas necessárias com o comando abaixo:

```bash
pip install pymupdf pandas openpyxl tqdm
```

---

## ▶️ Como usar o script

1. Coloque o arquivo `.pdf` com as contas na mesma pasta do script, com o nome bem identificado (ex: `PREF MUNICIPAL - MAIO2025.pdf`).
2. Execute o script no terminal ou no VS Code:

```bash
python nome_do_arquivo.py
```

3. Ao executar, o script solicitará:

   - Seu nome (para exibição personalizada no final)
   - O nome base do arquivo PDF (sem a extensão `.pdf`)

   Exemplo:

   ```
   Olá, poderia informar seu nome:
   > @Lucasptrick_
   Digite o nome do PDF das contas:
   > PREF MUNICIPAL - MAIO2025
   ```
4. O script processará as páginas do PDF, filtrando **apenas as contas apenas as contas de um respectivo mês de um ano** (ex: `JAN25`) e salvando o resultado em:

```
Contas de Energia/MAIO2025.xlsx
```

---

## 📂 Estrutura da planilha gerada

- Aba **Contas Únicas**: contém as contas com endereços distintos.
- Aba **Descartadas (endereços)**: contém as contas ignoradas por endereço repetido (útil para revisão).

---

## 🛠 Personalizações futuras

Você pode facilmente adaptar o script para:

- Outros meses/anos (ajustando o filtro `JAN/25`)
- Outros municípios (modificando os campos fixos)
- Exportar CSVs ou logs `.txt`

---

## 👨‍💻 Autor - @lucasptrick_

Desenvolvido para automatizar e agilizar o processamento de contas públicas municipais.
Caso precise de adaptações, estou à disposição!
