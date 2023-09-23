import tkinter as tk
from tkinter import ttk
import re

# Lista para armazenar os usuários
usuarios = []

# Lista para armazenar as contas correntes
contas = []

# Função para realizar saque
def saque():
    numero_conta = numero_conta_saque_entry.get()
    valor = float(valor_saque_entry.get())
    conta = next((conta for conta in contas if conta["numero_conta"] == int(numero_conta)), None)
    if conta is not None:
        saldo = conta['saldo']
        extrato = conta['extrato']
        limite = conta['limite']
        numero_saques = conta['numero_saques']
        limite_saques = conta['limite_saques']

        excedeu_saldo = valor > saldo
        excedeu_limite = valor > limite
        excedeu_saques = numero_saques >= limite_saques

        if excedeu_saldo:
            resultado_label.config(text="Operação falhou! Você não tem saldo suficiente.")
        elif excedeu_limite:
            resultado_label.config(text="Operação falhou! O valor do saque excede o limite.")
        elif excedeu_saques:
            resultado_label.config(text="Operação falhou! Número máximo de saques excedido.")
        elif valor > 0:
            saldo -= valor
            extrato += f"Saque: R$ {valor:.2f}\n"
            numero_saques += 1

        conta['saldo'] = saldo
        conta['extrato'] = extrato
        conta['numero_saques'] = numero_saques
        numero_conta_label.config(text=f"Número da Conta: {numero_conta}")
        resultado_label.config(text="Saque realizado com sucesso.")
    else:
        resultado_label.config(text="Conta não encontrada.")

# Função para realizar depósito
def deposito():
    numero_conta = numero_conta_deposito_entry.get()
    valor = float(valor_deposito_entry.get())
    conta = next((conta for conta in contas if conta["numero_conta"] == int(numero_conta)), None)
    if conta is not None:
        saldo = conta['saldo']
        extrato = conta['extrato']
        if valor > 0:
            saldo += valor
            extrato += f"Depósito: R$ {valor:.2f}\n"
            conta['saldo'] = saldo
            conta['extrato'] = extrato
            resultado_label.config(text="Depósito realizado com sucesso.")
        else:
            resultado_label.config(text="Operação falhou! O valor informado é inválido.")
    else:
        resultado_label.config(text="Conta não encontrada.")

# Função para exibir o extrato
def exibir_extrato():
    numero_conta = numero_conta_extrato_entry.get()
    conta = next((conta for conta in contas if conta["numero_conta"] == int(numero_conta)), None)
    if conta is not None:
        saldo = conta['saldo']
        extrato = conta['extrato']
        extrato_text.config(text=extrato)
        saldo_text.config(text=f"Saldo: R$ {saldo:.2f}")
    else:
        resultado_label.config(text="Conta não encontrada.")

# Função para cadastrar usuário
def cadastrar_usuario():
    nome = nome_cadastro_entry.get()
    data_nascimento = data_nascimento_cadastro_entry.get()
    cpf = cpf_cadastro_entry.get()
    cep = cep_cadastro_entry.get()

    # Validar formato de data (DD-MM-YYYY)
    if not re.match(r'\d{2}-\d{2}-\d{4}', data_nascimento):
        resultado_label.config(text="Operação falhou! Data de nascimento no formato incorreto (DD-MM-YYYY).")
        return

    # Validar formato de CPF (inserir pontos e traço)
    if not re.match(r'\d{3}\.\d{3}\.\d{3}-\d{2}', cpf):
        resultado_label.config(text="Operação falhou! CPF no formato incorreto (XXX.XXX.XXX-XX).")
        return

    # Validar formato de CEP
    if not re.match(r'\d{5}-\d{3}', cep):
        resultado_label.config(text="Operação falhou! CEP no formato incorreto (XXXXX-XXX).")
        return

    # Verifica se o CPF já está cadastrado
    cpf_existente = any(usuario["cpf"] == cpf for usuario in usuarios)

    if cpf_existente or not nome or not cpf:
        resultado_label.config(text="Operação falhou! Preencha todos os campos e/ou CPF já cadastrado.")
    else:
        usuarios.append({
            "nome": nome,
            "data_nascimento": data_nascimento,
            "cpf": cpf,
            "cep": cep
        })
        resultado_label.config(text="Usuário cadastrado com sucesso!")

