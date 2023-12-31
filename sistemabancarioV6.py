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
        resultado_label.config(text="Operação falhou! CPF no formato incorreto (inserir pontos e traço).")
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
                "limite_saques": 3
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
        resultado_label.config(text="Operação falhou! Você não tem saldo suficiente.")
    elif valor > 0:
        conta_origem['saldo'] -= valor
        conta_origem['extrato'] += f"Transferência: R$ {valor:.2f} para a conta {numero_conta_destino}\n"
        conta_destino['saldo'] += valor
        resultado_label.config(text="Transferência realizada com sucesso.")
    else:
        resultado_label.config(text="Operação falhou! O valor informado é inválido.")

# Função para consultar saldo
def consultar_saldo():
    numero_conta = numero_conta_saldo_entry.get()
    conta = next((conta for conta in contas if conta["numero_conta"] == int(numero_conta)), None)
    if conta is not None:
        saldo = conta['saldo']
        resultado_label.config(text=f"O saldo da conta {numero_conta} é R$ {saldo:.2f}")
    else:
        resultado_label.config(text="Conta não encontrada.")

# Função para atualizar limite de saques
def atualizar_limite_saques():
    numero_conta = numero_conta_atualizar_limite_entry.get()
    novo_limite = novo_limite_entry.get()

    conta = next((conta for conta in contas if conta["numero_conta"] == int(numero_conta)), None)
    if conta is not None:
        try:
            novo_limite = int(novo_limite)
            if novo_limite >= 0:
                conta['limite_saques'] = novo_limite
                resultado_label.config(text="Limite de saques atualizado com sucesso.")
            else:
                resultado_label.config(text="Operação falhou! O novo limite deve ser um número não negativo.")
        except ValueError:
            resultado_label.config(text="Operação falhou! O novo limite deve ser um número inteiro não negativo.")
    else:
        resultado_label.config(text="Conta não encontrada.")

# Função para mostrar ajuda sobre a atualização do limite de saques
def mostrar_ajuda_limite_saques():
    ajuda_window = tk.Toplevel(root)
    ajuda_window.title("Ajuda - Limite de Saques")

    ajuda_text = tk.Label(ajuda_window, text="Para atualizar o limite de saques, insira o número da conta e o novo limite desejado.\n"
                                             "O novo limite deve ser um número inteiro não negativo.")
    ajuda_text.pack(padx=20, pady=20)

# Função para consultar conta por CPF
def consultar_conta_por_cpf():
    cpf_consulta = cpf_consulta_entry.get()
    conta = next((conta for conta in contas if conta["usuario"]["cpf"] == cpf_consulta), None)
    if conta is not None:
        # Abrir janela para exibir informações da conta
        abrir_janela_info_conta(conta)
    else:
        resultado_label.config(text="Conta não encontrada.")

# Função para abrir janela com informações da conta
def abrir_janela_info_conta(conta):
    info_window = tk.Toplevel(root)
    info_window.title("Informações da Conta")

    info_label = tk.Label(info_window, text=f"Informações da Conta")
    info_label.pack()

    numero_conta_label = tk.Label(info_window, text=f"Número da Conta: {conta['numero_conta']}")
    numero_conta_label.pack()

    agencia_label = tk.Label(info_window, text=f"Agência: {conta['agencia']}")
    agencia_label.pack()

    limite_label = tk.Label(info_window, text=f"Limite: R$ {conta['limite']:.2f}")
    limite_label.pack()

    saldo_label = tk.Label(info_window, text=f"Saldo: R$ {conta['saldo']:.2f}")
    saldo_label.pack()

# Função para sair do programa
def sair():
    root.quit()

# Criação de janela principal
root = tk.Tk()
root.title("Sistema Bancário")

