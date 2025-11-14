from flask import Flask, render_template, request, redirect, session, url_for

app = Flask(__name__)
app.secret_key = "segredo123"

# -----------------------------------------
# BANCO DE DADOS EM MEMÓRIA
# -----------------------------------------
usuarios = {
    "aluno1": {"senha": "1234", "tipo": "aluno"},
    "aluno2": {"senha": "4321", "tipo": "aluno"},
    "prof1": {"senha": "abcd", "tipo": "professor"}
}

notas = {
    "aluno1": [8.5, 7.0, 9.0],
    "aluno2": [5.0, 6.5]
}

atividades = {
    "aluno1": ["Trabalho de Matemática", "Redação sobre o meio ambiente"],
    "aluno2": ["Experimento de Ciências"]
}

questoes = [
    {
        "id": 1,
        "pergunta": "Quanto é 25 + 37?",
        "alternativas": ["52", "60", "45", "62"],
        "correta": "62"
    },
    {
        "id": 2,
        "pergunta": "Qual desses é um ecossistema?",
        "alternativas": ["Deserto", "Lápis", "Computador", "Carro"],
        "correta": "Deserto"
    },
    {
        "id": 3,
        "pergunta": "O que é fotossíntese?",
        "alternativas": [
            "Processo de respiração humana",
            "Processo em que plantas produzem alimento",
            "Tipo de rocha",
            "Movimento de placas tectônicas"
        ],
        "correta": "Processo em que plantas produzem alimento"
    }
]

# -----------------------------------------
# ROTAS PRINCIPAIS
# -----------------------------------------
@app.route("/")
def home():
    usuario = session.get("usuario")
    tipo = usuarios[usuario]["tipo"] if usuario in usuarios else None
    return render_template("home.html", usuario=usuario, tipo=tipo)

# -----------------------------------------
# LOGIN / LOGOUT / CADASTRO
# -----------------------------------------
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        usuario = request.form["usuario"]
        senha = request.form["senha"]
        if usuario in usuarios and usuarios[usuario]["senha"] == senha:
            session["usuario"] = usuario
            tipo = usuarios[usuario]["tipo"]
            return redirect(url_for(f"{tipo}_home"))
        else:
            return render_template("login.html", erro="Usuário ou senha inválidos")
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("home"))

@app.route("/cadastro", methods=["GET", "POST"])
def cadastro():
    if request.method == "POST":
        usuario = request.form["usuario"]
        senha = request.form["senha"]
        tipo = request.form["tipo"]
        if usuario in usuarios:
            return render_template("cadastro.html", erro="Usuário já existe!")
        usuarios[usuario] = {"senha": senha, "tipo": tipo}
        if tipo == "aluno":
            notas[usuario] = []
            atividades[usuario] = []
        return redirect(url_for("login"))
    return render_template("cadastro.html")

# -----------------------------------------
# ÁREA DO ALUNO
# -----------------------------------------
@app.route("/aluno/home")
def aluno_home():
    if "usuario" not in session or usuarios[session["usuario"]]["tipo"] != "aluno":
        return redirect(url_for("login"))
    nome = session["usuario"]
    return render_template("aluno_home.html", nome=nome)

@app.route("/aluno/atividades", methods=["GET", "POST"])
def aluno_atividades():
    if "usuario" not in session or usuarios[session["usuario"]]["tipo"] != "aluno":
        return redirect(url_for("login"))
    nome = session["usuario"]
    resultado = None
    nota_final = None

    if request.method == "POST":
        # Captura respostas do quiz
        pontos = 0
        for q in questoes:
            resp = request.form.get(f"questao_{q['id']}")
            if resp == q["correta"]:
                pontos += 1
        if pontos > 0:
            resultado = f"Você acertou {pontos} de {len(questoes)} perguntas!"
            nota_final = round((pontos / len(questoes)) * 10, 2)

    return render_template("aluno_atividades.html",
                           nome=nome,
                           atividades=atividades.get(nome, []),
                           questoes=questoes,
                           resultado=resultado,
                           nota_final=nota_final)

@app.route("/aluno/notas")
def aluno_notas():
    if "usuario" not in session or usuarios[session["usuario"]]["tipo"] != "aluno":
        return redirect(url_for("login"))
    nome = session["usuario"]
    notas_aluno = notas.get(nome, [])
    media = round(sum(notas_aluno) / len(notas_aluno), 2) if notas_aluno else 0
    situacao = "Aprovado 🩵" if media >= 7 else "Reprovado 💔"
    return render_template("aluno_notas.html",
                           nome=nome,
                           notas=notas_aluno,
                           media=media,
                           situacao=situacao)

# -----------------------------------------
# ÁREA DO PROFESSOR
# -----------------------------------------
@app.route("/professor/home")
def professor_home():
    if "usuario" not in session or usuarios[session["usuario"]]["tipo"] != "professor":
        return redirect(url_for("login"))
    nome = session["usuario"]
    alunos = [u for u, info in usuarios.items() if info["tipo"] == "aluno"]
    return render_template("professor_home.html", nome=nome, alunos=alunos)

@app.route("/professor/notas", methods=["GET", "POST"])
def professor_notas():
    if "usuario" not in session or usuarios[session["usuario"]]["tipo"] != "professor":
        return redirect(url_for("login"))
    if request.method == "POST":
        aluno = request.form.get("aluno")
        nota = request.form.get("nota")
        if aluno and nota:
            try:
                nota_float = float(nota)
                notas.setdefault(aluno, []).append(nota_float)
            except:
                pass
    alunos = [u for u, info in usuarios.items() if info["tipo"] == "aluno"]
    return render_template("professor_notas.html", notas=notas, alunos=alunos)

@app.route("/professor/atividades", methods=["GET", "POST"])
def professor_atividades():
    if "usuario" not in session or usuarios[session["usuario"]]["tipo"] != "professor":
        return redirect(url_for("login"))
    if request.method == "POST":
        aluno = request.form.get("aluno")
        atividade = request.form.get("atividade")
        if aluno and atividade:
            atividades.setdefault(aluno, []).append(atividade)
    alunos = [u for u, info in usuarios.items() if info["tipo"] == "aluno"]
    return render_template("professor_atividades.html", atividades=atividades, alunos=alunos)

# -----------------------------------------
# EXECUÇÃO
# -----------------------------------------
if __name__ == "__main__":
    app.run(debug=True)
