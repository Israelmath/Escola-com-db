from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen

class Gerenciador(ScreenManager):
    pass

class MenuInicial(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

class AdicionaAlunoTela(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        pass

    def defineVariaveis(self):
        nome = self.ids.Nome.text
        print(nome)

class Escola(App):
    def build(self):
        return Gerenciador()

Escola().run()