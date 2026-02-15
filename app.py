"""Portfolio - Servidor Flask com API REST."""

from flask import Flask, render_template, jsonify, request
from datetime import datetime

app = Flask(__name__)

# === DADOS (por enquanto em memória — na Etapa 5 vão pro banco) ===
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
        "descricao": "Este site! Portfolio responsivo com backend Flask, API REST e tema claro/escuro.",
        "categoria": "Web",
        "icone": "🌐",
        "tecnologias": ["HTML", "CSS", "JavaScript", "Flask"],
    },
]

mensagens = []


# === ROTAS DE PÁGINA ===
@app.route("/")
def index():
    return render_template("index.html", projetos=projetos)


# === API REST: PROJETOS ===
@app.route("/api/projetos", methods=["GET"])
def api_listar_projetos():
    """Retorna todos os projetos."""
    return jsonify(projetos)


@app.route("/api/projetos/<int:projeto_id>", methods=["GET"])
def api_obter_projeto(projeto_id):
    """Retorna um projeto por ID."""
    projeto = next((p for p in projetos if p["id"] == projeto_id), None)
    if not projeto:
        return jsonify({"erro": "Projeto não encontrado"}), 404
    return jsonify(projeto)


# === API REST: CONTATO ===
@app.route("/api/contato", methods=["POST"])
def api_contato():
    """Recebe uma mensagem de contato."""
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
def api_listar_mensagens():
    """Lista todas as mensagens recebidas."""
    return jsonify(mensagens)


if __name__ == "__main__":
    print("\n  Portfolio rodando em: http://localhost:5000\n")
    app.run(debug=True, port=5000)
