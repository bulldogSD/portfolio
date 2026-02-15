"""Portfolio - Servidor Flask com API REST, Admin e Blog."""

from flask import Flask, render_template, jsonify, request, session, redirect, url_for
from datetime import datetime
from functools import wraps

app = Flask(__name__)
app.secret_key = "chave-secreta-portfolio-2026"

# === DADOS (em memória — na Etapa 5 vão pro banco) ===
projetos = [
    {
        "id": 1,
        "titulo": "Calculadora Científica",
        "descricao": "Calculadora com interface gráfica no estilo Windows, com funções científicas, memória e histórico.",
        "categoria": "Python",
        "icone": "🧮",
        "tecnologias": ["Python", "Tkinter"],
    },
    {
        "id": 2,
        "titulo": "Organizador de Arquivos",
        "descricao": "App que organiza arquivos por extensão com interface visual, preview e função desfazer.",
        "categoria": "Python",
        "icone": "📁",
        "tecnologias": ["Python", "Tkinter", "Shutil"],
    },
    {
        "id": 3,
        "titulo": "To-Do List",
        "descricao": "Gerenciador de tarefas com interface gráfica, filtros, edição inline e 14 testes automatizados.",
        "categoria": "Python",
        "icone": "✅",
        "tecnologias": ["Python", "Tkinter", "JSON"],
    },
    {
        "id": 4,
        "titulo": "Cotações de Moedas",
        "descricao": "Dashboard de cotações em tempo real com 12 moedas, abas, variação colorida e atualização assíncrona.",
        "categoria": "API",
        "icone": "💹",
        "tecnologias": ["Python", "Requests", "Threading"],
    },
    {
        "id": 5,
        "titulo": "Portfolio Pessoal",
        "descricao": "Este site! Portfolio responsivo com backend Flask, API REST, painel admin e blog.",
        "categoria": "Web",
        "icone": "🌐",
        "tecnologias": ["HTML", "CSS", "JavaScript", "Flask"],
    },
]

mensagens = []

posts = [
    {
        "id": 1,
        "titulo": "Minha jornada no desenvolvimento",
        "resumo": "Como comecei a programar e o que aprendi até aqui.",
        "conteudo": "Tudo começou com Python e um simples Hello World. De lá pra cá, já criei calculadoras, organizadores de arquivos, apps de tarefas e até um dashboard de cotações em tempo real. Agora estou mergulhando no mundo web, aprendendo HTML, CSS, JavaScript e Flask. Cada projeto me ensina algo novo e me motiva a continuar evoluindo.",
        "data": "15/02/2026",
    },
    {
        "id": 2,
        "titulo": "O que aprendi sobre APIs REST",
        "resumo": "Entendendo como frontend e backend se comunicam.",
        "conteudo": "API REST é a ponte entre o que o usuário vê (frontend) e onde os dados vivem (backend). Aprendi que GET busca dados, POST envia dados, PUT atualiza e DELETE remove. Com Flask, criar uma API é surpreendentemente simples: basta definir rotas e retornar JSON. O frontend usa fetch() para se comunicar com essas rotas.",
        "data": "15/02/2026",
    },
]

ADMIN_SENHA = "admin123"
_proximo_id_projeto = 6
_proximo_id_post = 3


def _gerar_id_projeto():
    global _proximo_id_projeto
    id_atual = _proximo_id_projeto
    _proximo_id_projeto += 1
    return id_atual


def _gerar_id_post():
    global _proximo_id_post
    id_atual = _proximo_id_post
    _proximo_id_post += 1
    return id_atual


# === AUTENTICAÇÃO ===
def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get("admin"):
            return redirect(url_for("admin_login"))
        return f(*args, **kwargs)
    return decorated


@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    erro = None
    if request.method == "POST":
        if request.form.get("senha") == ADMIN_SENHA:
            session["admin"] = True
            return redirect(url_for("admin_painel"))
        erro = "Senha incorreta."
    return render_template("login.html", erro=erro)


@app.route("/admin/logout")
def admin_logout():
    session.pop("admin", None)
    return redirect(url_for("index"))


# === ROTAS DE PÁGINA ===
@app.route("/")
def index():
    return render_template("index.html", projetos=projetos)


@app.route("/blog")
def blog():
    return render_template("blog.html", posts=posts)


@app.route("/blog/<int:post_id>")
def blog_post(post_id):
    post = next((p for p in posts if p["id"] == post_id), None)
    if not post:
        return "Post não encontrado", 404
    return render_template("blog_post.html", post=post)


@app.route("/admin")
@login_required
def admin_painel():
    return render_template(
        "admin.html",
        projetos=projetos,
        posts=posts,
        mensagens=mensagens,
    )


# === API REST: PROJETOS ===
@app.route("/api/projetos", methods=["GET"])
def api_listar_projetos():
    return jsonify(projetos)


@app.route("/api/projetos/<int:projeto_id>", methods=["GET"])
def api_obter_projeto(projeto_id):
    projeto = next((p for p in projetos if p["id"] == projeto_id), None)
    if not projeto:
        return jsonify({"erro": "Projeto não encontrado"}), 404
    return jsonify(projeto)


