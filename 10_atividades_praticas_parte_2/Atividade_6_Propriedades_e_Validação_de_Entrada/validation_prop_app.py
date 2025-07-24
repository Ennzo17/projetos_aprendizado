from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty
from kivy.lang import Builder

# Carrega o arquivo KV diretamente
Builder.load_file("validation_prop.kv")


class ValidatedInputWidget(BoxLayout):
    # Propriedade de texto validado
    validated_text = StringProperty("Texto válido aparecerá aqui.")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._last_valid_text = self.validated_text

    def on_validated_text(self, instance, value):
        # Validação: mínimo 5 letras e sem números
        if len(value) >= 5 and not any(char.isdigit() for char in value):
            self._last_valid_text = value
        else:
            self.validated_text = self._last_valid_text


class ValidationPropApp(App):
    def build(self):
        return ValidatedInputWidget()


if __name__ == '__main__':
    ValidationPropApp().run()
