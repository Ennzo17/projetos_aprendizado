from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import NumericProperty, ReferenceListProperty
from kivy.lang import Builder

# Carrega o arquivo KV
Builder.load_file("ref_list_prop.kv")

class MovableDot(Widget):
    # Posição inicial do ponto
    pos_x = NumericProperty(100)
    pos_y = NumericProperty(100)

    # Agrupa as duas propriedades como uma tupla (x, y)
    dot_pos = ReferenceListProperty(pos_x, pos_y)

    def move_left(self):
        self.pos_x -= 10

    def move_right(self):
        self.pos_x += 10

    def move_up(self):
        self.pos_y += 10

    def move_down(self):
        self.pos_y -= 10

class RefListPropRoot(BoxLayout):
    pass

class RefListPropApp(App):
    def build(self):
        return RefListPropRoot()

if __name__ == '__main__':
    RefListPropApp().run()
