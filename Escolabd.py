"""
Faça um programa que permita que o usuário entre com diversos nomes e telefones para cadastro e crie um arquivo com essas
informações.

Obs. No arquivo de saída, as informações de cada usuário deverão estar em uma linha

"""
from random import randint
from Individuos import Usuario
from Verificadores import *
import sqlite3

SENHA = 'avaiana41'

connection = sqlite3.connect('Alunos.db')

cursor = connection.cursor()


def cria_menu():
    print(' ')
    print('\033[33m*' * 6, '\033[34;7mDigite a opção que deseja\033[m', '\033[33m*' * 7)
    print('\033[33m*\033[m' * 2, '\033[34m    1 - Adicionar um usuário\033[m      ', '\033[33m*' * 2)
    print('\033[33m*\033[m' * 2, '\033[34m2 - Apresenta usuários cadastrados\033[m', '\033[33m*' * 2)
    print('\033[33m*\033[m' * 2, '\033[34m       3 - Busca aluno\033[m            ', '\033[33m*' * 2)
    print('\033[33m*\033[m' * 2, '\033[34m      4 - Excluir aluno\033[m           ', '\033[33m*' * 2)
    print('\033[33m*\033[m' * 2, '  \033[34m  0 - Sair do programa     \033[m     ', '\033[33m*' * 2)
    print('\033[33m*\033[m' * 40, '\n')


def entrada_do_usuario():
    choice = input('-----> ')

    i = 0
    while i < 3:
        if choice.isnumeric():
            if choice == '0':
                print('\033[1;35mPrograma desligando...\033[m')
                connection.close()
                exit()
            elif int(choice) in range(1, 5):
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
    connection.close()
    exit()


def cria_aluno(id, nome, sobrenome, celular, cep):
    print('\033[35mAdicionando usuário no banco de dados. Aguarde...\033[m')
    user = Usuario(id, nome, sobrenome, celular, cep)
    guarda_no_bd(user)
    return user