# Função para criar conta corrente
def criar_conta_corrente():
    cpf = cpf_conta_corrente_entry.get()

    # Filtra a lista de usuários buscando o CPF informado
    usuario = next((usuario for usuario in usuarios if usuario["cpf"] == cpf), None)

    if usuario is None:
        resultado_label.config(text="Operação falhou! Não foi encontrado um usuário com o CPF informado.")
    else:
        # Verifica se o usuário já possui uma conta corrente
        conta_existente = any(conta["usuario"]["cpf"] == cpf for conta in contas)

        if conta_existente:
            resultado_label.config(text="Operação falhou! O usuário já possui uma conta corrente.")
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
                "limite_saques": 3,
                "limite_transferencia": 500  # Limite de transferência inicial
            })
            resultado_label.config(text="Conta corrente criada com sucesso!")

# Função para realizar transferência
def transferencia():
    numero_conta_origem = numero_conta_origem_transferencia_entry.get()
    numero_conta_destino = numero_conta_destino_transferencia_entry.get()
    valor = float(valor_transferencia_entry.get())

    conta_origem = next((conta for conta in contas if conta["numero_conta"] == int(numero_conta_origem)), None)
    conta_destino = next((conta for conta in contas if conta["numero_conta"] == int(numero_conta_destino)), None)

    if conta_origem is None or conta_destino is None:
        resultado_label.config(text="Operação falhou! Conta de origem ou destino não encontrada.")
    elif valor > conta_origem['saldo']:
        resultado_label.config(text="Operação falhou! Você não tem saldo suficiente para realizar a transferência.")
    elif valor > conta_origem['limite_transferencia']:
        resultado_label.config(text="Operação falhou! O valor da transferência excede o limite permitido.")
    else:
        saldo_origem = conta_origem['saldo']
        extrato_origem = conta_origem['extrato']

        saldo_destino = conta_destino['saldo']
        extrato_destino = conta_destino['extrato']

        saldo_origem -= valor
        extrato_origem += f"Transferência enviada para Conta {numero_conta_destino}: R$ {valor:.2f}\n"

        saldo_destino += valor
        extrato_destino += f"Transferência recebida da Conta {numero_conta_origem}: R$ {valor:.2f}\n"

        conta_origem['saldo'] = saldo_origem
        conta_origem['extrato'] = extrato_origem

        conta_destino['saldo'] = saldo_destino
        conta_destino['extrato'] = extrato_destino

        resultado_label.config(text="Transferência realizada com sucesso.")

# Função para consultar saldo
def consultar_saldo():
    numero_conta = numero_conta_saldo_entry.get()
    conta = next((conta for conta in contas if conta["numero_conta"] == int(numero_conta)), None)
    if conta is not None:
        saldo = conta['saldo']
        saldo_text.config(text=f"Saldo: R$ {saldo:.2f}")
    else:
        resultado_label.config(text="Conta não encontrada.")

# Função para atualizar limite de transferência
def atualizar_limite_transferencia():
    numero_conta = numero_conta_atualizar_limite_transferencia_entry.get()
    novo_limite_transferencia = int(novo_limite_transferencia_entry.get())

    conta = next((conta for conta in contas if conta["numero_conta"] == int(numero_conta)), None)

    if conta is not None:
        if 500 <= novo_limite_transferencia <= 100000:
            conta['limite_transferencia'] = novo_limite_transferencia
            resultado_label.config(text="Limite de transferência atualizado com sucesso.")
        else:
            resultado_label.config(text="Operação falhou! O novo limite de transferência deve estar entre 500 e 100,000.")
    else:
        resultado_label.config(text="Conta não encontrada.")