# Criação de widgets para cada operação
saque_label = tk.Label(root, text="Saque")
numero_conta_saque_label = tk.Label(root, text="Número da Conta:")
numero_conta_saque_entry = tk.Entry(root)
valor_saque_label = tk.Label(root, text="Valor:")
valor_saque_entry = tk.Entry(root)
saque_button = tk.Button(root, text="Realizar Saque", command=saque)

deposito_label = tk.Label(root, text="Depósito")
numero_conta_deposito_label = tk.Label(root, text="Número da Conta:")
numero_conta_deposito_entry = tk.Entry(root)
valor_deposito_label = tk.Label(root, text="Valor:")
valor_deposito_entry = tk.Entry(root)
deposito_button = tk.Button(root, text="Realizar Depósito", command=deposito)

extrato_label = tk.Label(root, text="Extrato")
numero_conta_extrato_label = tk.Label(root, text="Número da Conta:")
numero_conta_extrato_entry = tk.Entry(root)
extrato_button = tk.Button(root, text="Exibir Extrato", command=exibir_extrato)
extrato_text = tk.Label(root, text="", justify=tk.LEFT)
saldo_text = tk.Label(root, text="")

cadastrar_usuario_label = tk.Label(root, text="Cadastrar Usuário")
nome_cadastro_label = tk.Label(root, text="Nome:")
nome_cadastro_entry = tk.Entry(root)
data_nascimento_cadastro_label = tk.Label(root, text="Data de Nascimento (DD-MM-YYYY):")
data_nascimento_cadastro_entry = tk.Entry(root)
cpf_cadastro_label = tk.Label(root, text="CPF (inserir pontos e traço):")
cpf_cadastro_entry = tk.Entry(root)
cep_cadastro_label = tk.Label(root, text="CEP (XXXXX-XXX):")
cep_cadastro_entry = tk.Entry(root)
cadastrar_usuario_button = tk.Button(root, text="Cadastrar Usuário", command=cadastrar_usuario)

criar_conta_corrente_label = tk.Label(root, text="Criar Conta Corrente")
cpf_conta_corrente_label = tk.Label(root, text="CPF do Usuário:")
cpf_conta_corrente_entry = tk.Entry(root)
criar_conta_corrente_button = tk.Button(root, text="Criar Conta Corrente", command=criar_conta_corrente)

transferencia_label = tk.Label(root, text="Transferência")
numero_conta_origem_transferencia_label = tk.Label(root, text="Número da Conta de Origem:")
numero_conta_origem_transferencia_entry = tk.Entry(root)
numero_conta_destino_transferencia_label = tk.Label(root, text="Número da Conta de Destino:")
numero_conta_destino_transferencia_entry = tk.Entry(root)
valor_transferencia_label = tk.Label(root, text="Valor:")
valor_transferencia_entry = tk.Entry(root)
transferencia_button = tk.Button(root, text="Realizar Transferência", command=transferencia)

consultar_saldo_label = tk.Label(root, text="Consultar Saldo")
numero_conta_saldo_label = tk.Label(root, text="Número da Conta:")
numero_conta_saldo_entry = tk.Entry(root)
consultar_saldo_button = tk.Button(root, text="Consultar Saldo", command=consultar_saldo)

atualizar_limite_label = tk.Label(root, text="Atualizar Limite de Saques")
numero_conta_atualizar_limite_label = tk.Label(root, text="Número da Conta:")
numero_conta_atualizar_limite_entry = tk.Entry(root)
novo_limite_label = tk.Label(root, text="Novo Limite:")
novo_limite_entry = tk.Entry(root)
atualizar_limite_button = tk.Button(root, text="Atualizar Limite", command=atualizar_limite_saques)

ajuda_limite_button = tk.Button(root, text="?", command=mostrar_ajuda_limite_saques)

sair_button = tk.Button(root, text="Sair", command=sair)

# Rótulo para exibir o número da conta selecionada
numero_conta_label = tk.Label(root, text="", fg="blue")

# Resultado das operações
resultado_label = tk.Label(root, text="", fg="red")

