import os
import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine

# Funções do projeto (certifique-se que os nomes dos arquivos batem com os módulos!)
from web_sraping import baixar_anexos_ans
from transformação_de_dados import extrair_procedimentos_para_csv_zip
from teste_banco import importar_operadoras_para_postgres, importar_csvs_contabeis_para_postgres

# Carrega variáveis do .env
load_dotenv()

# Captura os dados de acesso
usuario = os.getenv("DB_USUARIO")
senha = os.getenv("DB_SENHA")
host = os.getenv("DB_HOST")
porta = os.getenv("DB_PORTA")
banco = os.getenv("DB_NOME")

# Cria a conexão com o banco
engine = create_engine(f"postgresql://{usuario}:{senha}@{host}:{porta}/{banco}")


def main():
    print("📥 Baixando anexos da ANS...")
    baixar_anexos_ans()

    print("🧠 Processando PDF e gerando CSV...")
    extrair_procedimentos_para_csv_zip()

    # Ajuste os caminhos para seu ambiente Ubuntu:
    pasta_contabeis = "./dados/1T2024"
    csv_operadoras = "./dados/Relatorio_cadop.csv"

    print("📊 Importando contábeis...")
    importar_csvs_contabeis_para_postgres(pasta_contabeis, engine)

    print("📑 Importando operadoras...")
    importar_operadoras_para_postgres(csv_operadoras, engine)

    print("🏁 Processo completo.")


if __name__ == "__main__":
    main()