# Função para mostrar ajuda sobre a atualização do limite de transferência
def mostrar_ajuda_limite_transferencia():
    ajuda_window = tk.Toplevel(root)
    ajuda_window.title("Ajuda - Limite de Transferência")

    ajuda_text = tk.Label(ajuda_window, text="Para atualizar o limite de transferência, insira o número da conta e o novo limite desejado.\n"
                                             "O novo limite deve estar no intervalo de 500 a 100,000.")
    ajuda_text.pack(padx=20, pady=20)

# Função para consultar conta por CPF
def consultar_conta_por_cpf():
    cpf = cpf_consulta_conta_entry.get()
    conta = next((conta for conta in contas if conta["usuario"]["cpf"] == cpf), None)
    if conta is not None:
        abrir_janela_info_conta(conta, conta['limite_transferencia'])
    else:
        resultado_label.config(text="Conta não encontrada.")

# Função para abrir janela com informações da conta
def abrir_janela_info_conta(conta, limite):
    info_window = tk.Toplevel(root)
    info_window.title(f"Informações da Conta - Número {conta['numero_conta']}")

    info_label = tk.Label(info_window, text=f"Informações da Conta - Número {conta['numero_conta']}\n"
                                             f"Titular: {conta['usuario']['nome']}\n"
                                             f"CPF: {conta['usuario']['cpf']}\n"
                                             f"CEP: {conta['usuario']['cep']}\n"
                                             f"Saldo: R$ {conta['saldo']:.2f}\n"
                                             f"Limite de Transferência: R$ {limite:.2f}")
    info_label.pack(padx=20, pady=20)

# Função para sair do programa
def sair():
    root.quit()

# Criação de janela principal
root = tk.Tk()
root.title("Sistema Bancário")

# Criação de widgets para cada operação
# Widgets para saque
saque_label = tk.Label(root, text="Saque")
numero_conta_saque_label = tk.Label(root, text="Número da Conta:")
numero_conta_saque_entry = tk.Entry(root)
valor_saque_label = tk.Label(root, text="Valor do Saque:")
valor_saque_entry = tk.Entry(root)
saque_button = tk.Button(root, text="Realizar Saque", command=saque)

# Widgets para depósito
deposito_label = tk.Label(root, text="Depósito")
numero_conta_deposito_label = tk.Label(root, text="Número da Conta:")
numero_conta_deposito_entry = tk.Entry(root)
valor_deposito_label = tk.Label(root, text="Valor do Depósito:")
valor_deposito_entry = tk.Entry(root)
deposito_button = tk.Button(root, text="Realizar Depósito", command=deposito)

# Widgets para extrato
extrato_label = tk.Label(root, text="Extrato")
numero_conta_extrato_label = tk.Label(root, text="Número da Conta:")
numero_conta_extrato_entry = tk.Entry(root)
extrato_button = tk.Button(root, text="Exibir Extrato", command=exibir_extrato)
extrato_text = tk.Label(root, text="", justify="left")
saldo_text = tk.Label(root, text="Saldo: R$ 0.00")

# Widgets para cadastro de usuário
cadastro_usuario_label = tk.Label(root, text="Cadastro de Usuário")
nome_cadastro_label = tk.Label(root, text="Nome:")
nome_cadastro_entry = tk.Entry(root)
data_nascimento_cadastro_label = tk.Label(root, text="Data de Nascimento (DD-MM-YYYY):")
data_nascimento_cadastro_entry = tk.Entry(root)
cpf_cadastro_label = tk.Label(root, text="CPF (XXX.XXX.XXX-XX):")
cpf_cadastro_entry = tk.Entry(root)
cep_cadastro_label = tk.Label(root, text="CEP (XXXXX-XXX):")
cep_cadastro_entry = tk.Entry(root)
cadastrar_usuario_button = tk.Button(root, text="Cadastrar Usuário", command=cadastrar_usuario)