# Adicionar campo para consultar conta por CPF
consultar_conta_por_cpf_label = tk.Label(root, text="Consultar Conta por CPF")
cpf_consulta_label = tk.Label(root, text="CPF do Usuário:")
cpf_consulta_entry = tk.Entry(root)
consultar_conta_button = tk.Button(root, text="Consultar Conta", command=consultar_conta_por_cpf)

# Posicionamento de widgets na janela
saque_label.grid(row=0, column=0)
numero_conta_saque_label.grid(row=1, column=0)
numero_conta_saque_entry.grid(row=1, column=1)
valor_saque_label.grid(row=2, column=0)
valor_saque_entry.grid(row=2, column=1)
saque_button.grid(row=3, column=0)

deposito_label.grid(row=0, column=2)
numero_conta_deposito_label.grid(row=1, column=2)
numero_conta_deposito_entry.grid(row=1, column=3)
valor_deposito_label.grid(row=2, column=2)
valor_deposito_entry.grid(row=2, column=3)
deposito_button.grid(row=3, column=2)

extrato_label.grid(row=0, column=4)
numero_conta_extrato_label.grid(row=1, column=4)
numero_conta_extrato_entry.grid(row=1, column=5)
extrato_button.grid(row=2, column=4)
extrato_text.grid(row=3, column=4, columnspan=2)
saldo_text.grid(row=4, column=4, columnspan=2)
numero_conta_label.grid(row=5, column=4, columnspan=2)

cadastrar_usuario_label.grid(row=6, column=0)
nome_cadastro_label.grid(row=7, column=0)
nome_cadastro_entry.grid(row=7, column=1)
data_nascimento_cadastro_label.grid(row=8, column=0)
data_nascimento_cadastro_entry.grid(row=8, column=1)
cpf_cadastro_label.grid(row=9, column=0)
cpf_cadastro_entry.grid(row=9, column=1)
cep_cadastro_label.grid(row=10, column=0)
cep_cadastro_entry.grid(row=10, column=1)
cadastrar_usuario_button.grid(row=11, column=0)

criar_conta_corrente_label.grid(row=6, column=2)
cpf_conta_corrente_label.grid(row=7, column=2)
cpf_conta_corrente_entry.grid(row=7, column=3)
criar_conta_corrente_button.grid(row=8, column=2)

transferencia_label.grid(row=6, column=4)
numero_conta_origem_transferencia_label.grid(row=7, column=4)
numero_conta_origem_transferencia_entry.grid(row=7, column=5)
numero_conta_destino_transferencia_label.grid(row=8, column=4)
numero_conta_destino_transferencia_entry.grid(row=8, column=5)
valor_transferencia_label.grid(row=9, column=4)
valor_transferencia_entry.grid(row=9, column=5)
transferencia_button.grid(row=10, column=4)

consultar_saldo_label.grid(row=6, column=6)
numero_conta_saldo_label.grid(row=7, column=6)
numero_conta_saldo_entry.grid(row=7, column=7)
consultar_saldo_button.grid(row=8, column=6)

atualizar_limite_label.grid(row=11, column=2)
numero_conta_atualizar_limite_label.grid(row=12, column=2)
numero_conta_atualizar_limite_entry.grid(row=12, column=3)
novo_limite_label.grid(row=13, column=2)
novo_limite_entry.grid(row=13, column=3)
atualizar_limite_button.grid(row=14, column=2)
ajuda_limite_button.grid(row=14, column=3)

sair_button.grid(row=15, column=0, columnspan=8)

resultado_label.grid(row=16, column=0, columnspan=8)

# Adicionar campo para consultar conta por CPF
consultar_conta_por_cpf_label.grid(row=11, column=6)
cpf_consulta_label.grid(row=12, column=6)
cpf_consulta_entry.grid(row=12, column=7)
consultar_conta_button.grid(row=13, column=6)

# Iniciar a interface gráfica
root.mainloop()