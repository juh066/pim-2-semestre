from flask import Flask, render_template, request, redirect, session, url_for

app = Flask(__name__)
app.secret_key = "segredo123"

# "Banco de dados" em memória (dados de exemplo)
usuarios = {
    "aluno1": {"senha": "1234", "tipo": "aluno"},
    "aluno2": {"senha": "4321", "tipo": "aluno"},
    "prof1": {"senha": "abcd", "tipo": "professor"}
}

# Notas iniciais (para já calcular média)
notas = {
    "aluno1": [8.5, 7.0, 9.0],
    "aluno2": [5.0, 6.5]
}

# Atividades iniciais
atividades = {
    "aluno1": ["Trabalho de Matemática", "Redação sobre o meio ambiente"],
    "aluno2": ["Experimento de Ciências"]
}

# -------------------------------
# ROTAS PRINCIPAIS
# -------------------------------
@app.route("/")
def home():
    if "usuario" in session:
        usuario = session["usuario"]

        # 🔒 Verifica se o usuário ainda existe no dicionário
        if usuario in usuarios:
            tipo = usuarios[usuario]["tipo"]
            return render_template("home.html", usuario=usuario, tipo=tipo)
        else:
            # Se o usuário não existir mais, limpa a sessão
            session.clear()
            return redirect(url_for("login"))

    return render_template("home.html")


# -------------------------------
# LOGIN / LOGOUT / CADASTRO
# -------------------------------

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
        else:
            usuarios[usuario] = {"senha": senha, "tipo": tipo}
            if tipo == "aluno":
                notas[usuario] = []
                atividades[usuario] = []
            return redirect(url_for("login"))

    return render_template("cadastro.html")

# -------------------------------
# ÁREA DO ALUNO
# -------------------------------

@app.route("/aluno/home")
def aluno_home():
    if "usuario" not in session or usuarios[session["usuario"]]["tipo"] != "aluno":
        return redirect(url_for("login"))
    nome = session["usuario"]
    return render_template("aluno_home.html", nome=nome)


@app.route("/aluno/atividades")
def aluno_atividades():
    if "usuario" not in session or usuarios[session["usuario"]]["tipo"] != "aluno":
        return redirect(url_for("login"))

    nome = session["usuario"]
    return render_template("aluno_atividades.html", nome=nome, atividades=atividades.get(nome, []))


@app.route("/aluno/notas")
def aluno_notas():
    if "usuario" not in session or usuarios[session["usuario"]]["tipo"] != "aluno":
        return redirect(url_for("login"))

    nome = session["usuario"]
    notas_aluno = notas.get(nome, [])
    media = round(sum(notas_aluno) / len(notas_aluno), 2) if notas_aluno else 0
    situacao = "Aprovado 🩵" if media >= 7 else "Reprovado 💔"

    return render_template(
        "aluno_notas.html",
        nome=nome,
        notas=notas_aluno,
        media=media,
        situacao=situacao
    )

# -------------------------------
# ÁREA DO PROFESSOR
# -------------------------------

@app.route("/professor/home")
def professor_home():
    if "usuario" not in session or usuarios[session["usuario"]]["tipo"] != "professor":
        return redirect(url_for("login"))
    nome = session["usuario"]
    return render_template("professor_home.html", nome=nome, alunos=notas.keys())


@app.route("/professor/notas", methods=["GET", "POST"])
def professor_notas():
    if "usuario" not in session or usuarios[session["usuario"]]["tipo"] != "professor":
        return redirect(url_for("login"))

    # Professor pode adicionar nota
    if request.method == "POST":
        aluno = request.form["aluno"]
        nota = request.form.get("nota")
        if aluno in notas and nota:
            try:
                notas[aluno].append(float(nota))
            except ValueError:
                pass  # Ignora se não for número
        elif aluno not in notas:
            notas[aluno] = [float(nota)]

    return render_template("professor_notas.html", notas=notas)


@app.route("/professor/atividades", methods=["GET", "POST"])
def professor_atividades():
    if "usuario" not in session or usuarios[session["usuario"]]["tipo"] != "professor":
        return redirect(url_for("login"))

    # Professor pode adicionar atividade
    if request.method == "POST":
        aluno = request.form["aluno"]
        atividade = request.form["atividade"]
        if aluno in atividades:
            atividades[aluno].append(atividade)
        else:
            atividades[aluno] = [atividade]

    return render_template("professor_atividades.html", atividades=atividades)

# -------------------------------
# EXECUÇÃO
# -------------------------------

if __name__ == "__main__":
    app.run(debug=True)
