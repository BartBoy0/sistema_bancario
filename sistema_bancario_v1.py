menu = """

[d] Depositar
[s] Sacar
[e] Extrato
[q] Sair

=> """

saldo = 0
LIMITE = 500
extrato = ""
numero_saques = 0
LIMITE_SAQUES = 3

while True:

    opcao = input(menu)

    if opcao == "d":
        print("Realizando deposito...")
        deposito=float(input("Quanto deseja depositar? \n"))
        if(deposito>0):
            saldo+=deposito
            extrato+=f'Deposito: R${deposito:.2f}\n'
            print("Deposito realizado")
        else:
            print("Valor inválido")

    elif opcao == "s":
        print("Realizando saque...")
        saque = float(input("Quanto deseja sacar? \n"))
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


    elif opcao == "e":
        print("Não foram realizadas movimentações.")if not extrato else print(f"Extrato... \n{extrato}\nSaldo atual:R${saldo:.2f}")


    elif opcao == "q":
        print("Saindo...")
        break

    else:
        print("Operação inválida, por favor selecione novamente a operação desejada.")