from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout

class HelloWorldApp(App):
    def build(self):
        # Criar um layout para centralizar o texto
        layout = BoxLayout()
        
        # Criar o label com a mensagem
        label = Label(
            text="Hello, World!",
            font_size='40sp',
            color=(1, 1, 1, 1)  # Cor branca
        )
        
        # Adicionar o label ao layout
        layout.add_widget(label)
        
        return layout

# Executar a aplicação
if __name__ == '__main__':
    HelloWorldApp().run()