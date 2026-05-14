# Changelog

Todas as mudanças notáveis deste projeto serão documentadas neste arquivo.

O formato segue [Keep a Changelog](https://keepachangelog.com/pt-BR/1.0.0/),
e este projeto adere ao [Versionamento Semântico](https://semver.org/lang/pt-BR/).

---

## [1.0.0] — 2024-01-01

### ✨ Adicionado

#### Back-end
- API REST completa com **FastAPI**
- CRUD de refeições (`/api/v1/meals/`)
- CRUD de exercícios (`/api/v1/exercises/`)
- CRUD de registros de peso (`/api/v1/weight/`)
- Endpoint de resumo diário (`/api/v1/dashboard/summary`)
- Modelos SQLAlchemy: `Meal`, `Exercise`, `WeightLog`
- Schemas Pydantic com validação completa
- Camada de serviços separada da camada de rotas
- Banco de dados SQLite com inicialização automática
- Filtro por data em todos os endpoints de listagem
- CORS configurado para desenvolvimento local
- Tratamento de erros com status HTTP corretos (404, 422, etc.)

#### Front-end
- SPA com navegação lateral (sidebar) sem recarregamento
- Dashboard com 4 cards de métricas
- Barra de progresso animada de hidratação
- Gráfico de evolução de peso em **Canvas puro** (sem bibliotecas)
- Modal de criação/edição para todos os módulos
- Tabelas de dados com ações de editar e deletar
- Filtro por data em todas as listagens
- Sistema de notificações toast (sucesso, erro, aviso, info)
- Diálogo de confirmação antes de deletar
- Loading states com spinner animado
- Estado vazio (empty state) quando não há dados
- Responsividade completa (mobile/tablet/desktop)
- Dark theme moderno com CSS custom properties

#### Qualidade
- 13 testes automatizados com **pytest**
- Linting com **Ruff**
- Pipeline CI com **GitHub Actions**
- Documentação: README, CHANGELOG, CONTRIBUTING, LICENSE

---

## [Não publicado]

### Planejado para versões futuras

- Autenticação de usuários (JWT)
- Metas calóricas personalizadas por usuário
- Exportação de dados em CSV/PDF
- Notificações de hidratação
- Integração com APIs de alimentos (TACO/USDA)
- PWA (Progressive Web App) com suporte offline
- Tema claro (light mode)
- Internacionalização (i18n)
