import pandas as pd
import zipfile
import os
from tabula import read_pdf

def extrair_procedimentos_para_csv_zip(
    caminho_pdf: str = "Anexo_I.pdf",
    caminho_csv: str = "procedimentos.csv",
    caminho_zip: str = "Teste_Lucas_Jaensen_Daros.zip",
    paginas: str = "3-181"
):
    """
    Extrai tabelas de um PDF, processa, salva como CSV e compacta em ZIP.
    
    :param caminho_pdf: Caminho do PDF de origem.
    :param caminho_csv: Nome do arquivo CSV a ser salvo.
    :param caminho_zip: Nome do arquivo ZIP a ser gerado.
    :param paginas: Páginas do PDF a serem lidas (ex: '3-181').
    """
    print("📄 Lendo tabelas do PDF...")
    tabelas = read_pdf(caminho_pdf, pages=paginas, multiple_tables=True, lattice=True)

    print("🔗 Concatenando dados...")
    df_completo = pd.concat(tabelas, ignore_index=True)

    print("🔍 Substituindo siglas 'OD' e 'AMB'...")
    for col in df_completo.columns:
        df_completo[col] = df_completo[col].replace('OD', 'Seg. Odontológico')
        df_completo[col] = df_completo[col].replace('AMB', 'Seg. Ambulatorial')

    print("💾 Salvando CSV...")
    df_completo.to_csv(caminho_csv, index=False)

    print("📦 Compactando CSV em ZIP...")
    with zipfile.ZipFile(caminho_zip, 'w') as zipf:
        zipf.write(caminho_csv)

    print(f"✅ Arquivo ZIP gerado com sucesso: {caminho_zip}")