from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import NumericProperty, AliasProperty
from kivy.lang import Builder

# Carrega o arquivo KV
Builder.load_file("alias_prop.kv")

class CalculatorWidget(BoxLayout):
    """
    Widget calculadora com propriedades baseadas em AliasProperty.
    """

    # Propriedades numéricas principais
    num1 = NumericProperty(10)
    num2 = NumericProperty(5)

    # Função GET para a soma
    def get_sum(self):
        return self.num1 + self.num2

    # AliasProperty (somente leitura)
    sum_result = AliasProperty(get_sum, None, bind=('num1', 'num2'))

class AliasPropApp(App):
    def build(self):
        return CalculatorWidget()

if __name__ == '__main__':
    AliasPropApp().run()
