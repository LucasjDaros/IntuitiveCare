# 🧠 Descrição do Projeto – IntuitiveCare

Este projeto tem como objetivo automatizar o processo de:

- **Raspagem de dados da ANS** (Agência Nacional de Saúde Suplementar), baixando os anexos em PDF disponíveis no site oficial.
- **Extração e transformação de dados** dos PDFs em CSV, com tratamento e substituição de siglas específicas.
- **Importação de dados** para um banco de dados PostgreSQL com estrutura definida para as tabelas contábeis e operadoras.
- **Empacotamento dos resultados** em arquivos `.zip` para distribuição ou arquivamento.
- **Execução de testes unitários** com `pytest`.

---

## 🚀 Tecnologias Utilizadas

- **Python 3.11+**
- **Bibliotecas**: `pandas`, `sqlalchemy`, `tabula-py`, `jpype1`, `requests`, `bs4`, `python-dotenv`
- **Banco de Dados**: PostgreSQL
- **Ambiente**: WSL (recomendado para Linux-like experience)
- **Docker** (opcional para isolar o ambiente)

---

## 🧰 Ambiente Recomendado

### ✅ WSL (Windows Subsystem for Linux)

- **Motivo**: Compatibilidade com `tabula-py`, Java, estrutura de diretórios Linux e maior estabilidade com bibliotecas que dependem de Java.

---

## 🛠 Como Rodar o Projeto

### 📁 1. Clone o Projeto

```bash
git clone https://github.com/seu-usuario/intuitivecare.git
cd intuitivecare
```

### 📦 2. Crie e Ative o Ambiente Virtual

#### WSL/Linux:

```bash
python3 -m venv venv
source venv/bin/activate
```

#### Windows (PowerShell):

```bash
python -m venv venv
.\venv\Scripts\activate
```

### 📄 3. Instale as Dependências

```bash
pip install -r requirements.txt
```

⚠ **Se estiver no WSL e aparecer erro de `externally-managed-environment`, use:**

```bash
pip install --break-system-packages -r requirements.txt
```

### ☕ 4. Instale o Java (Obrigatório para `tabula-py`)

```bash
sudo apt update
sudo apt install default-jre -y
```

Verifique a instalação com:

```bash
java -version
```

### 🗄 5. Configure seu Arquivo `.env`

Crie um arquivo `.env` com as credenciais do banco:

```env
DB_USUARIO=postgres
DB_SENHA=postgres
DB_HOST=localhost
DB_PORTA=5432
DB_NOME=postgres
```

### ▶ 6. Execute o Projeto

```bash
python3 main.py
```

Isso irá:

- Baixar os anexos da ANS.
- Extrair os dados do PDF.
- Salvar um CSV com os dados tratados.
- Gerar um `.zip` com o CSV.
- Inserir os dados no banco PostgreSQL.

---

## 🧪 Executar os Testes com `pytest`

1. Verifique se o ambiente virtual está ativado.
2. No terminal, dentro do projeto, execute:

```bash
pytest
```

Os testes estão organizados na pasta `/tests` e cobrem os módulos de raspagem, extração e inserção no banco (com SQLite em memória para simulação).

---

## 🐳 (Opcional) Usar Docker

Se preferir usar Docker:

1. Crie um `Dockerfile` para Python + Java + PostgreSQL client.
2. Monte a imagem e execute com `docker-compose`.

Se quiser, posso gerar um `Dockerfile` pronto para você.

---

## ✅ Conclusão

Este projeto pode ser executado tanto no WSL/Linux quanto no Windows, porém o uso de WSL é altamente recomendado por conta da compatibilidade com bibliotecas que exigem Java (como `tabula-py`).

Se precisar de ajuda para:

- Criar um `Dockerfile`
- Criar um `Makefile`
- Automatizar testes ou deploy
