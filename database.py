"""Banco de dados SQLite para o Portfolio."""

import sqlite3
from datetime import datetime

DB_PATH = "portfolio.db"


def _conectar():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def inicializar():
    """Cria as tabelas se não existirem e insere dados iniciais."""
    conn = _conectar()

    conn.executescript("""
        CREATE TABLE IF NOT EXISTS projetos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            descricao TEXT DEFAULT '',
            categoria TEXT DEFAULT '',
            icone TEXT DEFAULT '📦',
            tecnologias TEXT DEFAULT ''
        );

        CREATE TABLE IF NOT EXISTS posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            resumo TEXT DEFAULT '',
            conteudo TEXT DEFAULT '',
            data TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS mensagens (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            email TEXT NOT NULL,
            mensagem TEXT NOT NULL,
            data TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS visitas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            pagina TEXT NOT NULL,
            data TEXT NOT NULL
        );
    """)

    # Insere dados iniciais se tabela estiver vazia
    if conn.execute("SELECT COUNT(*) FROM projetos").fetchone()[0] == 0:
        projetos_iniciais = [
            ("Calculadora Científica", "Calculadora com interface gráfica no estilo Windows, com funções científicas, memória e histórico.", "Python", "🧮", "Python,Tkinter"),
            ("Organizador de Arquivos", "App que organiza arquivos por extensão com interface visual, preview e função desfazer.", "Python", "📁", "Python,Tkinter,Shutil"),
            ("To-Do List", "Gerenciador de tarefas com interface gráfica, filtros, edição inline e 14 testes automatizados.", "Python", "✅", "Python,Tkinter,JSON"),
            ("Cotações de Moedas", "Dashboard de cotações em tempo real com 12 moedas, abas, variação colorida e atualização assíncrona.", "API", "💹", "Python,Requests,Threading"),
            ("Portfolio Pessoal", "Este site! Portfolio completo com Flask, SQLite, painel admin e blog.", "Web", "🌐", "HTML,CSS,JavaScript,Flask,SQLite"),
        ]
        conn.executemany(
            "INSERT INTO projetos (titulo, descricao, categoria, icone, tecnologias) VALUES (?, ?, ?, ?, ?)",
            projetos_iniciais
        )

    if conn.execute("SELECT COUNT(*) FROM posts").fetchone()[0] == 0:
        posts_iniciais = [
            ("Minha jornada no desenvolvimento", "Como comecei a programar e o que aprendi até aqui.",
             "Tudo começou com Python e um simples Hello World. De lá pra cá, já criei calculadoras, organizadores de arquivos, apps de tarefas e até um dashboard de cotações em tempo real. Agora estou mergulhando no mundo web, aprendendo HTML, CSS, JavaScript e Flask. Cada projeto me ensina algo novo e me motiva a continuar evoluindo.",
             "15/02/2026"),
            ("O que aprendi sobre APIs REST", "Entendendo como frontend e backend se comunicam.",
             "API REST é a ponte entre o que o usuário vê (frontend) e onde os dados vivem (backend). Aprendi que GET busca dados, POST envia dados, PUT atualiza e DELETE remove. Com Flask, criar uma API é surpreendentemente simples: basta definir rotas e retornar JSON. O frontend usa fetch() para se comunicar com essas rotas.",
             "15/02/2026"),
        ]
        conn.executemany(
            "INSERT INTO posts (titulo, resumo, conteudo, data) VALUES (?, ?, ?, ?)",
            posts_iniciais
        )

    conn.commit()
    conn.close()


def _row_to_dict(row):
    return dict(row) if row else None


def _rows_to_list(rows):
    return [dict(r) for r in rows]


# === PROJETOS ===
def listar_projetos():
    conn = _conectar()
    rows = conn.execute("SELECT * FROM projetos ORDER BY id").fetchall()
    conn.close()
    resultado = _rows_to_list(rows)
    for p in resultado:
        p["tecnologias"] = [t.strip() for t in p["tecnologias"].split(",") if t.strip()]
    return resultado


def obter_projeto(projeto_id):
    conn = _conectar()
    row = conn.execute("SELECT * FROM projetos WHERE id = ?", (projeto_id,)).fetchone()
    conn.close()
    if not row:
        return None
    p = _row_to_dict(row)
    p["tecnologias"] = [t.strip() for t in p["tecnologias"].split(",") if t.strip()]
    return p


