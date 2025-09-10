# Objetivo: Acessar e alterar uma propriedade de outro widget dentro de um principal.

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import BooleanProperty, ObjectProperty

class StatusIndicator(BoxLayout):
    is_active = BooleanProperty(False)

class MainControlWidget(BoxLayout):
    status_obj = ObjectProperty()

    def toggle_status(self):
        self.status_obj.is_active = not self.status_obj.is_active

class NestedPropApp(App):
    def build(self):
        return MainControlWidget()

if __name__ == '__main__':
    NestedPropApp().run()
