# Contribuindo com o BioRitmo

Obrigado por querer contribuir! 🎉 Este guia explica como colaborar com o projeto.

---

## 🚀 Como contribuir

### 1. Fork e clone

```bash
git clone https://github.com/seu-usuario/biorritmo.git
cd biorritmo
```

### 2. Crie uma branch

Use o padrão `tipo/descricao-curta`:

```bash
git checkout -b feat/exportacao-csv
git checkout -b fix/calculo-balanco
git checkout -b docs/atualizar-readme
```

### 3. Configure o ambiente

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 4. Faça suas alterações

Siga os padrões de código descritos abaixo.

### 5. Execute lint e testes

```bash
ruff check app/
pytest app/tests/ -v
```

### 6. Commit

Use **Conventional Commits**:

```
feat: adiciona exportação de dados em CSV
fix: corrige cálculo de saldo calórico negativo
docs: atualiza instruções de instalação
test: adiciona teste para peso limite superior
refactor: extrai lógica de filtro para service
```

### 7. Pull Request

Abra um PR descrevendo:
- O que foi feito
- Por que foi feito
- Como testar

---

## 📐 Padrões de Código

### Python (Back-end)

- **Formatação:** Ruff (linha máx. 120 chars)
- **Docstrings:** obrigatórias em funções públicas
- **Tipagem:** use type hints em todas as funções
- **Testes:** novos endpoints devem ter testes correspondentes
- **Imports:** organizados (stdlib → third-party → local)

```python
# ✅ Correto
def get_meal(db: Session, meal_id: int) -> Optional[Meal]:
    """Get a single meal by ID."""
    return db.query(Meal).filter(Meal.id == meal_id).first()

# ❌ Evitar
def get_meal(db, id):
    return db.query(Meal).filter(Meal.id == id).first()
```

### JavaScript (Front-end)

- **ES Modules** — use `import/export`, sem globals desnecessários
- **Async/await** — preferido a `.then()`
- **Sem frameworks** — Vanilla JS apenas
- **Comentários** — em português ou inglês, consistentemente

---

## 🧪 Testes

Cada novo endpoint ou serviço deve ter no mínimo:

1. **Cenário válido** — fluxo feliz
2. **Cenário inválido** — dado errado ou ID inexistente
3. **Caso limite** — valor no extremo do domínio

---

## 🐛 Reportando Bugs

Abra uma **Issue** com:

- Versão do Python e sistema operacional
- Passos para reproduzir
- Comportamento esperado vs. atual
- Logs de erro (se houver)

---

## 💡 Sugestões

Abra uma **Issue** com a label `enhancement` descrevendo:

- O problema que resolve
- Como você imagina a solução
- Exemplos de uso

---

## 📄 Licença

Ao contribuir, você concorda que suas contribuições serão licenciadas sob a [MIT License](LICENSE).
