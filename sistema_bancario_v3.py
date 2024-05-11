from abc import ABC, abstractclassmethod, abstractproperty



class PessoaFIsica():
    def __init__(self,cpf,nome,data_nascimento):
        self._cpf=cpf
        self._nome=nome
        self._data_nascimento=data_nascimento

    @property
    def cpf(self):
        return self._cpf
    @property
    def nome(self):
        return self._nome
    @property
    def data_nascimento(self):
        return self._data_nascimento

class Cliente(PessoaFIsica):
    def __init__(self,cpf,nome,data_nascimento,endereco):
        super().__init__(cpf,nome,data_nascimento)
        self._endereco=endereco
        self._contas=[]

    @property
    def contas(self):
        return self._contas

    @property
    def endereco(self):
        return self._endereco

    def realizar_transacao(self,conta,transacao):
        transacao.registrar(conta)
    def adicionar_conta(self,conta):
        self._contas.append(conta)

class Conta():
    def __init__(self,numero,cliente):
        self._saldo=0
        self._numero=numero
        self._agencia="0001"
        self._cliente=cliente
        self._historico=Historico()

    @property
    def saldo(self):
        return self._saldo
    @property
    def numero(self):
        return self._numero
    @property
    def agencia(self):
        return self._agencia
    @property
    def cliente(self):
        return self._cliente
    @property
    def historico(self):
        return self._historico

    @classmethod
    def nova_conta(cls,cliente,numero):
        return cls(numero,cliente)


    def sacar(self,valor):
        saldo=self._saldo
        if(valor<0):
            print("Valor inválido")
            return False
        elif(valor>saldo):
            print("Valor excede saldo")
            return False
        else:
            self._saldo -= valor
            print("\n=== Saque realizado com sucesso! ===")
            return True

    def depositar(self,valor):
        if(valor<0):
            print("Valor inválido")
            return False
        else:
            self._saldo += valor
            print("\n=== Deposito realizado com sucesso! ===")
            return True



class ContaCorrente(Conta):
    def __init__(self,numero,cliente):
        self._limite=500
        self._limite_saques=3
        super().__init__(numero,cliente)

    def sacar(self,valor):
        numero_saques = len(
            {transacao for transacao in self.historico.
            transacoes if transacao["tipo"] == "Saque"}
        )
        
        if valor>self._limite:
            print("Valor acima do limite")
            return False
        elif numero_saques>=self._limite_saques:
            print("Atingiu o número máximo de saques")
            return False
        else:
            super().sacar(valor)
            return True

    def __str__(self):
        return f"""
                Agência:{self.agencia}
                Número:{self.numero}
                C/C:{self.numero}
                Titular:{self.cliente.nome}
        """

class Historico():
    def __init__(self):
        self._transacoes=[]

    @property
    def transacoes(self):
        return self._transacoes
    def adicionar_transacao(self,transacao):
        self._transacoes.append(
            {
                "tipo": transacao.__class__.__name__,
                "valor": transacao.valor
            }
        )

class Transacao(ABC):
    @property
    @abstractproperty
    def valor(self):
        pass

    @abstractclassmethod
    def registrar(self, conta):
        pass

class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        sucesso_transacao = conta.sacar(self.valor)
        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)


class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        sucesso_transacao = conta.depositar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)



def menu():
    menu = """\n
    ================ MENU ================
    [d]\tDepositar
    [s]\tSacar
    [e]\tExtrato
    [nc]\tNova conta
    [lc]\tListar contas
    [nu]\tNovo usuário
    [q]\tSair
    => """
    return input(menu)



def filtrar_usuario(cpf, usuarios):
    usuarios_filtrados = [usuario for usuario in usuarios if usuario.cpf == cpf]
    return usuarios_filtrados[0] if usuarios_filtrados else None






