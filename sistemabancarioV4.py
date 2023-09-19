import tkinter as tk

# Função para realizar saque
def saque(*, saldo, valor, extrato, limite, numero_saques, limite_saques):
    excedeu_saldo = valor > saldo
    excedeu_limite = valor > limite
    excedeu_saques = numero_saques >= limite_saques

    if excedeu_saldo:
        return saldo, extrato + "Operação falhou! Você não tem saldo suficiente.\n"
    elif excedeu_limite:
        return saldo, extrato + "Operação falhou! O valor do saque excede o limite.\n"
    elif excedeu_saques:
        return saldo, extrato + "Operação falhou! Número máximo de saques excedido.\n"
    elif valor > 0:
        saldo -= valor
        extrato += f"Saque: R$ {valor:.2f}\n"
        numero_saques += 1

    return saldo, extrato

# Função para realizar depósito
def deposito(saldo, valor, extrato):
    if valor > 0:
        saldo += valor
        extrato += f"Depósito: R$ {valor:.2f}\n"
    else:
        extrato += "Operação falhou! O valor informado é inválido.\n"

    return saldo, extrato

# Função para exibir o extrato
def exibir_extrato(saldo, *, extrato):
    result = "\n================ EXTRATO ================\n"
    result += "Não foram realizadas movimentações.\n" if not extrato else extrato
    result += f"\nSaldo: R$ {saldo:.2f}\n"
    result += "==========================================\n"
    return result

# Função para cadastrar usuário
def cadastrar_usuario(usuarios):
    nome = input("Informe o nome do usuário: ")
    data_nascimento = input("Informe a data de nascimento do usuário: ")
    cpf = input("Informe o CPF do usuário: ")
    endereco = input("Informe o endereço do usuário: ")

    # Verifica se o CPF já está cadastrado
    cpf_existente = any(usuario["cpf"] == cpf for usuario in usuarios)

    if cpf_existente:
        return usuarios, "Operação falhou! Já existe um usuário cadastrado com o CPF informado.\n"

    usuarios.append({
        "nome": nome,
        "data_nascimento": data_nascimento,
        "cpf": cpf,
        "endereco": endereco
    })
    return usuarios, "Usuário cadastrado com sucesso!\n"

# Função para criar conta corrente
def criar_conta_corrente(usuarios, contas):
    cpf = input("Informe o CPF do usuário para associar a conta corrente: ")

    # Filtra a lista de usuários buscando o CPF informado
    usuario = next((usuario for usuario in usuarios if usuario["cpf"] == cpf), None)

    if usuario is None:
        return contas, "Operação falhou! Não foi encontrado um usuário com o CPF informado.\n"

    numero_conta = len(contas) + 1
    contas.append({
        "agencia": "0001",
        "numero_conta": numero_conta,
        "usuario": usuario
    })
    return contas, "Conta corrente criada com sucesso!\n"

def criar_menu():
    # Crie a janela principal do aplicativo
    root = tk.Tk()
    root.title("Sistema Bancário")

    # Variáveis do sistema bancário
    saldo = 0
    limite = 500
    extrato = ""
    numero_saques = 0
    LIMITE_SAQUES = 3

    # Lista para armazenar os usuários
    usuarios = []

    # Lista para armazenar as contas correntes
    contas = []

    # Função para lidar com a seleção de opções
    def selecionar_opcao():
        opcao = entry.get()
        nonlocal saldo, extrato, numero_saques

        if opcao == "d":
            valor = float(entry_valor.get())
            saldo, extrato = deposito(saldo, valor, extrato)
        elif opcao == "s":
            valor = float(entry_valor.get())
            saldo, extrato = saque(saldo=saldo, valor=valor, extrato=extrato, limite=limite, numero_saques=numero_saques, limite_saques=LIMITE_SAQUES)
        elif opcao == "e":
            result = exibir_extrato(saldo, extrato=extrato)
            extrato_text.config(text=result)
        elif opcao == "uc":
            usuarios, result = cadastrar_usuario(usuarios)
            resultado_text.config(text=result)
        elif opcao == "cc":
            contas, result = criar_conta_corrente(usuarios, contas)
            resultado_text.config(text=result)
        elif opcao == "q":
            root.destroy()
        else:
            resultado_text.config(text="Operação inválida, por favor selecione novamente a operação desejada.")

    # Crie uma label para exibir as opções
    label = tk.Label(root, text="""
[d] Depositar
[s] Sacar
[e] Extrato
[uc] Cadastrar Usuário
[cc] Criar Conta Corrente
[q] Sair
""")
    label.pack()

    # Crie uma entry para o usuário inserir a opção desejada
    entry = tk.Entry(root)
    entry.pack()

    # Crie uma label e uma entry para inserir o valor de depósito ou saque
    label_valor = tk.Label(root, text="Informe o valor:")
    label_valor.pack()
    entry_valor = tk.Entry(root)
    entry_valor.pack()

    # Crie um botão para confirmar a seleção
    botao = tk.Button(root, text="Selecionar", command=selecionar_opcao)
    botao.pack()

    # Crie uma label para exibir o resultado das operações
    resultado_text = tk.Label(root, text="")
    resultado_text.pack()

    # Crie uma label para exibir o extrato
    extrato_text = tk.Label(root, text="")
    extrato_text.pack()

    root.mainloop()

# Chame a função principal para criar o menu
criar_menu()
