from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.lang import Builder
from os.path import join, dirname
from kivy.uix.image import Image

Builder.load_file(join(dirname(__file__), 'calendar.kv'))

class Calendario(GridLayout):
    pass

