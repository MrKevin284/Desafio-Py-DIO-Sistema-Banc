from datetime import date

class Transacao:
    def registrar(self, conta):
        pass

class Deposito(Transacao):
    def __init__(self, valor):
        self.valor = valor

    def registrar(self, conta):
        conta.depositar(self.valor)

class Saque(Transacao):
    def __init__(self, valor):
        self.valor = valor

    def registrar(self, conta):
        conta.sacar(self.valor)

class Historico:
    def __init__(self):
        self.historico = []

    def adicionar_transacao(self, transacao):
        self.historico.append(transacao)

class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []

    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self.contas.append(conta)

class PessoaFisica(Cliente):
    def __init__(self, nome, cpf, data_nascimento, endereco):
        super().__init__(endereco)
        self.nome = nome
        self.cpf = cpf
        self.data_nascimento = data_nascimento

class Conta:
    def __init__(self, cliente, numero, agencia):
        self.saldo = 0
        self.numero = numero
        self.agencia = agencia
        self.cliente = cliente
        self.historico = Historico()

    def saldo(self):
        return self.saldo

    def sacar(self, valor):
        saldo_disponivel = self.saldo + self.limite
        if valor <= saldo_disponivel:
            self.saldo -= valor
            self.historico.adicionar_transacao(Saque(valor))
            return True
        else:
            return False

    def depositar(self, valor):
        if valor > 0:
            self.saldo += valor
            self.historico.adicionar_transacao(Deposito(valor))
            return True
        else:
            return False

class ContaCorrente(Conta):
    def __init__(self, cliente, numero, agencia, limite, limite_saques):
        super().__init__(cliente, numero, agencia)
        self.limite = limite
        self.limite_saques = limite_saques
        self.numero_saques = 0

    def sacar(self, valor):
        if self.numero_saques < self.limite_saques:
            self.numero_saques += 1
            return super().sacar(valor)
        else:
            return False

# Criando o menu de interação com o usuário
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

# Variáveis para armazenar os usuários e contas correntes
usuarios = []
contas = []

# Função para cadastrar usuário
def cadastrar_usuario():
    nome = input("Informe o nome do usuário: ")
    data_nascimento = input("Informe a data de nascimento do usuário (formato YYYY-MM-DD): ")
    cpf = input("Informe o CPF do usuário: ")
    endereco = input("Informe o endereço do usuário: ")

    # Verifica se o CPF já está cadastrado
    cpf_existente = any(usuario.cpf == cpf for usuario in usuarios)

    if cpf_existente:
        print("Operação falhou! Já existe um usuário cadastrado com o CPF informado.")
    else:
        usuarios.append(PessoaFisica(nome, cpf, data_nascimento, endereco))
        print("Usuário cadastrado com sucesso!")

# Função para criar conta corrente
def criar_conta_corrente():
    cpf = input("Informe o CPF do usuário para associar a conta corrente: ")

    # Busca o usuário com o CPF informado
    cliente = next((usuario for usuario in usuarios if usuario.cpf == cpf), None)

    if cliente is None:
        print("Operação falhou! Não foi encontrado um usuário com o CPF informado.")
    else:
        numero_conta = len(contas) + 1
        contas.append(ContaCorrente(cliente, numero_conta, "0001", 500, 3))
        cliente.adicionar_conta(contas[-1])
        print("Conta corrente criada com sucesso!")

# Função para realizar transferência
def transferencia():
    numero_conta_origem = int(input("Informe o número da conta de origem: "))
    numero_conta_destino = int(input("Informe o número da conta de destino: "))
    valor = float(input("Informe o valor da transferência: "))

    conta_origem = next((conta for conta in contas if conta.numero == numero_conta_origem), None)
    conta_destino = next((conta for conta in contas if conta.numero == numero_conta_destino), None)

    if conta_origem is None or conta_destino is None:
        print("Operação falhou! Conta de origem ou destino não encontrada.")
    elif valor > conta_origem.saldo:
        print("Operação falhou! Você não tem saldo suficiente.")
    elif valor > 0:
        conta_origem.sacar(valor)
        conta_destino.depositar(valor)
        print("Transferência realizada com sucesso!")
    else:
        print("Operação falhou! O valor informado é inválido.")

# Função para consultar saldo
def consultar_saldo():
    numero_conta = int(input("Informe o número da conta: "))

    conta = next((conta for conta in contas if conta.numero == numero_conta), None)

    if conta is None:
        print("Operação falhou! Conta não encontrada.")
    else:
        print(f"O saldo da conta {numero_conta} é R$ {conta.saldo:.2f}")

while True:
    opcao = input(menu)

    if opcao == "d":
        numero_conta = int(input("Informe o número da conta para depósito: "))
        valor = float(input("Informe o valor do depósito: "))
        conta = next((conta for conta in contas if conta.numero == numero_conta), None)
        if conta is not None:
            conta.depositar(valor)
            print("Depósito realizado com sucesso!")
        else:
            print("Conta não encontrada.")

    elif opcao == "s":
        numero_conta = int(input("Informe o número da conta para saque: "))
        valor = float(input("Informe o valor do saque: "))
        conta = next((conta for conta in contas if conta.numero == numero_conta), None)
        if conta is not None:
            if conta.sacar(valor):
                print("Saque realizado com sucesso!")
            else:
                print("Operação falhou! Saldo insuficiente ou limite de saques excedido.")
        else:
            print("Conta não encontrada.")

    elif opcao == "e":
        numero_conta = int(input("Informe o número da conta para exibir extrato: "))
        conta = next((conta for conta in contas if conta.numero == numero_conta), None)
        if conta is not None:
            print("\n================ EXTRATO ================")
            for transacao in conta.historico.historico:
                if isinstance(transacao, Deposito):
                    print(f"Depósito: R$ {transacao.valor:.2f}")
                elif isinstance(transacao, Saque):
                    print(f"Saque: R$ {transacao.valor:.2f}")
            print(f"\nSaldo: R$ {conta.saldo:.2f}")
            print("==========================================")
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
