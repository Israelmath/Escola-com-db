from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout

class TestApp(App):
    
    def build(self, *args, **kwargs):
        box = BoxLayout()
        botao = Button(text = 'Sei lá')
        botao.bind(state = self.callback)
        box.add_widget(botao)
        return box

    def callback(self, instance, value, *args, **kwargs):
        print('My button <%s> state is <%s>' % (instance, value))

TestApp().run()