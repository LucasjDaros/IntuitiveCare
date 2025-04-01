import requests
from bs4 import BeautifulSoup
from zipfile import ZipFile
import os

def baixar_anexos_ans(
    url: str = "https://www.gov.br/ans/pt-br/acesso-a-informacao/participacao-da-sociedade/atualizacao-do-rol-de-procedimentos",
    pasta_destino: str = "."
) -> None:
    """
    Acessa o site da ANS, extrai os links dos PDFs 'Anexo I' e 'Anexo II',
    baixa os arquivos e os compacta em um arquivo ZIP.

    :param url: URL da página com os anexos.
    :param pasta_destino: Caminho onde os arquivos serão salvos (padrão: diretório atual).
    """
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")
        body_content = soup.find("body")

        with open(os.path.join(pasta_destino, "ans_body_content.html"), "w", encoding="utf-8") as file:
            file.write(str(body_content))

        print("✅ HTML salvo com sucesso.")

        link_pdf1 = None
        link_pdf2 = None

        for a in soup.find_all('a', href=True):
            href = a['href']
            if not href.endswith('.pdf'):
                continue

            if 'Anexo_I' in href and link_pdf1 is None:
                link_pdf1 = href
            if 'Anexo_II' in href and link_pdf2 is None:
                link_pdf2 = href

            if link_pdf1 and link_pdf2:
                break

        def baixar_pdf(link, nome_arquivo):
            if not link.startswith('http'):
                link = "https://www.gov.br" + link
            print(f"🔗 Link encontrado: {link}")
            pdf_response = requests.get(link)
            caminho_arquivo = os.path.join(pasta_destino, nome_arquivo)
            with open(caminho_arquivo, 'wb') as f:
                f.write(pdf_response.content)
            print(f"✅ PDF baixado: {nome_arquivo}")
            return caminho_arquivo

        arquivos_baixados = []
        if link_pdf1:
            arquivos_baixados.append(baixar_pdf(link_pdf1, "Anexo_I.pdf"))
        else:
            print("❌ Link do Anexo I não encontrado.")

        if link_pdf2:
            arquivos_baixados.append(baixar_pdf(link_pdf2, "Anexo_II.pdf"))
        else:
            print("❌ Link do Anexo II não encontrado.")

        if arquivos_baixados:
            zip_path = os.path.join(pasta_destino, "Anexos.zip")
            with ZipFile(zip_path, 'w') as zipf:
                for arquivo in arquivos_baixados:
                    zipf.write(arquivo, arcname=os.path.basename(arquivo))
            print(f"✅ Arquivo ZIP criado: {zip_path}")
        else:
            print("⚠️ Nenhum PDF foi baixado. ZIP não criado.")

    except requests.exceptions.RequestException as e:
        print(f"❌ Erro ao acessar o site: {e}")
