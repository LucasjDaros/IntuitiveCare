import pandas as pd
from sqlalchemy import create_engine
import os

def importar_csvs_contabeis_para_postgres(pasta_csvs: str, engine) -> None:
    """
    Lê todos os CSVs de uma pasta e importa os dados para a tabela 'contabeis' no PostgreSQL.
    :param pasta_csvs: Caminho da pasta com os arquivos CSV.
    :param engine: Engine SQLAlchemy com conexão ativa ao PostgreSQL.
    """
    for arquivo in os.listdir(pasta_csvs):
        if arquivo.lower().endswith('.csv'):
            caminho_csv = os.path.join(pasta_csvs, arquivo)
            print(f"📂 Lendo arquivo: {arquivo}")

            try:
                df = pd.read_csv(caminho_csv, sep=';', encoding='latin1')

                df.rename(columns={
                    'DATA': 'data_registro',
                    'REG_ANS': 'reg_ans',
                    'CD_CONTA_CONTABIL': 'cd_contabeis',
                    'DESCRICAO': 'descricao',
                    'VL_SALDO_INICIAL': 'vl_saldo_inicial',
                    'VL_SALDO_FINAL': 'vl_saldo_final'
                }, inplace=True)

                df['vl_saldo_inicial'] = df['vl_saldo_inicial'].astype(str).str.replace(',', '.').astype(float)
                df['vl_saldo_final'] = df['vl_saldo_final'].astype(str).str.replace(',', '.').astype(float)
                df['descricao'] = df['descricao'].apply(
                    lambda x: x.encode('latin1').decode('utf-8') if isinstance(x, str) else x
                )

                df.to_sql("contabeis", engine, if_exists="append", index=False)
                print(f"✅ Dados de '{arquivo}' inseridos com sucesso.")

            except Exception as e:
                print(f"❌ Erro ao processar '{arquivo}': {e}")

    print("\n🏁 Importação de contábeis finalizada.")

def importar_operadoras_para_postgres(caminho_csv: str, engine) -> None:
    """
    Lê o CSV com dados das operadoras e importa para o PostgreSQL.
    :param caminho_csv: Caminho do arquivo CSV.
    :param engine: Engine SQLAlchemy com conexão ativa ao PostgreSQL.
    """
    try:
        df = pd.read_csv(caminho_csv, sep=';', encoding='latin1')
        df['Data_Registro_ANS'] = pd.to_datetime(df['Data_Registro_ANS'], errors='coerce', dayfirst=True)

        df.columns = [
            'registro_ans', 'cnpj', 'razao_social', 'nome_fantasia', 'modalidade',
            'logradouro', 'numero', 'complemento', 'bairro', 'cidade', 'uf', 'cep',
            'ddd', 'telefone', 'fax', 'endereco_eletronico', 'representante',
            'cargo_representante', 'regiao_de_comercializacao', 'data_registro_ans'
        ]

        for col in df.select_dtypes(include='object').columns:
            df[col] = df[col].apply(
                lambda x: x.encode('latin1').decode('utf-8') if isinstance(x, str) else x
            )

        df.to_sql("operadoras", engine, if_exists="append", index=False)
        print("✅ Dados importados com sucesso para a tabela 'operadoras'.")

    except Exception as e:
        print(f"❌ Erro ao importar operadoras: {e}")

