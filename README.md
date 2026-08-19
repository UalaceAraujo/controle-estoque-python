# Sistema de Controle de Estoque

Sistema de linha de comando (CLI) para controle de estoque, desenvolvido em Python com banco de dados SQLite.

## Sobre o projeto

Este projeto nasceu da união entre minha experiência prática em logística e o aprendizado de Python e SQL na faculdade. A ideia foi sair do exercício isolado e construir uma ferramenta que resolve um problema real do dia a dia de um estoque: saber o que entra, o que sai, e quando é hora de repor.

## Funcionalidades

- Cadastro de produtos com quantidade inicial e quantidade mínima
- Registro de entradas e saídas, com validação de estoque insuficiente
- Listagem do estoque atual com alerta visual de itens em baixa
- Relatório dedicado de produtos abaixo da quantidade mínima
- Histórico de movimentações salvo no banco de dados

## Tecnologias

- **Python 3** — lógica do sistema
- **SQLite** (via módulo `sqlite3`, nativo do Python) — armazenamento dos dados

## Como executar

```bash
git clone https://github.com/UalaceAraujo/controle-estoque-python.git
cd controle-estoque-python
python estoque.py
```

Não é necessário instalar nenhuma dependência externa — o projeto usa apenas bibliotecas nativas do Python.

## Estrutura do banco de dados

- **produtos**: id, nome, quantidade atual, quantidade mínima
- **movimentacoes**: histórico de entradas e saídas, vinculado a cada produto

## Próximos passos

- Adicionar exportação de relatórios em CSV
- Criar interface web simples com Flask
- Adicionar testes automatizados

## Autor

Ualace Araujo — estudante de Ciência da Computação (UNIP), em transição de carreira da logística para tecnologia.
[LinkedIn](#) · [GitHub](https://github.com/UalaceAraujo)
