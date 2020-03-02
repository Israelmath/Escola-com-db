"""
Faça um programa que permita que o usuário entre com diversos nomes e telefones para cadastro e crie um arquivo com essas
informações.

Obs. No arquivo de saída, as informações de cada usuário deverão estar em uma linha

"""
from random import randint
import os
import pandas as pd
import sqlite3

SENHA = 'avaiana41'

connection = sqlite3.connect('/home/israel/Documentos/Cursos/Programas/Escola_com_db/alunos.db')

cursor = connection.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS alunos (
        id TEXT NOT NULL,
        nome TEXT NOT NULL,
        celular TEXT NOT NULL,
        cep TEXT NOT NULL
    );
''')

class Usuario:

    def __init__(self, id, nome, numero, cep):
        self.__id = id
        self.__nome = nome
        self.__numero = numero
        self.__cep = cep

    @property
    def numero(self):
        return self.__numero

    @property
    def cep(self):
        return self.__cep

    @property
    def id(self):
        return self.__id

    @property
    def nome(self):
        return self.__nome

    @id.setter
    def id(self, novo_id):
        self.__id = novo_id

    @numero.setter
    def numero(self, novo_numero):
        self.__numero = novo_numero

    @nome.setter
    def nome(self, novo_nome):
        self.__nome = novo_nome

    def __str__(self):
        return '{},{}'.format(self.nome, self.numero)


class UsuariosCadastrados(list):
    def __init__(self, usuarios):
        super().__init__(usuarios)


def cria_menu():
    print('\n', '\033[33m*' * 40)
    print('\n', '\033[33m*' * 6, '\033[34;7mDigite a opção que deseja\033[m', '\033[33m*' * 7)
    print('\n', '\033[33m*\033[m' * 2, '\033[34m    1 - Adicionar um usuário\033[m      ', '\033[33m*' * 2)
    print('\n', '\033[33m*\033[m' * 2, '\033[34m2 - Apresenta usuários cadastrados\033[m', '\033[33m*' * 2)
    print('\n', '\033[33m*\033[m' * 2, '\033[34m       3 - Excluir usuário\033[m        ', '\033[33m*' * 2)
    print('\n', '\033[33m*\033[m' * 2, '  \033[34m    0 - Sair do programa   \033[m     ', '\033[33m*' * 2)
    print('\n', '\033[33m*\033[m' * 40)
    print('\n', '\033[33m*\033[m' * 40, '\n')


def entrada_do_usuario():
    choice = ' '
    i = 0

    choice = input('-----> ')

    while i < 3:
        if choice.isnumeric():
            if choice == '0':
                print('\033[1;35mPrograma desligando...\033[m')
                exit()
            elif int(choice) in range(1, 4):
                return choice
            else:
                print('Você precisa digitar umas das opções apresentadas no menu acima.')
                print(f'Você tem mais {3 - i} chances')
                choice = input('-----> ')
        else:
            print('Você precisa digitar umas das opções apresentadas no menu acima.')
            print(f'Você tem mais {3 - i} chances')
            choice = input('-----> ')
        i += 1
    print('\033[1;35mPrograma desligando...\033[m')
    exit()


def mkuser(id, nome, numero):
    print('\033[35mAdicionando usuário no banco de dados. Aguarde...\033[m')
    user = Usuario(id, nome, numero)
    imprime_lista(user)
    return user


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

def exclui_usuario(choice):
    if choice == '3':
        return True
    else:
        return False


def imprime_lista(usuario):

    saida = open('/home/israel/Documentos/Cursos/Arquivos/lista_de_usuarios.csv', 'a')

    saida.write(str(usuario.id))
    saida.write(',')
    saida.write(str(usuario))
    saida.write('\n')

    saida.close()


def imprime_usuarios_cadastrados():
    data = pd.read_csv('/home/israel/Documentos/Cursos/Arquivos/lista_de_usuarios.csv')
    print(data.head())


def usuario_existe(usuario):
    if not os.path.exists('/home/israel/Documentos/Cursos/Arquivos/lista_de_usuarios.csv'):
        return False
    else:
        data = pd.read_csv('/home/israel/Documentos/Cursos/Arquivos/lista_de_usuarios.csv')
        i = 0
        for nome in data['Usuário']:
            if data['Usuário'][i] == usuario:
                i += 1
                return True
        return False


def deleta_usuario():
    delete = input('Qual usuário deseja excluir? (Nome ou Id): ')
    data = pd.read_csv('/home/israel/Documentos/Cursos/Arquivos/lista_de_usuarios.csv')


    if delete.isnumeric():
        try:
            delete = int(delete)
            index = data[data['Id'] == delete].index[0]
            print('\033[34mProcurando o Id do usuário...\033[m', '\n')
            print('Usuário encontrado:')
            print(index)
            print('\033[32m', data.iloc[index], '\033[m')
            data = data.drop(index)
            # print(data.head())
        except IndexError:
            print('Usuário não encontrado. Tente novamente.')
    else:
        try:
            index = data[data['Usuário'] == delete].index[0]
            print('\033[34mProcurando o nome do usuário...\033[m')
            print('Usuário encontrado:')
            print(index)
            print('\033[32m', data.iloc[index], '\033[m', '\n')
            data = data.drop(index)
            # print(data.head())
        except IndexError:
            print('Usuário não encontrado. Tente novamente.')

    atualiza_usuarios(data)


def atualiza_usuarios(data):
    print(data.head())
    cadastro = []
    for user in data.itertuples():
        usuario = Usuario(user[1], user[2], user[3])
        cadastro.append(usuario)
    usuarios = UsuariosCadastrados(cadastro)
    os.remove('/home/israel/Documentos/Cursos/Arquivos/lista_de_usuarios.csv')
    reinicia_programa()
    for user in usuarios:
        imprime_lista(user)


def reinicia_programa():

    if not os.path.exists('/home/israel/Documentos/Cursos/Arquivos/lista_de_usuarios.csv'):
        saida = open('/home/israel/Documentos/Cursos/Arquivos/lista_de_usuarios.csv', 'a')
        saida.write("Id,Usuário,Número")
        saida.write('\n')
    else:
        if os.path.exists('/home/israel/Documentos/Cursos/Arquivos/lista_de_usuarios.csv'):
            data = pd.read_csv('/home/israel/Documentos/Cursos/Arquivos/lista_de_usuarios.csv')
            cadastro = []
            for user in data.itertuples():
                usuario = Usuario(user[1], user[2], user[3])
                cadastro.append(usuario)
            usuarios = UsuariosCadastrados(cadastro)
            return usuarios


def main():

    data = reinicia_programa()
    cria_menu()
    choice = entrada_do_usuario()
    usuarios = []

    while True:
        if adiciona_aluno(choice):
            nome = input('Digite nome do usuário: ')
            numero = input('Digite o telefone do usuário: ')

            if usuario_existe(nome):
                print(f'\033[37mO usuário {nome} já existe\033[m.')
            else:
                user = mkuser(randint(1000, 10000), nome, numero)
                usuarios.append(user)

        if mostra_cadastro(choice):
            imprime_usuarios_cadastrados()

        if exclui_usuario(choice):
            deleta_usuario()

        cria_menu()
        choice = entrada_do_usuario()


    print('\033[1;35mPrograma desligando...\033[m')
    exit()


main()
