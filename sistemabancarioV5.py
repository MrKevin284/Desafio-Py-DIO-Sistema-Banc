menu = """

[d] Depositar
[s] Sacar
[e] Extrato
[uc] Cadastrar Usuário
[cc] Criar Conta Corrente
[t] Transferir
[cs] Consultar Saldo
[q] Sair

=> """

# Lista para armazenar os usuários
usuarios = []

# Lista para armazenar as contas correntes
contas = []

# Função para realizar saque
def saque(conta, valor):
    saldo = conta['saldo']
    extrato = conta['extrato']
    limite = conta['limite']
    numero_saques = conta['numero_saques']
    limite_saques = conta['limite_saques']

    excedeu_saldo = valor > saldo
    excedeu_limite = valor > limite
    excedeu_saques = numero_saques >= limite_saques

    if excedeu_saldo:
        print("Operação falhou! Você não tem saldo suficiente.")
    elif excedeu_limite:
        print("Operação falhou! O valor do saque excede o limite.")
    elif excedeu_saques:
        print("Operação falhou! Número máximo de saques excedido.")
    elif valor > 0:
        saldo -= valor
        extrato += f"Saque: R$ {valor:.2f}\n"
        numero_saques += 1

    conta['saldo'] = saldo
    conta['extrato'] = extrato
    conta['numero_saques'] = numero_saques

# Função para realizar depósito
def deposito(conta, valor):
    saldo = conta['saldo']
    extrato = conta['extrato']

    if valor > 0:
        saldo += valor
        extrato += f"Depósito: R$ {valor:.2f}\n"
    else:
        print("Operação falhou! O valor informado é inválido.")

    conta['saldo'] = saldo
    conta['extrato'] = extrato

# Função para exibir o extrato
def exibir_extrato(conta):
    saldo = conta['saldo']
    extrato = conta['extrato']

    print("\n================ EXTRATO ================")
    print("Não foram realizadas movimentações." if not extrato else extrato)
    print(f"\nSaldo: R$ {saldo:.2f}")
    print("==========================================")

# Função para cadastrar usuário
def cadastrar_usuario():
    nome = input("Informe o nome do usuário: ")
    data_nascimento = input("Informe a data de nascimento do usuário: ")
    cpf = input("Informe o CPF do usuário: ")
    endereco = input("Informe o endereço do usuário: ")

    # Verifica se o CPF já está cadastrado
    cpf_existente = any(usuario["cpf"] == cpf for usuario in usuarios)

    if cpf_existente:
        print("Operação falhou! Já existe um usuário cadastrado com o CPF informado.")
    else:
        usuarios.append({
            "nome": nome,
            "data_nascimento": data_nascimento,
            "cpf": cpf,
            "endereco": endereco
        })
        print("Usuário cadastrado com sucesso!")

# Função para criar conta corrente
def criar_conta_corrente():
    cpf = input("Informe o CPF do usuário para associar a conta corrente: ")

    # Filtra a lista de usuários buscando o CPF informado
    usuario = next((usuario for usuario in usuarios if usuario["cpf"] == cpf), None)

    if usuario is None:
        print("Operação falhou! Não foi encontrado um usuário com o CPF informado.")
    else:
        numero_conta = len(contas) + 1
        contas.append({
            "agencia": "0001",
            "numero_conta": numero_conta,
            "usuario": usuario,
            "saldo": 0,
            "limite": 500,
            "extrato": "",
            "numero_saques": 0,
            "limite_saques": 3
        })
        print("Conta corrente criada com sucesso!")

# Função para realizar transferência
def transferencia():
    numero_conta_origem = input("Informe o número da conta de origem: ")
    numero_conta_destino = input("Informe o número da conta de destino: ")
    valor = float(input("Informe o valor da transferência: "))

    conta_origem = next((conta for conta in contas if conta["numero_conta"] == int(numero_conta_origem)), None)
    conta_destino = next((conta for conta in contas if conta["numero_conta"] == int(numero_conta_destino)), None)

    if conta_origem is None or conta_destino is None:
        print("Operação falhou! Conta de origem ou destino não encontrada.")
    elif valor > conta_origem['saldo']:
        print("Operação falhou! Você não tem saldo suficiente.")
    elif valor > 0:
        conta_origem['saldo'] -= valor
        conta_origem['extrato'] += f"Transferência: R$ {valor:.2f} para a conta {numero_conta_destino}\n"
        # Adicionando o valor na conta destino
        conta_destino['saldo'] += valor
    else:
        print("Operação falhou! O valor informado é inválido.")

# Função para consultar saldo
def consultar_saldo():
    numero_conta = input("Informe o número da conta: ")

    conta = next((conta for conta in contas if conta["numero_conta"] == int(numero_conta)), None)

    if conta is None:
        print("Operação falhou! Conta não encontrada.")
    else:
        print(f"O saldo da conta {numero_conta} é R$ {conta['saldo']:.2f}")

while True:
    opcao = input(menu)

    if opcao == "d":
        numero_conta = input("Informe o número da conta para depósito: ")
        valor = float(input("Informe o valor do depósito: "))
        conta = next((conta for conta in contas if conta["numero_conta"] == int(numero_conta)), None)
        if conta is not None:
            deposito(conta, valor)
        else:
            print("Conta não encontrada.")

    elif opcao == "s":
        numero_conta = input("Informe o número da conta para saque: ")
        valor = float(input("Informe o valor do saque: "))
        conta = next((conta for conta in contas if conta["numero_conta"] == int(numero_conta)), None)
        if conta is not None:
            saque(conta, valor)
        else:
            print("Conta não encontrada.")

    elif opcao == "e":
        numero_conta = input("Informe o número da conta para exibir extrato: ")
        conta = next((conta for conta in contas if conta["numero_conta"] == int(numero_conta)), None)
        if conta is not None:
            exibir_extrato(conta)
        else:
            print("Conta não encontrada.")

    elif opcao == "uc":
        cadastrar_usuario()

    elif opcao == "cc":
        criar_conta_corrente()

    elif opcao == "t":
        transferencia()

    elif opcao == "cs":
        consultar_saldo()

    elif opcao == "q":
        break

    else:
        print("Operação inválida, por favor selecione novamente a operação desejada.")