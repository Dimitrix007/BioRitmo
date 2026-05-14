# 💚 BioRitmo

[![CI](https://github.com/Dimitrix007/BioRitmo/actions/workflows/ci.yml/badge.svg)](https://github.com/Dimitrix007/BioRitmo/actions/workflows/ci.yml)
[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![SQLite](https://img.shields.io/badge/SQLite-3-003B57?logo=sqlite&logoColor=white)](https://sqlite.org)
[![Ruff](https://img.shields.io/badge/lint-Ruff-D7FF64?logo=ruff&logoColor=black)](https://docs.astral.sh/ruff/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Version](https://img.shields.io/badge/version-1.0.0-blue)](VERSION)

> **Plataforma pessoal de gestão de saúde** focada em balanço calórico, hidratação, monitoramento de hábitos e acompanhamento de peso corporal.

---

# 📋 Descrição do Problema

Manter hábitos saudáveis é difícil sem visibilidade. A maioria das pessoas não sabe:

- Quantas calorias consome por dia
- Quanto queima em exercícios
- Se está bebendo água suficiente
- Como seu peso evolui ao longo do tempo

Sem dados, não há decisões conscientes.

---

# 💡 Solução Proposta

O **BioRitmo** centraliza o registro diário de saúde em uma interface limpa e moderna, exibindo:

- **Balanço calórico automático** — calorias consumidas vs. queimadas
- **Hidratação com barra de progresso** — meta diária de 2 litros
- **Gráfico de evolução do peso** — feito em Canvas puro, sem bibliotecas
- **CRUD completo** para refeições, exercícios e registros de peso

---

# 👥 Público-Alvo

Pessoas que querem acompanhar sua saúde de forma simples, sem depender de apps complexos ou assinaturas pagas.

---

# ✨ Funcionalidades

| Módulo | Funcionalidades |
|---|---|
| 🍽️ **Refeições** | Registrar, editar, deletar e filtrar refeições por data |
| 🏋️ **Exercícios** | CRUD completo com calorias queimadas e duração |
| ⚖️ **Peso** | Histórico de peso com tendência (↑ ↓ =) e gráfico |
| 📊 **Dashboard** | Saldo calórico, hidratação, cards resumo e gráfico de peso |
| 💧 **Hidratação** | Meta diária com barra animada e progresso em % |
| 🔔 **UX** | Toasts, loading states, confirmação antes de deletar |

---

# 🛠️ Tecnologias

## Back-end
- **Python 3.11+**
- **FastAPI** — framework REST moderno e assíncrono
- **SQLAlchemy** — ORM para mapeamento objeto-relacional
- **Pydantic v2** — validação e serialização de dados
- **SQLite** — banco de dados embutido, sem configuração
- **Uvicorn** — servidor ASGI de alta performance

## Front-end
- **HTML5** semântico
- **CSS3** com variáveis, animações e responsividade
- **JavaScript (ES Modules)** — Vanilla JS puro, sem frameworks

## Dev / Qualidade
- **Pytest** — testes automatizados
- **Ruff** — linter e formatter ultrarrápido
- **GitHub Actions** — CI/CD automatizado

---

# 📁 Estrutura de Pastas

```txt
BioRitmo/
│
├── backend/
│   ├── app/
│   │   ├── routes/
│   │   ├── models/
│   │   ├── schemas/
│   │   ├── services/
│   │   ├── database/
│   │   ├── tests/
│   │   └── main.py
│   │
│   ├── requirements.txt
│   └── pyproject.toml
│
├── frontend/
│   ├── index.html
│   ├── css/
│   │   └── style.css
│   └── js/
│       ├── app.js
│       ├── api.js
│       ├── ui.js
│       ├── chart.js
│       ├── dashboard.js
│       ├── meals.js
│       ├── exercises.js
│       └── weight.js
│
├── .github/
│   └── workflows/
│       └── ci.yml
│
├── README.md
├── CHANGELOG.md
├── CONTRIBUTING.md
├── LICENSE
└── VERSION
```

---

# 🚀 Instalação e Execução

## 📌 Pré-requisitos

- Python 3.11 ou superior
- Git instalado
- VS Code recomendado
- Extensão Live Server ou Live Preview

---

# 🔽 1. Clonar o repositório

```bash
git clone https://github.com/Dimitrix007/BioRitmo.git
```

---

# 📂 2. Entrar na pasta do projeto

```bash
cd BioRitmo
```

---

# ⚙️ 3. Criar ambiente virtual

```bash
python -m venv venv
```

---

# ▶️ 4. Ativar ambiente virtual

## Windows PowerShell

```powershell
.\venv\Scripts\Activate.ps1
```

---

# 📦 5. Instalar dependências do backend

```bash
pip install fastapi uvicorn sqlalchemy pydantic pytest httpx ruff
```

---

# 🔥 6. Entrar na pasta backend

```bash
cd backend
```

---

# 🚀 7. Rodar o backend

```bash
python -m uvicorn app.main:app --reload
```

---

# 🌐 8. Acessar API

## Swagger

```txt
http://127.0.0.1:8000/docs
```

## API

```txt
http://127.0.0.1:8000
```

---

# 🎨 9. Rodar o frontend

Abra outro terminal sem fechar o backend.

Volte para a raiz do projeto:

```bash
cd ..
```

Entre na pasta frontend:

```bash
cd frontend
```

---

# 🖥️ 10. Abrir frontend

Abra o arquivo:

```txt
index.html
```

com:

- Open with Live Server
ou
- Open with Live Preview

---

# 🌍 11. Acessar frontend

Exemplo:

```txt
http://127.0.0.1:3001/frontend/index.html
```

---

# 🧪 Testes Automatizados

Dentro da pasta backend:

```bash
pytest
```

---

# 🔍 Linting / Análise Estática

```bash
ruff check .
```

## Correção automática

```bash
ruff check . --fix
```

---

# 📡 Endpoints da API

| Método | Endpoint | Descrição |
|---|---|---|
| `GET` | `/api/v1/meals/` | Listar refeições |
| `POST` | `/api/v1/meals/` | Criar refeição |
| `GET` | `/api/v1/meals/{id}` | Buscar refeição |
| `PUT` | `/api/v1/meals/{id}` | Atualizar refeição |
| `DELETE` | `/api/v1/meals/{id}` | Deletar refeição |
| `GET` | `/api/v1/exercises/` | Listar exercícios |
| `POST` | `/api/v1/exercises/` | Criar exercício |
| `PUT` | `/api/v1/exercises/{id}` | Atualizar exercício |
| `DELETE` | `/api/v1/exercises/{id}` | Deletar exercício |
| `GET` | `/api/v1/weight/` | Listar registros de peso |
| `POST` | `/api/v1/weight/` | Criar registro de peso |
| `PUT` | `/api/v1/weight/{id}` | Atualizar registro |
| `DELETE` | `/api/v1/weight/{id}` | Deletar registro |
| `GET` | `/api/v1/dashboard/summary` | Resumo diário |

---

# 🔄 Integração Contínua

O projeto utiliza GitHub Actions para:

- executar testes automatizados;
- verificar linting;
- validar qualidade do código automaticamente.

---

# 📦 Versionamento

Versão atual:

```txt
1.0.0
```

Padrão utilizado:

- MAJOR.MINOR.PATCH

---

# 👤 Autor

Desenvolvido por **Marcos André Camargo Belo**

GitHub:
[Dimitrix007 GitHub](https://github.com/Dimitrix007?utm_source=chatgpt.com)

---

# 🔗 Repositório Público

[BioRitmo Repository](https://github.com/Dimitrix007/BioRitmo?utm_source=chatgpt.com)

---

# 📄 Licença

Este projeto está licenciado sob a [MIT License](LICENSE).