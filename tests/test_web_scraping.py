from web_sraping import baixar_anexos_ans
import os

def test_baixar_anexos_cria_zip():
    baixar_anexos_ans(pasta_destino=".")
    assert os.path.exists("Anexos.zip")