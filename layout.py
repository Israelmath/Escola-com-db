from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.popup import Popup
from kivy.uix.image import Image
from kivy.core.window import Window
from Individuos import Usuario
from Verificadores import mascara_celular, mascara_cep, certifica_cep
from random import randint
import Escolabd
import sqlite3

connection = sqlite3.connect('Alunos.db')

cursor = connection.cursor()

class Gerenciador(ScreenManager):
    def Sair(self, *args, **kwargs):
        MenuInicial.confirmacao(self, *args, **kwargs)

class MenuInicial(Screen):

    def on_pre_enter(self, *args, **kwargs):
        Window.bind(on_request_close = self.confirmacao)

    def confirmacao(self, *args, **kwargs):
        box = BoxLayout(padding = 5,
                        spacing = 5,
                        orientation = 'vertical')
        botoes = BoxLayout(padding = 5,
                        spacing = 15
                        )

        pop = Popup(title = 'Deseja mesmo sair?', 
            content = box,
            size_hint = (None, None),
            size = (300, 180)
            )

        sim = Button(text= 'Sim', on_release = App.get_running_app().stop)
        nao = Button(text= 'Não', on_release = pop.dismiss)

        botoes.add_widget(sim)
        botoes.add_widget(nao)

        atencao = Image(source = 'Images/error.png')
        
        box.add_widget(atencao)
        box.add_widget(botoes)

        pop.open()
        return True

    def on_pre_leave(self):
        Window.bind(on_keyboard = self.voltar)

    def voltar(self, window, key, *args):
        if key == 27:
            App.get_running_app().root.current = 'Tela inicial'
            return True



class ListaAlunosTela(Screen):
    def on_pre_enter(self, *args, **kwargs):
        self.atualiza()
        
        
    def atualiza(self, *args, **kwargs):    
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


class Aluno(BoxLayout):
    def __init__(self, id, nome, sobrenome, celular, cep, **kwargs):
        super().__init__()
        self.ids.Identificador.text = id
        self.ids.Nome.text = nome
        self.ids.Sobrenome.text = sobrenome
        self.ids.Celular.text = celular
        self.ids.Cep.text = cep

class AdicionaAlunoTela(Screen):

    def VerificaCep(self):
        # print(self.ids.CEP.text)
        endereco, bairro = certifica_cep(self.ids.CEP.text)
        # print(endereco, bairro)
        self.ids.Rua.text = endereco
        self.ids.Bairro.text = bairro


    def defineVariaveis(self):
        erro = 0
        
        if Escolabd.certifica_nome(self.ids.Nome.text):
            nome = self.ids.Nome.text
        else:
            print('Digite o nome novamente!')
            erro = 1

        if Escolabd.certifica_nome(self.ids.Sobrenome.text):
            sobrenome = self.ids.Sobrenome.text
        else: 
            print('Digite o sobrenome novamente!')
            erro = 1
        
        if Escolabd.certifica_celular(self.ids.Celular.text):
            celular = self.ids.Celular.text
        else:
            print('Digite o celular novamente!')
            erro = 1
        
        if Escolabd.certifica_cep(self.ids.CEP.text):
            cep = self.ids.CEP.text
        else:
            print('Digite o cep novamente!')
            erro = 1

        endereco = self.ids.Rua.text
        bairro = self.ids.Bairro.text

        print(f'Nome: {nome}')
        print(f'Sobrenome: {sobrenome}')
        print(f'Celular: {celular}')
        print(f'Cep: {cep}')
        print(f'Endereço: {endereco}')
        print(f'Bairro: {bairro}')
        
        if erro == 0:
            Escolabd.cria_aluno(randint(1000, 10000), nome, sobrenome, celular, cep)


class BuscaAlunoTela(Screen):

    def busca(self):
        aluno = self.ids.Aluno.text
        encontrados = Escolabd.encontra_aluno(aluno, from_layout = True)
        for aluno in encontrados:
            elemento = Aluno(id = aluno[0],
                            nome = aluno[1],
                            sobrenome = aluno[2],
                            celular = mascara_celular(aluno[3]),
                            cep = mascara_cep(aluno[4])
                            )
            self.ids.bigbox.add_widget(elemento)

class Escola(App):
    def build(self):
        return Gerenciador()

Escola().run()