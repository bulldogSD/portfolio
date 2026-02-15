"""Portfolio - Servidor Flask com SQLite, Admin e Blog."""

from flask import Flask, render_template, jsonify, request, session, redirect, url_for
from functools import wraps
import database as db

app = Flask(__name__)
app.secret_key = "chave-secreta-portfolio-2026"

ADMIN_SENHA = "admin123"

# Inicializa o banco de dados
db.inicializar()


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
    db.registrar_visita("/")
    projetos = db.listar_projetos()
    return render_template("index.html", projetos=projetos)


@app.route("/blog")
def blog():
    db.registrar_visita("/blog")
    posts = db.listar_posts()
    return render_template("blog.html", posts=posts)


@app.route("/blog/<int:post_id>")
def blog_post(post_id):
    db.registrar_visita(f"/blog/{post_id}")
    post = db.obter_post(post_id)
    if not post:
        return "Post não encontrado", 404
    return render_template("blog_post.html", post=post)


@app.route("/admin")
@login_required
def admin_painel():
    return render_template(
        "admin.html",
        projetos=db.listar_projetos(),
        posts=db.listar_posts(),
        mensagens=db.listar_mensagens(),
        stats=db.estatisticas(),
    )


# === API REST: PROJETOS ===
@app.route("/api/projetos", methods=["GET"])
def api_listar_projetos():
    return jsonify(db.listar_projetos())


@app.route("/api/projetos/<int:projeto_id>", methods=["GET"])
def api_obter_projeto(projeto_id):
    projeto = db.obter_projeto(projeto_id)
    if not projeto:
        return jsonify({"erro": "Projeto não encontrado"}), 404
    return jsonify(projeto)


@app.route("/api/projetos", methods=["POST"])
@login_required
def api_criar_projeto():
    dados = request.get_json()
    titulo = dados.get("titulo", "").strip()
    if not titulo:
        return jsonify({"erro": "Título é obrigatório"}), 400

    projeto = db.criar_projeto(
        titulo=titulo,
        descricao=dados.get("descricao", "").strip(),
        categoria=dados.get("categoria", "").strip(),
        icone=dados.get("icone", "📦").strip(),
        tecnologias=dados.get("tecnologias", "").strip(),
    )
    return jsonify(projeto), 201


@app.route("/api/projetos/<int:projeto_id>", methods=["PUT"])
@login_required
def api_editar_projeto(projeto_id):
    projeto = db.obter_projeto(projeto_id)
    if not projeto:
        return jsonify({"erro": "Projeto não encontrado"}), 404

    dados = request.get_json()
    atualizado = db.editar_projeto(
        projeto_id,
        titulo=dados.get("titulo", projeto["titulo"]).strip(),
        descricao=dados.get("descricao", projeto["descricao"]).strip(),
        categoria=dados.get("categoria", projeto["categoria"]).strip(),
        icone=dados.get("icone", projeto["icone"]).strip(),
        tecnologias=dados.get("tecnologias", ",".join(projeto["tecnologias"])).strip(),
    )
    return jsonify(atualizado)


@app.route("/api/projetos/<int:projeto_id>", methods=["DELETE"])
@login_required
def api_deletar_projeto(projeto_id):
    if not db.deletar_projeto(projeto_id):
        return jsonify({"erro": "Projeto não encontrado"}), 404
    return jsonify({"sucesso": True})


# === API REST: POSTS ===
@app.route("/api/posts", methods=["GET"])
def api_listar_posts():
    return jsonify(db.listar_posts())


@app.route("/api/posts", methods=["POST"])
@login_required
def api_criar_post():
    dados = request.get_json()
    titulo = dados.get("titulo", "").strip()
    if not titulo:
        return jsonify({"erro": "Título é obrigatório"}), 400

    post = db.criar_post(
        titulo=titulo,
        resumo=dados.get("resumo", "").strip(),
        conteudo=dados.get("conteudo", "").strip(),
    )
    return jsonify(post), 201


@app.route("/api/posts/<int:post_id>", methods=["DELETE"])
@login_required
def api_deletar_post(post_id):
    if not db.deletar_post(post_id):
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

    nova = db.criar_mensagem(nome, email, mensagem)
    print(f"[Nova mensagem] De: {nome} ({email})")
    return jsonify({"sucesso": True, "mensagem": "Mensagem recebida!"}), 201


@app.route("/api/contato", methods=["GET"])
@login_required
def api_listar_mensagens():
    return jsonify(db.listar_mensagens())


@app.route("/api/contato/<int:msg_id>", methods=["DELETE"])
@login_required
def api_deletar_mensagem(msg_id):
    if not db.deletar_mensagem(msg_id):
        return jsonify({"erro": "Mensagem não encontrada"}), 404
    return jsonify({"sucesso": True})


# === API: ESTATÍSTICAS ===
@app.route("/api/stats", methods=["GET"])
@login_required
def api_stats():
    return jsonify(db.estatisticas())


if __name__ == "__main__":
    print("\n  Portfolio rodando em: http://localhost:5000")
    print("  Painel admin:        http://localhost:5000/admin")
    print("  Blog:                http://localhost:5000/blog")
    print(f"  Senha admin:         {ADMIN_SENHA}\n")
    app.run(debug=True, port=5000)
