# Objetivo: Criar um evento disparado quando uma propriedade muda.

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty

class MyCustomWidget(BoxLayout):
    message = StringProperty("")

    __events__ = ('on_message_changed',)

    def on_message(self, instance, value):
        # Quando a propriedade message muda, dispare o evento personalizado
        self.dispatch('on_message_changed', value)

    def on_message_changed(self, value):
        pass  # Pode ser tratado via .kv ou sobrescrito em subclasses

class CustomEventApp(App):
    def build(self):
        return MyCustomWidget()

if __name__ == '__main__':
    CustomEventApp().run()