# Widgets para criação de conta corrente
conta_corrente_label = tk.Label(root, text="Criação de Conta Corrente")
cpf_conta_corrente_label = tk.Label(root, text="CPF do Titular:")
cpf_conta_corrente_entry = tk.Entry(root)
criar_conta_corrente_button = tk.Button(root, text="Criar Conta Corrente", command=criar_conta_corrente)

# Widgets para transferência
transferencia_label = tk.Label(root, text="Transferência")
numero_conta_origem_transferencia_label = tk.Label(root, text="Conta de Origem:")
numero_conta_origem_transferencia_entry = tk.Entry(root)
numero_conta_destino_transferencia_label = tk.Label(root, text="Conta de Destino:")
numero_conta_destino_transferencia_entry = tk.Entry(root)
valor_transferencia_label = tk.Label(root, text="Valor da Transferência:")
valor_transferencia_entry = tk.Entry(root)
transferencia_button = tk.Button(root, text="Realizar Transferência", command=transferencia)

# Widgets para consulta de saldo
saldo_label = tk.Label(root, text="Consulta de Saldo")
numero_conta_saldo_label = tk.Label(root, text="Número da Conta:")
numero_conta_saldo_entry = tk.Entry(root)
saldo_button = tk.Button(root, text="Consultar Saldo", command=consultar_saldo)

# Widgets para atualização de limite de transferência
atualizar_limite_transferencia_label = tk.Label(root, text="Atualizar Limite de Transferência")
numero_conta_atualizar_limite_transferencia_label = tk.Label(root, text="Número da Conta:")
numero_conta_atualizar_limite_transferencia_entry = tk.Entry(root)
novo_limite_transferencia_label = tk.Label(root, text="Novo Limite de Transferência:")
novo_limite_transferencia_entry = tk.Entry(root)
atualizar_limite_transferencia_button = tk.Button(root, text="Atualizar Limite", command=atualizar_limite_transferencia)
ajuda_limite_transferencia_button = tk.Button(root, text="Ajuda", command=mostrar_ajuda_limite_transferencia)

# Widgets para consulta de conta por CPF
consulta_conta_label = tk.Label(root, text="Consultar Conta por CPF")
cpf_consulta_conta_label = tk.Label(root, text="CPF do Titular:")
cpf_consulta_conta_entry = tk.Entry(root)
consulta_conta_button = tk.Button(root, text="Consultar Conta", command=consultar_conta_por_cpf)

# Widget para resultado das operações
resultado_label = tk.Label(root, text="", font=("Helvetica", 12), fg="blue")

# Widget para botão de sair
sair_button = tk.Button(root, text="Sair", command=sair)

# Posicionamento dos widgets na janela principal
saque_label.grid(row=0, column=0, padx=20, pady=10, sticky="w")
numero_conta_saque_label.grid(row=1, column=0, padx=20, sticky="w")
numero_conta_saque_entry.grid(row=1, column=1, padx=10, pady=10)
valor_saque_label.grid(row=2, column=0, padx=20, sticky="w")
valor_saque_entry.grid(row=2, column=1, padx=10, pady=10)
saque_button.grid(row=3, column=0, columnspan=2, padx=20, pady=10)

deposito_label.grid(row=0, column=2, padx=20, pady=10, sticky="w")
numero_conta_deposito_label.grid(row=1, column=2, padx=20, sticky="w")
numero_conta_deposito_entry.grid(row=1, column=3, padx=10, pady=10)
valor_deposito_label.grid(row=2, column=2, padx=20, sticky="w")
valor_deposito_entry.grid(row=2, column=3, padx=10, pady=10)
deposito_button.grid(row=3, column=2, columnspan=2, padx=20, pady=10)

