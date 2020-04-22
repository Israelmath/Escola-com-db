from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.popup import Popup
from kivy.uix.image import Image
from kivy.core.window import Window
from Calendar import Calendario
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

class Calendar(Calendario):
    pass

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

    def on_leave(self, *args):
        self.ids.bigbox.clear_widgets()


class Aluno(BoxLayout):
    def __init__(self, id, nome, sobrenome, celular, cep, **kwargs):
        super().__init__()
        self.ids.Identificador.text = id
        self.ids.Nome.text = nome
        self.ids.Sobrenome.text = sobrenome
        self.ids.Celular.text = celular
        self.ids.Cep.text = cep

    def ExcluiDados(self):
        Escolabd.deleta_usuario(self.ids.Nome.text, from_layout= True)
        self.clear_widgets()
        self.canvas.before.clear()
    
    def confere_exclusao(self):
        confirma_exclusao_popup(self)


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

        
        if erro == 0:
            Escolabd.cria_aluno(randint(1000, 10000), nome, sobrenome, celular, cep)


class BuscaAlunoTela(Screen):

    def busca(self):
        aluno = self.ids.Aluno.text
        encontrados = Escolabd.encontra_aluno(aluno, from_layout = True)
        if len(encontrados) == 0:
            AlunoNaoEncontrado()
        else:
            for aluno in encontrados:
                elemento = Aluno(id = aluno[0],
                                nome = aluno[1],
                                sobrenome = aluno[2],
                                celular = mascara_celular(aluno[3]),
                                cep = mascara_cep(aluno[4])
                                )
                self.ids.bigbox.add_widget(elemento)
        self.ids.Aluno.text = ''


    def on_leave(self, *args):
        self.ids.bigbox.clear_widgets()
        self.ids.Aluno.text = ''


class Escola(App):
    def build(self):
        return Gerenciador()

def AlunoNaoEncontrado(*args, **kwargs):
    pop = Popup(title= 'Algo de errado não está certo...', 
                content = Label(text = '''Infelizmente não encontramos\n o(a) aluno(a) que procurava. Tente novamente.'''),
                                size_hint = (None, None),
                                size = (400,150)
                            )

    pop.open()


def confirma_exclusao_popup(self, *args, **kwargs):
    aluno = self

    def callback(instance, value):
        if value == 'down':
            Aluno.ExcluiDados(aluno)

    box = BoxLayout()
    pop = Popup(title= 'Algo de errado não está certo...', 
            content = box,
            size_hint = (None, None),
            size = (400,150)
                        )

    botaosim = Button(text = 'Sim', on_release = pop.dismiss)
    botaonao = Button(text = 'Não', on_release = pop.dismiss)

    botaosim.bind(state = callback)

    box.add_widget(botaosim)
    box.add_widget(botaonao)

    pop.open()

Escola().run()