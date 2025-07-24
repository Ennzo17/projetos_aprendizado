from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import DictProperty
from kivy.lang import Builder

# Carrega o layout do arquivo KV (interface gráfica)
Builder.load_file("dict_prop.kv")

class UserProfileWidget(BoxLayout):
    """
    Classe que representa o perfil do usuário na interface.
    Herda de BoxLayout para organizar os widgets verticalmente.
    """

    # Propriedade do tipo dicionário com dados iniciais do usuário
    user_data = DictProperty({
        'name': 'João',
        'age': 30,
        'city': 'São Paulo'
    })

    def update_age(self):
        """
        Incrementa a idade do usuário em 1.
        Como user_data é uma DictProperty, a interface será atualizada automaticamente.
        """
        self.user_data['age'] += 1

class DictPropApp(App):
    """
    Classe principal da aplicação.
    Responsável por construir e executar o aplicativo.
    """
    def build(self):
        # Retorna o widget principal da interface
        return UserProfileWidget()

# Ponto de entrada da aplicação
if __name__ == "__main__":
    DictPropApp().run()