extrato_label.grid(row=0, column=4, padx=20, pady=10, sticky="w")
numero_conta_extrato_label.grid(row=1, column=4, padx=20, sticky="w")
numero_conta_extrato_entry.grid(row=1, column=5, padx=10, pady=10)
extrato_button.grid(row=2, column=4, columnspan=2, padx=20, pady=10)
extrato_text.grid(row=3, column=4, columnspan=2, padx=20, pady=10, sticky="w")
saldo_text.grid(row=3, column=5, padx=20, pady=10, sticky="e")

cadastro_usuario_label.grid(row=4, column=0, padx=20, pady=10, sticky="w")
nome_cadastro_label.grid(row=5, column=0, padx=20, sticky="w")
nome_cadastro_entry.grid(row=5, column=1, padx=10, pady=10)
data_nascimento_cadastro_label.grid(row=6, column=0, padx=20, sticky="w")
data_nascimento_cadastro_entry.grid(row=6, column=1, padx=10, pady=10)
cpf_cadastro_label.grid(row=7, column=0, padx=20, sticky="w")
cpf_cadastro_entry.grid(row=7, column=1, padx=10, pady=10)
cep_cadastro_label.grid(row=8, column=0, padx=20, sticky="w")
cep_cadastro_entry.grid(row=8, column=1, padx=10, pady=10)
cadastrar_usuario_button.grid(row=9, column=0, columnspan=2, padx=20, pady=10)

conta_corrente_label.grid(row=4, column=2, padx=20, pady=10, sticky="w")
cpf_conta_corrente_label.grid(row=5, column=2, padx=20, sticky="w")
cpf_conta_corrente_entry.grid(row=5, column=3, padx=10, pady=10)
criar_conta_corrente_button.grid(row=6, column=2, columnspan=2, padx=20, pady=10)

transferencia_label.grid(row=4, column=4, padx=20, pady=10, sticky="w")
numero_conta_origem_transferencia_label.grid(row=5, column=4, padx=20, sticky="w")
numero_conta_origem_transferencia_entry.grid(row=5, column=5, padx=10, pady=10)
numero_conta_destino_transferencia_label.grid(row=6, column=4, padx=20, sticky="w")
numero_conta_destino_transferencia_entry.grid(row=6, column=5, padx=10, pady=10)
valor_transferencia_label.grid(row=7, column=4, padx=20, sticky="w")
valor_transferencia_entry.grid(row=7, column=5, padx=10, pady=10)
transferencia_button.grid(row=8, column=4, columnspan=2, padx=20, pady=10)

saldo_label.grid(row=9, column=2, padx=20, pady=10, sticky="w")
numero_conta_saldo_label.grid(row=10, column=2, padx=20, sticky="w")
numero_conta_saldo_entry.grid(row=10, column=3, padx=10, pady=10)
saldo_button.grid(row=11, column=2, columnspan=2, padx=20, pady=10)

atualizar_limite_transferencia_label.grid(row=9, column=4, padx=20, pady=10, sticky="w")
numero_conta_atualizar_limite_transferencia_label.grid(row=10, column=4, padx=20, sticky="w")
numero_conta_atualizar_limite_transferencia_entry.grid(row=10, column=5, padx=10, pady=10)
novo_limite_transferencia_label.grid(row=11, column=4, padx=20, sticky="w")
novo_limite_transferencia_entry.grid(row=11, column=5, padx=10, pady=10)
atualizar_limite_transferencia_button.grid(row=12, column=4, padx=20, pady=10)
ajuda_limite_transferencia_button.grid(row=12, column=5, padx=20, pady=10)

consulta_conta_label.grid(row=13, column=0, padx=20, pady=10, sticky="w")
cpf_consulta_conta_label.grid(row=14, column=0, padx=20, sticky="w")
cpf_consulta_conta_entry.grid(row=14, column=1, padx=10, pady=10)
consulta_conta_button.grid(row=15, column=0, columnspan=2, padx=20, pady=10)

resultado_label.grid(row=14, column=0, columnspan=6, padx=20, pady=10)

sair_button.grid(row=15, column=10, columnspan=6, padx=20, pady=10)

# Inicialização da janela
root.mainloop()
