import fitz  # PyMuPDF
import pandas as pd
from tqdm import tqdm
import re


import fitz  # PyMuPDF
import re
from tqdm import tqdm

def extrair_info_contas(pdf_path, mes_referencia, ano_referencia=None):
    doc = fitz.open(pdf_path)
    contas_validas = []
    contas_descartadas = []
    enderecos_unicos = set()
    CNPJ_FIXO = "CNPJ DA PREFEITURA DO MUNICÍPIO EM QUESTÃO"
    MUNICIPIO_FIXO = "NOME DO MUNICÍPIO"

    # Garantir que o mês tenha dois dígitos (ex: 04)
    mes_referencia = mes_referencia.zfill(2)

    print(f"Lendo PDF: {pdf_path}")
    for pagina in tqdm(doc, desc="Processando páginas"):
        texto = pagina.get_text()

        # === FILTRO PELO MÊS E ANO DE LEITURA ATUAL ===
        leitura_match = re.search(r"LEITURA ATUAL\s*(\d{2})/(\d{2})/(\d{4})", texto)
        if not leitura_match:
            continue  # Se não encontrar a data, ignora

        dia, mes, ano = leitura_match.groups()
        if mes != mes_referencia:
            continue  # Mês não bate

        if ano_referencia and ano != ano_referencia:
            continue  # Ano não bate

        # Extrações
        cod_instalacao = re.search(r"CÓDIGO DA INSTALAÇÃO\s*[\n:]?\s*(\d+)", texto, re.IGNORECASE)
        cod_cliente = re.search(r"CÓDIGO DO CLIENTE\s*[\n:]?\s*(\d+)", texto, re.IGNORECASE)
        nome_cliente_match = re.search(r"NOME DO CLIENTE\s*:?[\n]?\s*(PREF[^\n]+)", texto, re.IGNORECASE)
        nome_cliente = nome_cliente_match.group(1).strip() if nome_cliente_match else ""

        endereco_match = re.search(r"ENDEREÇO\s*:?[\n]?\s*(.+)", texto, re.IGNORECASE)
        endereco_raw = endereco_match.group(1).strip() if endereco_match else ""
        endereco_linha = endereco_raw.split('\n')[0].strip().upper()

        bairro_match = re.search(r"\n([A-ZÇ ]+?)/AGUA PRETA", texto, re.IGNORECASE)
        bairro = bairro_match.group(1).strip().upper() if bairro_match else ""

        cep_match = re.search(r"(\d{5}-?\d{3})\s+AGUA PRETA", texto, re.IGNORECASE)
        cep = cep_match.group(1).strip() if cep_match else "INSIRA O CEP DO MUNICÍPIO"

        total_a_pagar = re.search(r"TOTAL A PAGAR\s*R?\$?\s*([\d.,]+)", texto.upper())

        conta_info = {
            "Município": MUNICIPIO_FIXO,
            "Código da Instalação": cod_instalacao.group(1) if cod_instalacao else "",
            "Código do Cliente": cod_cliente.group(1) if cod_cliente else "",
            "Nome do Cliente": nome_cliente,
            "CNPJ": CNPJ_FIXO,
            "Endereço": endereco_linha,
            "Bairro": bairro,
            "CEP": cep,
            f"Total a Pagar ({mes}/{ano})": total_a_pagar.group(1).replace(',', '.') if total_a_pagar else ""
        }

        if not endereco_linha:
            continue

        if endereco_linha in enderecos_unicos:
            contas_descartadas.append(conta_info)
            continue

        enderecos_unicos.add(endereco_linha)
        contas_validas.append(conta_info)

    doc.close()
    return contas_validas, contas_descartadas


def salvar_excel(dados_validos, dados_descartados, caminho_saida, usuario):
    with pd.ExcelWriter(caminho_saida, engine="openpyxl") as writer:
        pd.DataFrame(dados_validos).to_excel(writer, index=False, sheet_name="Contas Únicas")
        pd.DataFrame(dados_descartados).to_excel(writer, index=False, sheet_name="Descartadas (endereços)")
    print(f"\nOlá, sr(a) {usuario} seu processo foi finalizado!")
    print(f"📄 Contas válidas: {len(dados_validos)}")
    print(f"❌ Contas descartadas por endereço duplicado: {len(dados_descartados)}")
    print(f"📁 Arquivo Excel salvo como: {caminho_saida}")


# Execução principal
if __name__ == "__main__":
    usuario = input(f"Olá, poderia informar seu nome:\n> ")
    urlPDF = input(f"Digite o nome do PDF das contas:\n>")
    mesPDF = input(f"Digite o MÊS para o filtro de busca:\n>")
    
    caminho_pdf = urlPDF+'.pdf'
    caminho_excel = "INFORME O NOME DO ARQUIVO QUE SERÁ CRIAR .xlsx" 

    contas_validas, contas_descartadas = extrair_info_contas(caminho_pdf, mesPDF)
    salvar_excel(contas_validas, contas_descartadas, caminho_excel, usuario)