def criar_projeto(titulo, descricao, categoria, icone, tecnologias):
    conn = _conectar()
    cursor = conn.execute(
        "INSERT INTO projetos (titulo, descricao, categoria, icone, tecnologias) VALUES (?, ?, ?, ?, ?)",
        (titulo, descricao, categoria, icone, tecnologias)
    )
    conn.commit()
    projeto_id = cursor.lastrowid
    conn.close()
    return obter_projeto(projeto_id)


def editar_projeto(projeto_id, titulo, descricao, categoria, icone, tecnologias):
    conn = _conectar()
    conn.execute(
        "UPDATE projetos SET titulo=?, descricao=?, categoria=?, icone=?, tecnologias=? WHERE id=?",
        (titulo, descricao, categoria, icone, tecnologias, projeto_id)
    )
    conn.commit()
    conn.close()
    return obter_projeto(projeto_id)


def deletar_projeto(projeto_id):
    conn = _conectar()
    cursor = conn.execute("DELETE FROM projetos WHERE id = ?", (projeto_id,))
    conn.commit()
    conn.close()
    return cursor.rowcount > 0


# === POSTS ===
def listar_posts():
    conn = _conectar()
    rows = conn.execute("SELECT * FROM posts ORDER BY id DESC").fetchall()
    conn.close()
    return _rows_to_list(rows)


def obter_post(post_id):
    conn = _conectar()
    row = conn.execute("SELECT * FROM posts WHERE id = ?", (post_id,)).fetchone()
    conn.close()
    return _row_to_dict(row)


def criar_post(titulo, resumo, conteudo):
    conn = _conectar()
    data = datetime.now().strftime("%d/%m/%Y")
    cursor = conn.execute(
        "INSERT INTO posts (titulo, resumo, conteudo, data) VALUES (?, ?, ?, ?)",
        (titulo, resumo, conteudo, data)
    )
    conn.commit()
    post_id = cursor.lastrowid
    conn.close()
    return obter_post(post_id)


def deletar_post(post_id):
    conn = _conectar()
    cursor = conn.execute("DELETE FROM posts WHERE id = ?", (post_id,))
    conn.commit()
    conn.close()
    return cursor.rowcount > 0


# === MENSAGENS ===
def listar_mensagens():
    conn = _conectar()
    rows = conn.execute("SELECT * FROM mensagens ORDER BY id DESC").fetchall()
    conn.close()
    return _rows_to_list(rows)


def criar_mensagem(nome, email, mensagem):
    conn = _conectar()
    data = datetime.now().strftime("%d/%m/%Y %H:%M")
    cursor = conn.execute(
        "INSERT INTO mensagens (nome, email, mensagem, data) VALUES (?, ?, ?, ?)",
        (nome, email, mensagem, data)
    )
    conn.commit()
    msg_id = cursor.lastrowid
    conn.close()
    return {"id": msg_id, "nome": nome, "email": email, "mensagem": mensagem, "data": data}


def deletar_mensagem(msg_id):
    conn = _conectar()
    cursor = conn.execute("DELETE FROM mensagens WHERE id = ?", (msg_id,))
    conn.commit()
    conn.close()
    return cursor.rowcount > 0


# === VISITAS ===
def registrar_visita(pagina):
    conn = _conectar()
    data = datetime.now().strftime("%d/%m/%Y %H:%M")
    conn.execute("INSERT INTO visitas (pagina, data) VALUES (?, ?)", (pagina, data))
    conn.commit()
    conn.close()


def contar_visitas():
    conn = _conectar()
    total = conn.execute("SELECT COUNT(*) FROM visitas").fetchone()[0]
    conn.close()
    return total


def estatisticas():
    conn = _conectar()
    stats = {
        "projetos": conn.execute("SELECT COUNT(*) FROM projetos").fetchone()[0],
        "posts": conn.execute("SELECT COUNT(*) FROM posts").fetchone()[0],
        "mensagens": conn.execute("SELECT COUNT(*) FROM mensagens").fetchone()[0],
        "visitas": conn.execute("SELECT COUNT(*) FROM visitas").fetchone()[0],
    }
    conn.close()
    return stats
