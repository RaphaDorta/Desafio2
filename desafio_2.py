import textwrap 

# Função para exibir o menu e obter a opção do usuário
def menu():
    menu = '''\n
    ======= MENU ========
    [1]\tDEPOSITAR
    [2]\tSACAR
    [3]\tEXTRATO
    [4]\tNOVA CONTA
    [5]\tLISTAR CONTAS
    [6]\tNOVO USUÁRIO
    [0]\tSAIR         
    ==>'''
    return input(textwrap.dedent(menu))

# Função para realizar saques
def sacar(*, saldo, valor, extrato, limite, numero_saques, limite_saques):
    # Verifica se o valor do saque excede o saldo
    excedeu_saldo = valor > saldo
    # Verifica se o valor do saque excede o limite
    excedeu_limite = valor > limite
    # Verifica se o número de saques excede o limite
    excedeu_saques = numero_saques > limite_saques

    # Realiza as verificações e executa as ações correspondentes
    if excedeu_saldo:
        print("\n@@@ Operação falhou! Você não tem saldo suficiente. @@@")

    elif excedeu_limite:
        print("@@@ Operação falhou! O valor do saque excede o limite. @@@")
        
    elif excedeu_saques:
        print("\n @@@ Operação falhou! Número máximo de saques excedido. @@@")

    elif valor > 0 :
        saldo -= valor
        extrato += f"Saque: \t\t R$ - {valor:.2f}\n"
        numero_saques += 1
        print("\n=== Saque realizado com sucesso! ===")
        
    else: 
        print("\n@@@ Operação falhou! O valor informado é inválido. @@@")

    return saldo, extrato
 
# Função para realizar depósitos
def depositar(saldo, valor, extrato, /):
    if valor > 0:
        saldo += valor
        extrato += f"Depósito:\t R$ + {valor:.2f}\n"
        print("\n=== Depósito realizado com sucesso! ===")
    else:
        print("\n@@@ Operação falhou! O valor informado é inválido.@@@")

    return saldo, extrato
    
# Função para exibir o extrato da conta
def exibir_extrato(saldo, *, extrato=""):
    print("\n========== EXTRATO ============")
    print("Não foram realizadas movimentações" if not extrato else extrato)
    print(f"\nSaldo:\t\t R$ {saldo:.2f}")
    print("=======================")

# Função para criar um novo usuário
def criar_usuario(usuarios):
    # Solicita informações do usuário
    cpf = input("Informe o CPF(somente números): ")
    usuario = filtrar_usuarios(cpf, usuarios)
    
    if usuario:
        print("\n@@ Já existe usuário com esse CPF! @@@")
    
    nome = input("Informe o nome completo: ")
    data_nascimento = input("informe a data de nascimento (dd--mm--aaaa): ")
    endereco = input("Informe o endereço (logradoro, número - bairro - cidade/sigla do estado): ")
    
    # Adiciona o usuário à lista de usuários
    usuarios.append({"nome": nome, "data_nascimento": data_nascimento, "cpf": cpf, "endereco": endereco})
    
    print("=== Usuário criado com sucesso! ===")
    
# Função para filtrar usuários pelo CPF
def filtrar_usuarios(cpf, usuarios):
    # Filtra os usuários pela correspondência do CPF
    usuarios_filtrados = [usuario for usuario in usuarios if usuario["cpf"] == cpf]
    # Retorna o primeiro usuário encontrado, se houver, caso contrário retorna None
    return usuarios_filtrados[0] if usuarios_filtrados else None

# Função para criar uma nova conta
def criar_conta(agencia, numero_conta, usuarios):
    # Solicita o CPF do usuário para vincular a conta
    cpf = input("Informe o CPF do usuário: ")
    usuario = filtrar_usuarios(cpf, usuarios)
    
    if usuario:
        print("\n=== Conta criada com sucesso! ===")
        return {"agencia": agencia, "numero_conta": numero_conta, "usuario": usuario}
    
    print("\@@@ Usuário não encontrado, fluxo de criação de conta encerrado! @@@")

# Função para listar todas as contas
def listar_contas(contas):
    for conta in contas:
        # Formatação da linha para exibição da conta
        linha = f"""
            Agencia:\t{conta['agencia']}
            C/C:\t\t{conta['numero_conta']}
            Titular:\t{conta['usuario']['nome']}
        """
        # Exibe a linha formatada
        print("=" * 100)
        print(textwrap.dedent(linha))

# Função principal
def main():
    LIMITE_SAQUES = 3
    AGENCIA = "0001"

    saldo = 0
    limite = 500
    extrato = ""
    numero_saques = 0
    usuarios = []
    contas = []
    
    while True:
        # Obtém a opção do usuário a partir do menu
        opcao = menu()
        
        # Realiza ações de acordo com a opção selecionada pelo usuário
        if opcao == "1":
            valor = float(input("Informe o valor do depósito: "))

            saldo, extrato = depositar(saldo, valor, extrato)
            
        elif opcao == "2":
            valor = float(input("Informe o Valor do saque: "))

            saldo, extrato = sacar(
                saldo = saldo,
                valor = valor,
                extrato = extrato,
                limite = limite,
                numero_saques = numero_saques,
                limite_saques = LIMITE_SAQUES, # Corrigi o nome dos argumentos aqui
            )
        elif opcao == "3":
            exibir_extrato(saldo, extrato = extrato)
        
        elif opcao == "4":
            numero_conta = len(contas) + 1
            conta = criar_conta(AGENCIA, numero_conta, usuarios)
            
            if conta:
                contas.append(conta)
        
        elif opcao == "5":
            listar_contas(contas)
        
        elif opcao == "6":
            criar_usuario(usuarios)
        
        elif opcao == "0":
            break
