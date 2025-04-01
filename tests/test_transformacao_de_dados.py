from transformação_de_dados import extrair_procedimentos_para_csv_zip
import os

def test_csv_zip_gerados():
    extrair_procedimentos_para_csv_zip()
    assert os.path.exists("procedimentos.csv")
    assert os.path.exists("Teste_Lucas_Jaensen_Daros.zip")