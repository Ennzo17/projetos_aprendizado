from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button


class WelcomeApp(App):
    def build(self):
        # Layout principal (vertical)
        layout = BoxLayout(orientation="vertical", padding=20, spacing=10)

        # Campo de entrada
        self.input_name = TextInput(
            hint_text="Digite seu nome",
            multiline=False,
            size_hint=(1, 0.3)
        )
        layout.add_widget(self.input_name)

        # Botão
        self.button = Button(
            text="Enviar",
            size_hint=(1, 0.3)
        )
        self.button.bind(on_press=self.mostrar_mensagem)
        layout.add_widget(self.button)

        # Label (saída da mensagem)
        self.output_label = Label(
            text="",
            font_size=20
        )
        layout.add_widget(self.output_label)

        return layout

    def mostrar_mensagem(self, instance):
        nome = self.input_name.text.strip()
        if nome:
            self.output_label.text = f"Bem-vindo(a), {nome}!"
        else:
            self.output_label.text = "Por favor, digite seu nome."


if __name__ == "__main__":
    WelcomeApp().run()