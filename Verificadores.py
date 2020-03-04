import requests


def adiciona_aluno(choice):
    if choice == '1':
        return True
    else:
        return False


def mostra_cadastro(choice):
    if choice == '2':
        return True
    else:
        return False


def busca_aluno(choice):
    if choice == '3':
        return True
    else:
        return False


def exclui_usuario(choice):
    if choice == '4':
        return True
    else:
        return False


def certifica_nome(nome):
    if nome.isalpha():
        return True
    else:
        print('\033[36mUsuário não pôde ser cadastrado. Nome inválido.\033[m')
        return False


def certifica_celular(numero):
    if len(numero) != 11:
        print('\033[36mNúmero errado ou código de área faltante.\033[m')
        return False
    else:
        return True


def certifica_cep(cep):

    if len(cep) == 8 and confere_endereco(cep):
        return True
    else:
        print('\033[36mCEP incorreto.\033[m')
        return False


def mascara_celular(numero):
    numero_correto = f'({numero[:2]}) {numero[2:6]}-{numero[6:]}'
    return numero_correto


def mascara_cep(cep):
    cep_correto = f'{cep[:5]}-{cep[5:]}'
    return cep_correto


def confere_endereco(cep):
    r = requests.get('http://www.viacep.com.br/ws/' + cep + '/json/')
    endereco = r.json()['logradouro']
    bairro = r.json()['bairro']
    print('\033[34m\n', endereco, '\n', bairro, '\n \033[m')
    confirmacao = input('O endereco está correto? (S/n): ').lower()

    if confirmacao == 's':
        return True
    else:
        return False


def busca_endereco(cep):
    r = requests.get('http://www.viacep.com.br/ws/03069000/json/')
    endereco = r.json()['logradouro']
    return endereco


def busca_bairro(cep):
    r = requests.get('http://www.viacep.com.br/ws/03069000/json/')
    bairro = r.json()['bairro']
    return bairro