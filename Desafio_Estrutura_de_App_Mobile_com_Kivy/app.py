from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from kivy.lang import Builder
import os

# Importa as telas
from screens.home_screen import HomeScreen
from screens.tela1 import Tela1
from screens.tela2 import Tela2
from screens.tela3 import Tela3
from screens.tela4 import Tela4
from screens.tela5 import Tela5

class GerenciadorTelas(ScreenManager):
    pass

class MeuApp(App):
    def build(self):
        # Carrega o arquivo KV
        kv_path = os.path.join(os.path.dirname(__file__), "main.kv")
        Builder.load_file(kv_path)

        sm = GerenciadorTelas()
        sm.add_widget(HomeScreen(name="home"))
        sm.add_widget(Tela1(name="tela1"))
        sm.add_widget(Tela2(name="tela2"))
        sm.add_widget(Tela3(name="tela3"))
        sm.add_widget(Tela4(name="tela4"))
        sm.add_widget(Tela5(name="tela5"))

        return sm

if __name__ == "__main__":
    MeuApp().run()