@app.route("/api/projetos", methods=["POST"])
@login_required
def api_criar_projeto():
    dados = request.get_json()
    novo = {
        "id": _gerar_id_projeto(),
        "titulo": dados.get("titulo", "").strip(),
        "descricao": dados.get("descricao", "").strip(),
        "categoria": dados.get("categoria", "").strip(),
        "icone": dados.get("icone", "📦").strip(),
        "tecnologias": [t.strip() for t in dados.get("tecnologias", "").split(",") if t.strip()],
    }
    if not novo["titulo"]:
        return jsonify({"erro": "Título é obrigatório"}), 400
    projetos.append(novo)
    return jsonify(novo), 201


@app.route("/api/projetos/<int:projeto_id>", methods=["PUT"])
@login_required
def api_editar_projeto(projeto_id):
    projeto = next((p for p in projetos if p["id"] == projeto_id), None)
    if not projeto:
        return jsonify({"erro": "Projeto não encontrado"}), 404

    dados = request.get_json()
    projeto["titulo"] = dados.get("titulo", projeto["titulo"]).strip()
    projeto["descricao"] = dados.get("descricao", projeto["descricao"]).strip()
    projeto["categoria"] = dados.get("categoria", projeto["categoria"]).strip()
    projeto["icone"] = dados.get("icone", projeto["icone"]).strip()
    if "tecnologias" in dados:
        projeto["tecnologias"] = [t.strip() for t in dados["tecnologias"].split(",") if t.strip()]
    return jsonify(projeto)


@app.route("/api/projetos/<int:projeto_id>", methods=["DELETE"])
@login_required
def api_deletar_projeto(projeto_id):
    global projetos
    antes = len(projetos)
    projetos = [p for p in projetos if p["id"] != projeto_id]
    if len(projetos) == antes:
        return jsonify({"erro": "Projeto não encontrado"}), 404
    return jsonify({"sucesso": True})


# === API REST: POSTS ===
@app.route("/api/posts", methods=["GET"])
def api_listar_posts():
    return jsonify(posts)


@app.route("/api/posts", methods=["POST"])
@login_required
def api_criar_post():
    dados = request.get_json()
    novo = {
        "id": _gerar_id_post(),
        "titulo": dados.get("titulo", "").strip(),
        "resumo": dados.get("resumo", "").strip(),
        "conteudo": dados.get("conteudo", "").strip(),
        "data": datetime.now().strftime("%d/%m/%Y"),
    }
    if not novo["titulo"]:
        return jsonify({"erro": "Título é obrigatório"}), 400
    posts.append(novo)
    return jsonify(novo), 201


@app.route("/api/posts/<int:post_id>", methods=["DELETE"])
@login_required
def api_deletar_post(post_id):
    global posts
    antes = len(posts)
    posts = [p for p in posts if p["id"] != post_id]
    if len(posts) == antes:
        return jsonify({"erro": "Post não encontrado"}), 404
    return jsonify({"sucesso": True})


# === API REST: CONTATO ===
@app.route("/api/contato", methods=["POST"])
def api_contato():
    dados = request.get_json()
    if not dados:
        return jsonify({"erro": "Dados inválidos"}), 400

    nome = dados.get("nome", "").strip()
    email = dados.get("email", "").strip()
    mensagem = dados.get("mensagem", "").strip()

    erros = []
    if len(nome) < 2:
        erros.append("Nome deve ter pelo menos 2 caracteres.")
    if "@" not in email:
        erros.append("Email inválido.")
    if len(mensagem) < 10:
        erros.append("Mensagem deve ter pelo menos 10 caracteres.")

    if erros:
        return jsonify({"erro": erros}), 400

    nova_mensagem = {
        "id": len(mensagens) + 1,
        "nome": nome,
        "email": email,
        "mensagem": mensagem,
        "data": datetime.now().strftime("%d/%m/%Y %H:%M"),
    }
    mensagens.append(nova_mensagem)
    print(f"[Nova mensagem] De: {nome} ({email})")
    return jsonify({"sucesso": True, "mensagem": "Mensagem recebida!"}), 201


@app.route("/api/contato", methods=["GET"])
@login_required
def api_listar_mensagens():
    return jsonify(mensagens)


@app.route("/api/contato/<int:msg_id>", methods=["DELETE"])
@login_required
def api_deletar_mensagem(msg_id):
    global mensagens
    antes = len(mensagens)
    mensagens = [m for m in mensagens if m["id"] != msg_id]
    if len(mensagens) == antes:
        return jsonify({"erro": "Mensagem não encontrada"}), 404
    return jsonify({"sucesso": True})


if __name__ == "__main__":
    print("\n  Portfolio rodando em: http://localhost:5000")
    print("  Painel admin:        http://localhost:5000/admin")
    print("  Blog:                http://localhost:5000/blog")
    print(f"  Senha admin:         {ADMIN_SENHA}\n")
    app.run(debug=True, port=5000)
