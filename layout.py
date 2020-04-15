from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from Individuos import Usuario
from Verificadores import mascara_celular, mascara_cep
import Escolabd
import sqlite3

connection = sqlite3.connect('Alunos.db')

cursor = connection.cursor()

class Gerenciador(ScreenManager):
    pass

class MenuInicial(Screen):
    def __init__(self, **kwargs):
        super().__init__()

class AdicionaAlunoTela(Screen):
    def __init__(self, **kwargs):
        super().__init__()
        pass

    def defineVariaveis(self):
        nome = self.ids.Nome.text
        if not Escolabd.certifica_nome(nome):
            print('Digite o nome novamente!')
        sobrenome = self.ids.Sobrenome.text
        if not Escolabd.certifica_nome(sobrenome):
            print('Digite o sobrenome novamente!')
        celular = self.ids.Celular.text
        if not Escolabd.certifica_celular(celular):
            print('Digite o celular novamente!')
        cep = self.ids.CEP.text
        if not Escolabd.certifica_cep(cep):
            print('Digite o cep novamente!')


class ListaAlunosTela(Screen):
    def __init__(self, alunos = [ ], **kwargs):
        super().__init__()
        
        cursor.execute(f'''
            SELECT id, nome, sobrenome, celular, cep, endereco, bairro FROM alunos
        ''')
        if cursor.rowcount == 0:
            print('Nenhum aluno encontrado')
        else:
            for aluno in cursor.fetchall():
                self.ids.bigbox.add_widget(Aluno(id = aluno[0],
                                                nome = aluno[1],
                                                sobrenome = aluno[2],
                                                celular = mascara_celular(aluno[3]),
                                                cep = mascara_cep(aluno[4])
                                                )
                                            )

    
    # def adicionaWidget(self, aluno):
    #     self.ids.box.add_widget(Aluno(id = aluno[0],
    #                                 nome = aluno[1],
    #                                 sobrenome = aluno[2],
    #                                 celular = mascara_celular(aluno[3]),
    #                                 cep = mascara_cep(aluno[4])
    #                                 )
    #                             )
    #     print(aluno)


class Aluno(BoxLayout):
    def __init__(self, id, nome, sobrenome, celular, cep, **kwargs):
        super().__init__()
        self.ids.Identificador.text = id
        self.ids.Nome.text = nome
        self.ids.Sobrenome.text = sobrenome
        self.ids.Celular.text = celular
        self.ids.Cep.text = cep


class Escola(App):
    def build(self):
        return Gerenciador()

Escola().run()