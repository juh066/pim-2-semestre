import json
import os

# Arquivo do banco de dados JSON
DB_FILE = "sistema_academico.json"

# Disciplinas fixas do sistema
DISCIPLINAS = [
    "Matemática",
    "Engenharia de Software",
    "Banco de Dados",
    "Algoritmos e Estruturas de Dados",
    "Redes de Computadores"
]

def inicializar_bd():
    """Cria o arquivo JSON se não existir"""
    if not os.path.exists(DB_FILE):
        dados_iniciais = {
            "professores": {},
            "alunos": {},
            "notas": {}
        }
        salvar_dados(dados_iniciais)

def carregar_dados():
    """Carrega os dados do arquivo JSON"""
    try:
        with open(DB_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return {"professores": {}, "alunos": {}, "notas": {}}

def salvar_dados(dados):
    """Salva os dados no arquivo JSON"""
    with open(DB_FILE, 'w', encoding='utf-8') as f:
        json.dump(dados, f, ensure_ascii=False, indent=4)

def limpar_tela():
    """Limpa a tela do console"""
    os.system('cls' if os.name == 'nt' else 'clear')

def verificar_professor():
    """Verifica se um professor existe e retorna seu ID"""
    dados = carregar_dados()
    
    while True:
        print("\n--- Autenticação de Professor ---")
        id_prof = input("ID do Professor (ou 'sair' para cancelar): ").strip()
        
        if id_prof.lower() == 'sair':
            return None
        
        if id_prof in dados["professores"]:
            print(f"✓ Autenticado como: {dados['professores'][id_prof]['nome']}")
            return id_prof
        else:
            print("✗ Professor não encontrado! Tente novamente.")

# ==================== FUNÇÕES DE CADASTRO ====================

def cadastrar_professor():
    """Cadastra um novo professor no sistema"""
    dados = carregar_dados()
    
    while True:
        print("\n=== CADASTRAR PROFESSOR ===")
        id_prof = input("ID do Professor (ou 'sair' para cancelar): ").strip()
        
        if id_prof.lower() == 'sair':
            print("Operação cancelada.")
            return
        
        if not id_prof:
            print("✗ ID não pode ser vazio!")
            continue
        
        if id_prof in dados["professores"]:
            print("✗ Já existe um professor com este ID!")
            continue
        
        nome = input("Nome do Professor: ").strip()
        if not nome:
            print("✗ Nome não pode ser vazio!")
            continue
        
        dados["professores"][id_prof] = {"nome": nome}
        salvar_dados(dados)
        print("✓ Professor cadastrado com sucesso!")
        break

def cadastrar_aluno():
    """Cadastra um novo aluno no sistema"""
    dados = carregar_dados()
    
    while True:
        print("\n=== CADASTRAR ALUNO ===")
        matricula = input("Número de matrícula (ou 'sair' para cancelar): ").strip()
        
        if matricula.lower() == 'sair':
            print("Operação cancelada.")
            return
        
        if not matricula:
            print("✗ Matrícula não pode ser vazia!")
            continue
        
        if matricula in dados["alunos"]:
            print("✗ Já existe um aluno com esta matrícula!")
            continue
        
        nome = input("Nome do Aluno: ").strip()
        if not nome:
            print("✗ Nome não pode ser vazio!")
            continue
        
        endereco = input("Endereço: ").strip()
        cep = input("CEP: ").strip()
        
        dados["alunos"][matricula] = {
            "nome": nome,
            "endereco": endereco,
            "cep": cep
        }
        salvar_dados(dados)
        print("✓ Aluno cadastrado com sucesso!")
        break

def cadastrar_nota():
    """Cadastra uma nota (apenas professores podem fazer isso)"""
    id_prof = verificar_professor()
    if not id_prof:
        print("Operação cancelada.")
        return
    
    dados = carregar_dados()
    
    while True:
        print("\n=== CADASTRAR NOTA ===")
        matricula = input("Número de matrícula do Aluno (ou 'sair' para cancelar): ").strip()
        
        if matricula.lower() == 'sair':
            print("Operação cancelada.")
            return
        
        if matricula not in dados["alunos"]:
            print("✗ Aluno não encontrado!")
            continue
        
        print(f"\nAluno: {dados['alunos'][matricula]['nome']}")
        print("\n--- Disciplinas Disponíveis ---")
        for i, disc in enumerate(DISCIPLINAS, 1):
            print(f"{i}. {disc}")
        
        escolha = input("\nEscolha o número da disciplina (ou 'sair' para cancelar): ").strip()
        
        if escolha.lower() == 'sair':
            print("Operação cancelada.")
            return
        
        try:
            idx = int(escolha) - 1
            if idx < 0 or idx >= len(DISCIPLINAS):
                print("✗ Opção inválida!")
                continue
            disciplina = DISCIPLINAS[idx]
        except ValueError:
            print("✗ Digite um número válido!")
            continue
        
        try:
            nota = float(input("Nota (0-10): ").strip())
            if nota < 0 or nota > 10:
                print("✗ A nota deve estar entre 0 e 10!")
                continue
        except ValueError:
            print("✗ Nota inválida!")
            continue
        
        chave = f"{matricula}|{disciplina}"
        dados["notas"][chave] = {
            "matricula": matricula,
            "disciplina": disciplina,
            "nota": nota,
            "id_prof": id_prof
        }
        salvar_dados(dados)
        print("✓ Nota cadastrada com sucesso!")
        break

# ==================== FUNÇÕES DE CONSULTA ====================

def consultar_professores():
    """Lista todos os professores cadastrados"""
    dados = carregar_dados()
    
    print("\n=== PROFESSORES CADASTRADOS ===")
    if dados["professores"]:
        for id_prof, info in sorted(dados["professores"].items()):
            print(f"ID: {id_prof} | Nome: {info['nome']}")
    else:
        print("Nenhum professor cadastrado.")
    
    input("\nPressione ENTER para continuar...")

def consultar_disciplinas():
    """Lista todas as disciplinas disponíveis"""
    print("\n=== DISCIPLINAS DISPONÍVEIS ===")
    for i, disc in enumerate(DISCIPLINAS, 1):
        print(f"{i}. {disc}")
    
    input("\nPressione ENTER para continuar...")

def consultar_alunos():
    """Lista todos os alunos cadastrados"""
    dados = carregar_dados()
    
    print("\n=== ALUNOS CADASTRADOS ===")
    if dados["alunos"]:
        for mat, info in sorted(dados["alunos"].items()):
            print(f"Matrícula: {mat} | Nome: {info['nome']} | "
                  f"Endereço: {info['endereco']} | CEP: {info['cep']}")
    else:
        print("Nenhum aluno cadastrado.")
    
    input("\nPressione ENTER para continuar...")

def consultar_notas():
    """Lista todas as notas (apenas professores podem fazer isso)"""
    id_prof = verificar_professor()
    if not id_prof:
        print("Operação cancelada.")
        return
    
    dados = carregar_dados()
    
    print("\n=== NOTAS CADASTRADAS ===")
    if dados["notas"]:
        for chave, info in sorted(dados["notas"].items()):
            aluno_nome = dados["alunos"].get(info['matricula'], {}).get('nome', 'Desconhecido')
            prof_nome = dados["professores"].get(info['id_prof'], {}).get('nome', 'Desconhecido')
            print(f"Aluno: {aluno_nome} | Disciplina: {info['disciplina']} | "
                  f"Nota: {info['nota']:.1f} | Professor: {prof_nome}")
    else:
        print("Nenhuma nota cadastrada.")
    
    input("\nPressione ENTER para continuar...")

# ==================== FUNÇÕES DE ALTERAÇÃO ====================

def alterar_professor():
    """Altera os dados de um professor"""
    dados = carregar_dados()
    
    while True:
        print("\n=== ALTERAR PROFESSOR ===")
        id_prof = input("ID do Professor a alterar (ou 'sair' para cancelar): ").strip()
        
        if id_prof.lower() == 'sair':
            print("Operação cancelada.")
            return
        
        if id_prof not in dados["professores"]:
            print("✗ Professor não encontrado!")
            continue
        
        print(f"Professor atual: {dados['professores'][id_prof]['nome']}")
        novo_nome = input("Novo nome: ").strip()
        
        if not novo_nome:
            print("✗ Nome não pode ser vazio!")
            continue
        
        dados["professores"][id_prof]["nome"] = novo_nome
        salvar_dados(dados)
        print("✓ Professor alterado com sucesso!")
        break

def alterar_aluno():
    """Altera os dados de um aluno"""
    dados = carregar_dados()
    
    while True:
        print("\n=== ALTERAR ALUNO ===")
        matricula = input("Matrícula do Aluno a alterar (ou 'sair' para cancelar): ").strip()
        
        if matricula.lower() == 'sair':
            print("Operação cancelada.")
            return
        
        if matricula not in dados["alunos"]:
            print("✗ Aluno não encontrado!")
            continue
        
        print(f"\nAluno atual: {dados['alunos'][matricula]['nome']}")
        nome = input("Novo nome: ").strip()
        
        if not nome:
            print("✗ Nome não pode ser vazio!")
            continue
        
        endereco = input("Novo endereço: ").strip()
        cep = input("Novo CEP: ").strip()
        
        dados["alunos"][matricula] = {
            "nome": nome,
            "endereco": endereco,
            "cep": cep
        }
        salvar_dados(dados)
        print("✓ Aluno alterado com sucesso!")
        break

def alterar_nota():
    """Altera uma nota (apenas professores podem fazer isso)"""
    id_prof = verificar_professor()
    if not id_prof:
        print("Operação cancelada.")
        return
    
    dados = carregar_dados()
    
    while True:
        print("\n=== ALTERAR NOTA ===")
        matricula = input("Matrícula do Aluno (ou 'sair' para cancelar): ").strip()
        
        if matricula.lower() == 'sair':
            print("Operação cancelada.")
            return
        
        if matricula not in dados["alunos"]:
            print("✗ Aluno não encontrado!")
            continue
        
        print(f"\nAluno: {dados['alunos'][matricula]['nome']}")
        print("\n--- Disciplinas Disponíveis ---")
        for i, disc in enumerate(DISCIPLINAS, 1):
            print(f"{i}. {disc}")
        
        escolha = input("\nEscolha o número da disciplina (ou 'sair' para cancelar): ").strip()
        
        if escolha.lower() == 'sair':
            print("Operação cancelada.")
            return
        
        try:
            idx = int(escolha) - 1
            if idx < 0 or idx >= len(DISCIPLINAS):
                print("✗ Opção inválida!")
                continue
            disciplina = DISCIPLINAS[idx]
        except ValueError:
            print("✗ Digite um número válido!")
            continue
        
        chave = f"{matricula}|{disciplina}"
        
        if chave not in dados["notas"]:
            print("✗ Nota não encontrada para esta combinação!")
            continue
        
        print(f"Nota atual: {dados['notas'][chave]['nota']:.1f}")
        
        try:
            nova_nota = float(input("Nova nota (0-10): ").strip())
            if nova_nota < 0 or nova_nota > 10:
                print("✗ A nota deve estar entre 0 e 10!")
                continue
        except ValueError:
            print("✗ Nota inválida!")
            continue
        
        dados["notas"][chave]["nota"] = nova_nota
        dados["notas"][chave]["id_prof"] = id_prof
        salvar_dados(dados)
        print("✓ Nota alterada com sucesso!")
        break

# ==================== FUNÇÕES DE EXCLUSÃO ====================

def excluir_professor():
    """Exclui um professor do sistema"""
    dados = carregar_dados()
    
    while True:
        print("\n=== EXCLUIR PROFESSOR ===")
        id_prof = input("ID do Professor a excluir (ou 'sair' para cancelar): ").strip()
        
        if id_prof.lower() == 'sair':
            print("Operação cancelada.")
            return
        
        if id_prof not in dados["professores"]:
            print("✗ Professor não encontrado!")
            continue
        
        print(f"Professor: {dados['professores'][id_prof]['nome']}")
        confirmacao = input("Confirma a exclusão? (s/n): ").strip().lower()
        
        if confirmacao == 's':
            del dados["professores"][id_prof]
            salvar_dados(dados)
            print("✓ Professor excluído com sucesso!")
        else:
            print("Exclusão cancelada.")
        break

def excluir_aluno():
    """Exclui um aluno do sistema"""
    dados = carregar_dados()
    
    while True:
        print("\n=== EXCLUIR ALUNO ===")
        matricula = input("Matrícula do Aluno a excluir (ou 'sair' para cancelar): ").strip()
        
        if matricula.lower() == 'sair':
            print("Operação cancelada.")
            return
        
        if matricula not in dados["alunos"]:
            print("✗ Aluno não encontrado!")
            continue
        
        print(f"Aluno: {dados['alunos'][matricula]['nome']}")
        confirmacao = input("Confirma a exclusão? (s/n): ").strip().lower()
        
        if confirmacao == 's':
            del dados["alunos"][matricula]
            # Remove todas as notas do aluno
            notas_para_remover = [k for k in dados["notas"] if dados["notas"][k]["matricula"] == matricula]
            for k in notas_para_remover:
                del dados["notas"][k]
            salvar_dados(dados)
            print("✓ Aluno excluído com sucesso!")
        else:
            print("Exclusão cancelada.")
        break

def excluir_nota():
    """Exclui uma nota (apenas professores podem fazer isso)"""
    id_prof = verificar_professor()
    if not id_prof:
        print("Operação cancelada.")
        return
    
    dados = carregar_dados()
    
    while True:
        print("\n=== EXCLUIR NOTA ===")
        matricula = input("Matrícula do Aluno (ou 'sair' para cancelar): ").strip()
        
        if matricula.lower() == 'sair':
            print("Operação cancelada.")
            return
        
        if matricula not in dados["alunos"]:
            print("✗ Aluno não encontrado!")
            continue
        
        print(f"\nAluno: {dados['alunos'][matricula]['nome']}")
        print("\n--- Disciplinas Disponíveis ---")
        for i, disc in enumerate(DISCIPLINAS, 1):
            print(f"{i}. {disc}")
        
        escolha = input("\nEscolha o número da disciplina (ou 'sair' para cancelar): ").strip()
        
        if escolha.lower() == 'sair':
            print("Operação cancelada.")
            return
        
        try:
            idx = int(escolha) - 1
            if idx < 0 or idx >= len(DISCIPLINAS):
                print("✗ Opção inválida!")
                continue
            disciplina = DISCIPLINAS[idx]
        except ValueError:
            print("✗ Digite um número válido!")
            continue
        
        chave = f"{matricula}|{disciplina}"
        
        if chave not in dados["notas"]:
            print("✗ Nota não encontrada para esta combinação!")
            continue
        
        print(f"Nota atual: {dados['notas'][chave]['nota']:.1f}")
        confirmacao = input("Confirma a exclusão? (s/n): ").strip().lower()
        
        if confirmacao == 's':
            del dados["notas"][chave]
            salvar_dados(dados)
            print("✓ Nota excluída com sucesso!")
        else:
            print("Exclusão cancelada.")
        break

# ==================== MENU PRINCIPAL ====================

def menu():
    """Menu principal do sistema"""
    inicializar_bd()
    
    while True:
        limpar_tela()
        print("╔═══════════════════════════════════════╗")
        print("║   SISTEMA ACADÊMICO - VERSÃO 2.0     ║")
        print("╚═══════════════════════════════════════╝")
        print("\n1. Cadastro")
        print("2. Consulta")
        print("3. Alteração")
        print("4. Exclusão")
        print("0. Sair")
        print("\n" + "="*40)
        
        opcao = input("Escolha uma opção: ").strip()
        
        if opcao == "1":
            limpar_tela()
            print("═══ MENU DE CADASTRO ═══")
            print("1. Professor")
            print("2. Aluno")
            print("3. Nota")
            print("0. Voltar")
            escolha = input("\nEscolha uma opção: ").strip()
            
            if escolha == "1":
                cadastrar_professor()
            elif escolha == "2":
                cadastrar_aluno()
            elif escolha == "3":
                cadastrar_nota()
            elif escolha == "0":
                continue
            else:
                print("✗ Opção inválida!")
                input("\nPressione ENTER para continuar...")
        
        elif opcao == "2":
            limpar_tela()
            print("═══ MENU DE CONSULTA ═══")
            print("1. Professores")
            print("2. Disciplinas")
            print("3. Alunos")
            print("4. Notas")
            print("0. Voltar")
            escolha = input("\nEscolha uma opção: ").strip()
            
            if escolha == "1":
                consultar_professores()
            elif escolha == "2":
                consultar_disciplinas()
            elif escolha == "3":
                consultar_alunos()
            elif escolha == "4":
                consultar_notas()
            elif escolha == "0":
                continue
            else:
                print("✗ Opção inválida!")
                input("\nPressione ENTER para continuar...")
        
        elif opcao == "3":
            limpar_tela()
            print("═══ MENU DE ALTERAÇÃO ═══")
            print("1. Professor")
            print("2. Aluno")
            print("3. Nota")
            print("0. Voltar")
            escolha = input("\nEscolha uma opção: ").strip()
            
            if escolha == "1":
                alterar_professor()
            elif escolha == "2":
                alterar_aluno()
            elif escolha == "3":
                alterar_nota()
            elif escolha == "0":
                continue
            else:
                print("✗ Opção inválida!")
                input("\nPressione ENTER para continuar...")
        
        elif opcao == "4":
            limpar_tela()
            print("═══ MENU DE EXCLUSÃO ═══")
            print("1. Professor")
            print("2. Aluno")
            print("3. Nota")
            print("0. Voltar")
            escolha = input("\nEscolha uma opção: ").strip()
            
            if escolha == "1":
                excluir_professor()
            elif escolha == "2":
                excluir_aluno()
            elif escolha == "3":
                excluir_nota()
            elif escolha == "0":
                continue
            else:
                print("✗ Opção inválida!")
                input("\nPressione ENTER para continuar...")
        
        elif opcao == "0":
            print("\n✓ Encerrando o sistema...")
            print("Até logo!")
            break
        
        else:
            print("✗ Opção inválida!")
            input("\nPressione ENTER para continuar...")

# Executa o programa
if __name__ == "__main__":
    menu()