def criar_usuario(usuarios):
    cpf = input("Informe o CPF (somente número): ")
    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
        print("\n@@@ Já existe cliente com esse CPF! @@@")
        return

    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
    endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ")

    usuario = Cliente(nome=nome, data_nascimento=data_nascimento, cpf=cpf, endereco=endereco)

    usuarios.append(usuario)

    print("\n=== Usuário criado com sucesso! ===")




def criar_conta(usuarios,numero_conta,contas):
    cpf = input("Informe o CPF (somente número): ")
    usuario = filtrar_usuario(cpf, usuarios)

    if not usuario:
        print("\n@@@ Usuário não encontrado! @@@")
        return


    conta = ContaCorrente.nova_conta(usuario,numero_conta)

    contas.append(conta)
    usuario.contas.append(conta)

    print("\n=== Conta criado com sucesso! ===")



def listar_contas(contas):
    for conta in contas:
        print(f''' {conta} ''')
        print("+"*50)


def escolher_conta(contas,usuarios,usuario):
    if usuario:
        for conta in contas:
            if usuario.cpf==conta.cliente.cpf:
                print(f''' {conta} ''')
                print("+"*50)
    else:
        print("Usuário não encontrado")
        return False
    opcao=int(input("Qual conta você escolhe?\t"))
    numeros_contas=[conta.numero for conta in contas if usuario.cpf == conta.cliente.cpf]
    if opcao in numeros_contas:
        print("Sucesso escolhendo a conta")
        conta_escolhida=[conta for conta in contas if opcao == conta.numero]

        return conta_escolhida[0]
    else:
        print("Conta não encontrada")
        return False





def exibir_extrato(conta):
    transacoes=conta.historico.transacoes
    extrato = ""
    print("\n================ EXTRATO ================")
    if not transacoes:
        extrato = "Não foram realizadas movimentações."
    else:
        for transacao in transacoes:
            extrato += f"\n{transacao['tipo']}:\t\tR$ {transacao['valor']:.2f}"

    print(extrato)
    print(f"\nSaldo:\t\tR$ {conta.saldo}")
    print("==========================================")
'''
def depositar(conta):
    valor = float(input("Informe o valor do saque: "))
    transacao = Deposito(valor)
    usuario.realizar_transacao(conta_escolhida, transacao)
def sacar(conta):
    valor = float(input("Informe o valor do saque: "))
    transacao = Saque(valor)

    usuario.realizar_transacao(conta_escolhida, transacao)
def main():
    usuarios=[]
    contas=[]
'''




































def main():
    usuarios = []
    contas = []
    while True:
        opcao=menu()

        if opcao == "d":
            cpf = input("Informe o CPF (somente número): ")
            usuario = filtrar_usuario(cpf, usuarios)
            conta_escolhida=escolher_conta(contas,usuarios,usuario)
            if conta_escolhida:
                valor = float(input("Informe o valor do depósito: "))
                transacao = Deposito(valor)
                usuario.realizar_transacao(conta_escolhida, transacao)
        elif opcao == "s":
            cpf = input("Informe o CPF (somente número): ")
            usuario = filtrar_usuario(cpf, usuarios)
            conta_escolhida=escolher_conta(contas,usuarios,usuario)
            if conta_escolhida:
                valor = float(input("Informe o valor do saque: "))
                transacao = Saque(valor)

                usuario.realizar_transacao(conta_escolhida, transacao)

        elif opcao == "e":
            cpf = input("Informe o CPF (somente número): ")
            usuario = filtrar_usuario(cpf, usuarios)
            conta_escolhida=escolher_conta(contas,usuarios,usuario)
            if conta_escolhida:
                exibir_extrato(conta_escolhida)



        elif opcao == "nu":
            criar_usuario(usuarios)

        elif opcao == "nc":
            numero_conta =len(contas)+1
            criar_conta(usuarios,numero_conta,contas)

        elif opcao == "lc":
            listar_contas(contas)

        elif opcao == "q":
            break

        else:
            print("Operação inválida, por favor selecione novamente a operação desejada.")

main()