# Projeto TODO — Backend Assíncrono com FastAPI

Este projeto implementa uma API TODO moderna utilizando um stack atual e robusto, com foco em performance, testes, qualidade de código e ambiente totalmente reproduzível.

## 🚀 Tecnologias Utilizadas

- **FastAPI (async)**
- **Pytest** (com cobertura e testes assíncronos)
- **PEP8 Linting**
- **Formatter (Black/Isort)**
- **Docker & Docker Compose**
- **Coverage**
- **Alembic** (migrações)
- **Poetry** (gerenciamento de dependências)

---

## 📦 Requisitos Mínimos

- **Docker**
- **Poetry**

Clone o repositório:

git clone <https://github.com/ClaudioFritzen/FAST_API_ASYNC>
cd FAST_API_ASYNC


##  🔧 Instalação das Dependências

- **poetry install**

## 🔐 Variáveis de Ambiente
Crie um arquivo .env baseado no .env copy.

## ▶️ Executando o Projeto

- **poetry run task run**

Outros comandos úteis podem ser encontrados no pyproject.toml.

## 🧪 Testes e Cobertura
Rodar testes:
- **poetry run task test**

## Gerar relatório de cobertura:
- **poetry run task cov**
O relatório HTML será gerado em htmlcov/.

### Rate Limit  
    # link de inspiração: https://dev.to/rotirotirafa/como-limitar-e-proteger-suas-apis-com-rate-limit-2n5p

🔗 Links Úteis
Pytest warnings
https://docs.pytest.org/en/stable/how-to/capture-warnings.html

Testcontainers deprecated decorator
https://github.com/testcontainers/testcontainers-python

asyncio WindowsSelectorEventLoopPolicy
https://docs.python.org/3/library/asyncio-policy.html

Pytest cache warnings
https://docs.pytest.org/en/stable/how-to/capture-warnings.html