from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button

class WelcomeApp(App):
    def build(self):
        self.title = "App de Boas-Vindas"

        self.layout = BoxLayout(orientation='vertical', padding=20, spacing=20)
        self.name_input = TextInput(hint_text="Digite seu nome aqui...",
                                    multiline=False,
                                    font_size=18)

        self.message_label = Label(text="",
                                   font_size=20,
                                   halign="center",
                                   valign="middle")
        self.message_label.bind(size=self.message_label.setter("text_size"))

        self.button = Button(
            text="Enviar",
            size_hint=(1, 0.3),
            font_size=18
        )

        self.button.bind(on_press=self.show_message)

        self.layout.add_widget(self.name_input)
        self.layout.add_widget(self.button)
        self.layout.add_widget(self.message_label)

        return self.layout

    def show_message(self, instance):
        nome = self.name_input.text.strip()
