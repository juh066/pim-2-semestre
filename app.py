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

        # Verifica se o usuário ainda existe no dicionário
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
        usuario = request.form.get("usuario", "").strip()
        senha = request.form.get("senha", "")

        # Validação básica
        if not usuario or not senha:
            return render_template("login.html", erro="Preencha todos os campos")

        if usuario in usuarios and usuarios[usuario]["senha"] == senha:
            session["usuario"] = usuario
            tipo = usuarios[usuario]["tipo"]
            # Corrigido: redirecionamento baseado no tipo
            if tipo == "aluno":
                return redirect(url_for("aluno_home"))
            elif tipo == "professor":
                return redirect(url_for("professor_home"))
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
        usuario = request.form.get("usuario", "").strip()
        senha = request.form.get("senha", "")
        tipo = request.form.get("tipo", "")

        # Validações
        if not usuario or not senha or not tipo:
            return render_template("cadastro.html", erro="Preencha todos os campos")
        
        if tipo not in ["aluno", "professor"]:
            return render_template("cadastro.html", erro="Tipo de usuário inválido")

        if usuario in usuarios:
            return render_template("cadastro.html", erro="Usuário já existe!")
        
        # Cria novo usuário
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
    if "usuario" not in session:
        return redirect(url_for("login"))
    
    usuario = session["usuario"]
    if usuario not in usuarios or usuarios[usuario]["tipo"] != "aluno":
        return redirect(url_for("login"))
    
    return render_template("aluno_home.html", nome=usuario)


@app.route("/aluno/atividades")
def aluno_atividades():
    if "usuario" not in session:
        return redirect(url_for("login"))
    
    usuario = session["usuario"]
    if usuario not in usuarios or usuarios[usuario]["tipo"] != "aluno":
        return redirect(url_for("login"))

    return render_template("aluno_atividades.html", nome=usuario, atividades=atividades.get(usuario, []))


@app.route("/aluno/notas")
def aluno_notas():
    if "usuario" not in session:
        return redirect(url_for("login"))
    
    usuario = session["usuario"]
    if usuario not in usuarios or usuarios[usuario]["tipo"] != "aluno":
        return redirect(url_for("login"))

    notas_aluno = notas.get(usuario, [])
    media = round(sum(notas_aluno) / len(notas_aluno), 2) if notas_aluno else 0
    situacao = "Aprovado 🩵" if media >= 7 else "Reprovado 💔"

    return render_template(
        "aluno_notas.html",
        nome=usuario,
        notas=notas_aluno,
        media=media,
        situacao=situacao
    )

# -------------------------------
# ÁREA DO PROFESSOR
# -------------------------------

@app.route("/professor/home")
def professor_home():
    if "usuario" not in session:
        return redirect(url_for("login"))
    
    usuario = session["usuario"]
    if usuario not in usuarios or usuarios[usuario]["tipo"] != "professor":
        return redirect(url_for("login"))
    
    # Lista apenas alunos
    alunos = [user for user in usuarios if usuarios[user]["tipo"] == "aluno"]
    return render_template("professor_home.html", nome=usuario, alunos=alunos, notas=notas, atividades=atividades)


@app.route("/professor/notas", methods=["GET", "POST"])
def professor_notas():
    if "usuario" not in session:
        return redirect(url_for("login"))
    
    usuario = session["usuario"]
    if usuario not in usuarios or usuarios[usuario]["tipo"] != "professor":
        return redirect(url_for("login"))

    mensagem = None
    erro = None
    
    # Professor pode adicionar nota
    if request.method == "POST":
        aluno = request.form.get("aluno", "").strip()
        nota_str = request.form.get("nota", "").strip()
        
        if not aluno or not nota_str:
            erro = "Preencha todos os campos"
        else:
            # Verifica se o aluno existe
            if aluno not in usuarios:
                erro = f"Aluno '{aluno}' não está cadastrado no sistema"
            elif usuarios[aluno]["tipo"] != "aluno":
                erro = f"'{aluno}' não é um aluno"
            else:
                try:
                    nota = float(nota_str)
                    if 0 <= nota <= 10:
                        if aluno not in notas:
                            notas[aluno] = []
                        notas[aluno].append(nota)
                        mensagem = f"✅ Nota {nota} adicionada para {aluno} com sucesso!"
                    else:
                        erro = "A nota deve estar entre 0 e 10"
                except ValueError:
                    erro = "Nota inválida. Digite apenas números"

    # Lista apenas alunos para facilitar
    alunos_disponiveis = [user for user in usuarios if usuarios[user]["tipo"] == "aluno"]
    
    return render_template("professor_notas.html", 
                         notas=notas, 
                         mensagem=mensagem, 
                         erro=erro,
                         alunos_disponiveis=alunos_disponiveis)


@app.route("/professor/atividades", methods=["GET", "POST"])
def professor_atividades():
    if "usuario" not in session:
        return redirect(url_for("login"))
    
    usuario = session["usuario"]
    if usuario not in usuarios or usuarios[usuario]["tipo"] != "professor":
        return redirect(url_for("login"))

    mensagem = None
    erro = None
    
    # Professor pode adicionar atividade
    if request.method == "POST":
        aluno = request.form.get("aluno", "").strip()
        atividade = request.form.get("atividade", "").strip()
        
        if not aluno or not atividade:
            erro = "Preencha todos os campos"
        else:
            # Verifica se o aluno existe
            if aluno not in usuarios:
                erro = f"Aluno '{aluno}' não está cadastrado no sistema"
            elif usuarios[aluno]["tipo"] != "aluno":
                erro = f"'{aluno}' não é um aluno"
            else:
                if aluno not in atividades:
                    atividades[aluno] = []
                atividades[aluno].append(atividade)
                mensagem = f"✅ Atividade adicionada para {aluno} com sucesso!"

    # Lista apenas alunos para facilitar
    alunos_disponiveis = [user for user in usuarios if usuarios[user]["tipo"] == "aluno"]
    
    return render_template("professor_atividades.html", 
                         atividades=atividades, 
                         mensagem=mensagem, 
                         erro=erro,
                         alunos_disponiveis=alunos_disponiveis)

# -------------------------------
# EXECUÇÃO
# -------------------------------

if __name__ == "__main__":
    app.run(debug=True)
