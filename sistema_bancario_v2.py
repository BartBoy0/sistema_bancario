
saldo = 0
LIMITE = 500
extrato = ""
numero_saques = 0
LIMITE_SAQUES = 3
AGENCIA="0001"
conta=""
entrou=False

menu = f"""

Conta{conta}

[d] Depositar
[s] Sacar
[e] Extrato
[q] Sair

=> """
menu_cadastro = """

[e] Entrar na conta
[c] Criar conta

=> """



def criar_usuario():
    pessoa={
    "nome":input("Digite seu nome:"),
    "dt_nasc":input("Digite sua data de nascimento:"),
    "cpf":input("Digite seu CPF:"),
    "endereco":f'{input("Digite seu logradouro:")}-{input("Digite o número da sua casa:")}-{input("Digite seu bairro:")}-{input("Digite sua cidade:")}/{input("Digite seu estado:")}',
    "contas":""
    }

    cadastro_certo=True
    for c in usuarios:
        if  pessoa["cpf"] == c["cpf"]:
            cadastro_certo = False
        else:
            cadastro_certo=True


    return pessoa,cadastro_certo






usuarios=[]

def sacar(saldo,saque,extrato,limite,numero_saques,limite_saques):
    if (saque < 0):
        print("Valor inválido")
    elif(saque>saldo):
        print("Valor acima do saldo")
    elif(saque>LIMITE):
        print("Valor acima do limite")
    elif(numero_saques>=LIMITE_SAQUES):
        print("Saques diários alcançados")
    else:
        saldo -=saque
        numero_saques+=1
        extrato += f'Saque: R${saque:.2f}\n'
        print("Saque realizado")
    return saldo,numero_saques,extrato



def depositar(saldo,deposito,extrato,/):
    if(deposito>0):
        saldo+=deposito
        extrato+=f'Deposito: R${deposito:.2f}\n'
        print("Deposito realizado")
    else:
        print("Valor inválido")
    return saldo,extrato


def tirar_extrato(saldo,/,*,extrato):
    print("Não foram realizadas movimentações.") if not extrato else print(f"Extrato... \n{extrato}\nSaldo atual:R${saldo:.2f}")
    return saldo,extrato



while True:
    while entrou==False:
        opcao=input(menu_cadastro)

        if opcao=="e":
            opcao=input("Digite o número da sua conta:")
            opcao2=opcao[4:]
            if AGENCIA+usuarios[int(opcao2)]["num_conta"] == opcao:
                entrou=True
                conta=opcao+usuarios[int(opcao2)]["nome"]
            else:
                print("Número inválido")
        elif opcao=="c":
            print("Cadastrando...")
            usuario_criar=criar_usuario()
            if usuario_criar[1]:
                usuarios.append(usuario_criar[0])
                usuarios[len(usuarios)-1]["num_conta"]=str(len(usuarios)-1)
                entrou=True
                conta=AGENCIA+usuarios[len(usuarios)-1]["num_conta"]+usuarios[len(usuarios)-1]["nome"]


            else:
                print("CPF já cadastrado")
        else:
            print("Opção inválida")

    menu = f"""

Conta:{conta}

[d] Depositar
[s] Sacar
[e] Extrato
[q] Sair

=> """

    opcao = input(menu)

    if opcao == "d":
        print("Realizando deposito...")
        deposito=float(input("Quanto deseja depositar? \n"))
        res= depositar(saldo,deposito,extrato)
        saldo=res[0]
        extrato=res[1]

    elif opcao == "s":
        print("Realizando saque...")
        saque = float(input("Quanto deseja sacar? \n"))
        res= sacar(saldo=saldo,saque=saque,extrato=extrato,limite=LIMITE,numero_saques=numero_saques,limite_saques=LIMITE_SAQUES)
        saldo=res[0]
        numero_saques=res[1]
        extrato=res[2]

    elif opcao == "e":
        res = tirar_extrato(saldo,extrato=extrato)
        saldo = res[0]
        extrato = res[1]

    elif opcao == "q":
        print("Saindo...")
        entrou=False

    else:
        print("Operação inválida, por favor selecione novamente a operação desejada.")