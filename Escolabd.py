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

connection = sqlite3.connect('Alunos.db')

cursor = connection.cursor()

class Usuario:

    def __init__(self, id, nome, sobrenome, celular, cep):
        self.__id = id
        self.__nome = nome
        self.__sobrenome = sobrenome
        self.__celular = celular
        self.__cep = cep

    @property
    def celular(self):
        return self.__celular

    @property
    def sobrenome(self):
        return self.__sobrenome

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

    @celular.setter
    def celular(self, novo_celular):
        self.__celular = novo_celular

    @nome.setter
    def nome(self, novo_nome):
        self.__nome = novo_nome

    @sobrenome.setter
    def sobrenome(self, novo_sobrenome):
        self.__sobrenome = novo_sobrenome

    def __str__(self):
        return '{},{}'.format(self.nome, self.celular)


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
                print('\033[1;35mPrograma desligando2...\033[m')
                connection.close()
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
    print('\033[1;35mPrograma desligando3...\033[m')
    connection.close()
    exit()


def cria_aluno(id, nome, sobrenome, celular, cep):
    print('\033[35mAdicionando usuário no banco de dados. Aguarde...\033[m')
    user = Usuario(id, nome, sobrenome, celular, cep)
    guarda_no_bd(user)
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


def guarda_no_bd(usuario):

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS alunos (
            id TEXT NOT NULL,
            nome TEXT NOT NULL,
            sobrenome TEXT NOT NULL,
            celular TEXT NOT NULL,
            cep TEXT NOT NULL
        );
        ''')

    print(usuario.nome)
    cursor.execute(f'''
        INSERT INTO alunos (id, nome, sobrenome, celular, cep)
        VALUES ('{usuario.id}', '{usuario.nome}', '{usuario.sobrenome}', '{usuario.celular}', '{usuario.cep}')
    ''')

    connection.commit()


def imprime_usuarios_cadastrados():

    cursor.execute(f'''
        SELECT id, nome, sobrenome, celular, cep FROM alunos
    ''')
    if cursor.rowcount == 0:
        print('Nenhum aluno encontrado')
    else:
        for aluno in cursor.fetchall():
            print(aluno)


def usuario_existe(usuario):

    cursor.execute(f'''
        SELECT nome FROM alunos
        WHERE nome = '{usuario}'
    ''')

    print(cursor.rowcount)

    if cursor.rowcount != 0:
        return True
    else:
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
        usuario = Usuario(user[1], user[2], user[3], user[4])
        cadastro.append(usuario)
    usuarios = UsuariosCadastrados(cadastro)
    os.remove('/home/israel/Documentos/Cursos/Arquivos/lista_de_usuarios.csv')
    reinicia_programa()
    for user in usuarios:
        imprime_lista(user)


# def reinicia_programa():
#
#     cursor.execute('''
#         CREATE TABLE IF NOT EXISTS alunos (
#             id TEXT NOT NULL,
#             nome TEXT NOT NULL,
#             celular TEXT NOT NULL,
#             cep TEXT NOT NULL
#         );
#     ''')
#
#     cursor.execute(f'''
#         SELECT id, nome, celular, cep FROM alunos
#     ''')
#
#     cadastro = []
#     print(cursor.rowcount)
#     if cursor.rowcount == 0:
#         print('Não há alunos no banco de dados')
#     else:
#         for usuario in cursor.fetchall():
#             usuario = Usuario(usuario[1], usuario[2], usuario[3], usuario[4])
#             cadastro.append(usuario)
#         usuarios = UsuariosCadastrados(cadastro)
#
#         for usuario in usuarios:
#             print(usuario)
#     return usuarios


def main():

    cria_menu()
    choice = entrada_do_usuario()

    while True:

        if adiciona_aluno(choice):
            nome = input('Digite nome do aluno: ')
            sobrenome = input('Digite sobrenome do aluno: ')
            numero = input('Digite o telefone/celular do aluno: ')
            cep = input('Digite o cep do aluno: ')
            cria_aluno(randint(1000, 10000), nome, sobrenome, numero, cep)

        elif mostra_cadastro(choice):
            imprime_usuarios_cadastrados()

        else:
            print('\033[1;35mPrograma desligando1...\033[m')
            connection.close()
            exit()

        cria_menu()
        choice = entrada_do_usuario()


main()