def guarda_no_bd(usuario):
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS alunos (
            id TEXT NOT NULL,
            nome TEXT NOT NULL,
            sobrenome TEXT NOT NULL,
            celular TEXT NOT NULL,
            cep TEXT NOT NULL,
            endereco TEXT NOT NULL,
            bairro TEXT NOT NULL
        );
        ''')

    cursor.execute(f'''
        INSERT INTO alunos (id, nome, sobrenome, celular, cep, endereco, bairro)
        VALUES ('{usuario.id}', '{usuario.nome}', '{usuario.sobrenome}', '{usuario.celular}', '{usuario.cep}', '{usuario.endereco}', '{usuario.bairro}')
    ''')

    connection.commit()


def imprime_usuarios_cadastrados():
    cursor.execute(f'''
        SELECT id, nome, sobrenome, celular, cep, endereco, bairro FROM alunos
    ''')
    if cursor.rowcount == 0:
        print('Nenhum aluno encontrado')
    else:
        for aluno in cursor.fetchall():
            imprime_framework_de_aluno(aluno)


def imprime_framework_de_aluno(aluno):
    print(f'\033[35mNúmero de cadastro Id: {aluno[0]}------\033[m')
    print(f'Nome do(a) aluno(a): {aluno[1]} {aluno[2]}')
    print(f'Número do celular: {mascara_celular(aluno[3])}')
    print(f'CEP: {mascara_cep(aluno[4])}')
    print(f'Endereço: {aluno[5]}')
    print(f'Bairro: {aluno[6]}')
    print(' ')


def usuario_existe(usuario):
    cursor.execute(f'''
        SELECT nome FROM alunos
        WHERE nome = '{usuario}'
    ''')

    if cursor.rowcount != 0:
        return True
    else:
        return False


def busca_por_numero(busca):
    cursor.execute(f'''
                SELECT id, nome, sobrenome, celular, cep, endereco, bairro FROM alunos
                WHERE id = '{busca}'   
            ''')
    encontrados = cursor.fetchall()

    if len(encontrados) == 0:
        cursor.execute(f'''
                    SELECT id, nome, sobrenome, celular, cep, endereco, bairro FROM alunos
                    WHERE celular = '{busca}'   
                ''')
        encontrados = cursor.fetchall()

    if len(encontrados) == 0:
        cursor.execute(f'''
                    SELECT id, nome, sobrenome, celular, cep, endereco, bairro FROM alunos
                    WHERE cep = '{busca}'   
                ''')
        encontrados = cursor.fetchall()

    if len(encontrados) == 0:
        print('\033[36mO(a) aluno(a) não foi encontrado(a).\033[m')
        return []

    return encontrados


def busca_por_nome(busca):
    cursor.execute(f'''
        SELECT id, nome, sobrenome, celular, cep, endereco, bairro FROM alunos
        WHERE nome = '{busca}'   
    ''')
    encontrados = cursor.fetchall()

    if len(encontrados) == 0:
        cursor.execute(f'''
            SELECT id, nome, sobrenome, celular, cep, endereco, bairro FROM alunos
            WHERE sobrenome = '{busca}'   
        ''')
        encontrados = cursor.fetchall()

    if len(encontrados) == 0:
        cursor.execute(f'''
            SELECT id, nome, sobrenome, celular, cep, endereco, bairro FROM alunos
            WHERE endereco = '{busca}'   
        ''')
        encontrados = cursor.fetchall()

    if len(encontrados) == 0:
        cursor.execute(f'''
            SELECT id, nome, sobrenome, celular, cep, endereco, bairro FROM alunos
            WHERE bairro = '{busca}'   
        ''')
        encontrados = cursor.fetchall()

    if len(encontrados) == 0:
        print('\033[36mO(a) aluno(a) não foi encontrado(a).\033[m')
        return []

    return encontrados


def encontra_aluno(busca=False):
    if not busca:
        busca = input('Qual aluno deseja buscar? (Nome ou Id): ')

    if busca.isnumeric():
        encontrados = busca_por_numero(busca)

    else:
        encontrados = busca_por_nome(busca)

    if len(encontrados) != 0:
        for aluno in encontrados:
            imprime_framework_de_aluno(aluno)


def deleta_usuario():
    delete = input('Qual usuário deseja excluir? (Nome ou Id): ')
    encontra_aluno(delete)

    if delete.isnumeric():
        if verifica_exclusao():
            cursor.execute(f'''
                DELETE FROM alunos
                WHERE id = '{delete}'            
            ''')
            if cursor.rowcount == -1:
                print('\033[34mAluno(a) não encontrado(a).\033[m')
    else:
        if verifica_exclusao():
            cursor.execute(f'''
                DELETE FROM alunos
                WHERE nome = '{delete}'
            ''')
            if cursor.rowcount == -1:
                print('\033[34mAluno(a) não encontrado(a).\033[m')

    connection.commit()


def main():
    cria_menu()
    choice = entrada_do_usuario()

    while True:

        if adiciona_aluno(choice):

            nome = input('Digite nome do aluno: ')
            while not certifica_nome(nome):
                nome = input('Digite nome do aluno: ')

            sobrenome = input('Digite sobrenome do aluno: ')
            while not certifica_nome(sobrenome):
                sobrenome = input('Digite sobrenome do aluno: ')

            celular = input('Digite o telefone/celular do aluno: ')
            while not certifica_celular(celular):
                celular = input('Digite o telefone/celular do aluno: ')

            cep = input('Digite o cep do aluno: ')
            while not certifica_cep(cep):
                cep = input('Digite o cep do aluno: ')

            cria_aluno(randint(1000, 10000), nome, sobrenome, celular, cep)

        elif mostra_cadastro(choice):
            imprime_usuarios_cadastrados()

        elif busca_aluno(choice):
            encontra_aluno()

        elif exclui_usuario(choice):
            deleta_usuario()

        else:
            print('\033[1;35mPrograma desligando...\033[m')
            connection.close()
            exit()

        cria_menu()
        choice = entrada_do_usuario()


main()
