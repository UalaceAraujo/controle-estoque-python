"""
Sistema de Controle de Estoque
Autor: Ualace Araujo

Projeto criado para aplicar conceitos de Python e SQL em um problema real
da área de logística: controlar entrada e saída de produtos em um estoque.

Como usar:
    python estoque.py
"""

import sqlite3
from datetime import datetime

NOME_BANCO = "estoque.db"


def conectar():
    """Abre uma conexão com o banco de dados SQLite."""
    return sqlite3.connect(NOME_BANCO)


def criar_tabelas():
    """Cria as tabelas do banco de dados, caso ainda não existam."""
    conexao = conectar()
    cursor = conexao.cursor()

    # Tabela de produtos: cada produto tem um nome, quantidade atual
    # e uma quantidade mínima (para alertar quando o estoque está baixo)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS produtos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL UNIQUE,
            quantidade INTEGER NOT NULL DEFAULT 0,
            quantidade_minima INTEGER NOT NULL DEFAULT 0
        )
    """)

    # Tabela de movimentações: registra cada entrada ou saída de produto,
    # funcionando como um histórico do estoque
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS movimentacoes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            produto_id INTEGER NOT NULL,
            tipo TEXT NOT NULL CHECK (tipo IN ('entrada', 'saida')),
            quantidade INTEGER NOT NULL,
            data TEXT NOT NULL,
            FOREIGN KEY (produto_id) REFERENCES produtos (id)
        )
    """)

    conexao.commit()
    conexao.close()


def cadastrar_produto():
    """Cadastra um novo produto no estoque."""
    nome = input("Nome do produto: ").strip()
    try:
        quantidade_inicial = int(input("Quantidade inicial: "))
        quantidade_minima = int(input("Quantidade mínima (alerta de estoque baixo): "))
    except ValueError:
        print("Erro: digite apenas números para as quantidades.\n")
        return

    conexao = conectar()
    cursor = conexao.cursor()
    try:
        cursor.execute(
            "INSERT INTO produtos (nome, quantidade, quantidade_minima) VALUES (?, ?, ?)",
            (nome, quantidade_inicial, quantidade_minima)
        )
        conexao.commit()
        print(f"Produto '{nome}' cadastrado com sucesso.\n")
    except sqlite3.IntegrityError:
        print(f"Erro: já existe um produto chamado '{nome}'.\n")
    finally:
        conexao.close()


def buscar_produto_por_nome(cursor, nome):
    """Busca um produto pelo nome e retorna seus dados, ou None se não existir."""
    cursor.execute("SELECT id, nome, quantidade FROM produtos WHERE nome = ?", (nome,))
    return cursor.fetchone()


def registrar_movimentacao(tipo):
    """Registra uma entrada ou saída de produto no estoque.

    tipo: 'entrada' ou 'saida'
    """
    nome = input("Nome do produto: ").strip()
    try:
        quantidade = int(input(f"Quantidade de {tipo}: "))
    except ValueError:
        print("Erro: digite apenas números para a quantidade.\n")
        return

    conexao = conectar()
    cursor = conexao.cursor()

    produto = buscar_produto_por_nome(cursor, nome)
    if produto is None:
        print(f"Erro: produto '{nome}' não encontrado. Cadastre-o primeiro.\n")
        conexao.close()
        return

    produto_id, produto_nome, quantidade_atual = produto

    if tipo == "saida" and quantidade > quantidade_atual:
        print(f"Erro: estoque insuficiente. Quantidade atual de '{produto_nome}': {quantidade_atual}.\n")
        conexao.close()
        return

    nova_quantidade = quantidade_atual + quantidade if tipo == "entrada" else quantidade_atual - quantidade

    cursor.execute("UPDATE produtos SET quantidade = ? WHERE id = ?", (nova_quantidade, produto_id))
    cursor.execute(
        "INSERT INTO movimentacoes (produto_id, tipo, quantidade, data) VALUES (?, ?, ?, ?)",
        (produto_id, tipo, quantidade, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    )
    conexao.commit()
    conexao.close()

    print(f"{tipo.capitalize()} registrada. Novo estoque de '{produto_nome}': {nova_quantidade}\n")


def listar_produtos():
    """Lista todos os produtos cadastrados e sinaliza estoque baixo."""
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("SELECT nome, quantidade, quantidade_minima FROM produtos ORDER BY nome")
    produtos = cursor.fetchall()
    conexao.close()

    if not produtos:
        print("Nenhum produto cadastrado ainda.\n")
        return

    print("\n--- Estoque Atual ---")
    for nome, quantidade, quantidade_minima in produtos:
        alerta = " ⚠ ESTOQUE BAIXO" if quantidade <= quantidade_minima else ""
        print(f"{nome}: {quantidade} unidades{alerta}")
    print()


def relatorio_estoque_baixo():
    """Mostra apenas os produtos que estão com estoque igual ou abaixo do mínimo."""
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("""
        SELECT nome, quantidade, quantidade_minima
        FROM produtos
        WHERE quantidade <= quantidade_minima
        ORDER BY quantidade ASC
    """)
    produtos = cursor.fetchall()
    conexao.close()

    if not produtos:
        print("Nenhum produto com estoque baixo no momento.\n")
        return

    print("\n--- Alerta: Produtos com Estoque Baixo ---")
    for nome, quantidade, quantidade_minima in produtos:
        print(f"{nome}: {quantidade} unidades (mínimo recomendado: {quantidade_minima})")
    print()


def menu():
    """Exibe o menu principal e direciona para a função escolhida."""
    opcoes = {
        "1": cadastrar_produto,
        "2": lambda: registrar_movimentacao("entrada"),
        "3": lambda: registrar_movimentacao("saida"),
        "4": listar_produtos,
        "5": relatorio_estoque_baixo,
    }

    while True:
        print("=== Sistema de Controle de Estoque ===")
        print("1 - Cadastrar produto")
        print("2 - Registrar entrada")
        print("3 - Registrar saída")
        print("4 - Listar estoque")
        print("5 - Relatório de estoque baixo")
        print("0 - Sair")

        escolha = input("Escolha uma opção: ").strip()

        if escolha == "0":
            print("Encerrando o sistema. Até logo!")
            break

        acao = opcoes.get(escolha)
        if acao:
            acao()
        else:
            print("Opção inválida. Tente novamente.\n")


if __name__ == "__main__":
    criar_tabelas()
    menu()
