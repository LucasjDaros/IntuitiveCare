import pandas as pd
import os
from sqlalchemy import create_engine
from teste_banco import importar_csvs_contabeis_para_postgres, importar_operadoras_para_postgres
from dotenv import load_dotenv

load_dotenv()

# Captura os dados de acesso
usuario = os.getenv("DB_USUARIO")
senha = os.getenv("DB_SENHA")
host = os.getenv("DB_HOST")
porta = os.getenv("DB_PORTA")
banco = os.getenv("DB_NOME")

# Cria a conexão com o banco
engine = create_engine(f"postgresql://{usuario}:{senha}@{host}:{porta}/{banco}")

def test_importar_csvs_contabeis():
    engine = create_engine(f"postgresql://{usuario}:{senha}@{host}:{porta}/{banco}")
    pasta_csv = "./tests/mocks/contabeis"

    os.makedirs(pasta_csv, exist_ok=True)

    with open(os.path.join(pasta_csv, "exemplo.csv"), "w", encoding="latin1") as f:
        f.write("DATA;REG_ANS;CD_CONTA_CONTABIL;DESCRICAO;VL_SALDO_INICIAL;VL_SALDO_FINAL\n")
        f.write("01/01/2024;123;456;teste;1000,00;2000,00\n")

    importar_csvs_contabeis_para_postgres(pasta_csv, engine)
    df = pd.read_sql("contabeis", engine)
    assert not df.empty

def test_importar_operadoras():
    engine = create_engine(f"postgresql://{usuario}:{senha}@{host}:{porta}/{banco}")
    path = "./tests/mocks/operadoras.csv"

    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="latin1") as f:
        f.write("Registro_ANS;CNPJ;Razao_Social;Nome_Fantasia;Modalidade;Logradouro;Numero;Complemento;Bairro;Cidade;UF;CEP;DDD;Telefone;Fax;Endereco_Eletronico;Representante;Cargo_Representante;Regiao_de_Comercializacao;Data_Registro_ANS\n")
        f.write("123456;00.000.000/0001-00;Razão X;Fantasia Y;Cooperativa;Rua X;100;;Centro;Cidade Z;SP;00000-000;11;999999999;;email@exemplo.com;Fulano;Diretor;Sudeste;01/01/2024\n")

    importar_operadoras_para_postgres(path, engine)
    df = pd.read_sql("operadoras", engine)
    assert not df.empty