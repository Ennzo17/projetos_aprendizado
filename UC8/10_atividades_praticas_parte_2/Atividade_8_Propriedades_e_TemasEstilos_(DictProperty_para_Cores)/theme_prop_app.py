from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import DictProperty
from kivy.lang import Builder

# Carrega o KV
Builder.load_file("theme_prop.kv")


class ThemeRoot(BoxLayout):
    pass


class ThemedApp(App):
    # Tema atual da aplicação
    app_theme = DictProperty({
        'primary': [0.2, 0.6, 0.8, 1],
        'secondary': [0.9, 0.9, 0.9, 1]
    })

    def build(self):
        return ThemeRoot()

    def toggle_theme(self):
        # Alterna entre dois temas
        if self.app_theme['primary'] == [0.2, 0.6, 0.8, 1]:
            self.app_theme = {
                'primary': [0.8, 0.3, 0.3, 1],
                'secondary': [0.2, 0.2, 0.2, 1]
            }
        else:
            self.app_theme = {
                'primary': [0.2, 0.6, 0.8, 1],
                'secondary': [0.9, 0.9, 0.9, 1]
            }


if __name__ == "__main__":
    ThemedApp().run()
