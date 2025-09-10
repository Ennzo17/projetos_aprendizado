from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
from kivy.metrics import dp
from kivy.graphics import Color, Rectangle
from kivy.core.image import Image as CoreImage
from kivy.loader import Loader
import requests
from io import BytesIO
from kivy.clock import Clock

class BackgroundBoxLayout(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas.before:
            # Primeiro, adicionar a imagem de fundo
            self.bg_rect = Rectangle(size=self.size, pos=self.pos)
            # Depois, adicionar uma cor de fundo semi-transparente sobre a imagem
            Color(1, 1, 1, 0.8)  # Branco com 80% de opacidade
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self._update_rect, pos=self._update_rect)
    
    def _update_rect(self, instance, value):
        self.bg_rect.size = instance.size
        self.bg_rect.pos = instance.pos
        self.rect.size = instance.size
        self.rect.pos = instance.pos

    def set_background_texture(self, texture):
        self.bg_rect.texture = texture

class TaskApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.background_texture = None

    def build(self):
        # Layout principal que contém a imagem de fundo e a interface
        root_layout = BoxLayout()
        
        # Layout principal da interface com fundo semi-transparente
        self.main_layout = BackgroundBoxLayout(orientation='vertical', padding=dp(10), spacing=dp(10))
        
        # Título do aplicativo
        title = Label(
            text="Minha Lista de Tarefas", 
            size_hint=(1, 0.1),
            font_size='20sp',
            bold=True,
            color=(0, 0, 0, 1)  # Preto para melhor contraste com fundo claro
        )
        self.main_layout.add_widget(title)
        
        # Área de entrada de tarefas
        input_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.1), spacing=dp(5))
        
        self.task_input = TextInput(
            hint_text="Digite sua tarefa aqui...",
            multiline=False,
            size_hint=(0.7, 1),
            background_color=(1, 1, 1, 0.9)  # Fundo semi-transparente
        )
        input_layout.add_widget(self.task_input)
        
        # Botão para adicionar tarefa
        add_button = Button(
            text="Adicionar",
            size_hint=(0.3, 1),
            background_color=(0, 0.6, 0, 0.9)  # Verde com transparência
        )
        add_button.bind(on_press=self.add_task)
        input_layout.add_widget(add_button)
        
        self.main_layout.add_widget(input_layout)
        
        # Área para exibir mensagens de erro
        self.error_label = Label(
            text="",
            size_hint=(1, 0.05),
            color=(1, 0, 0, 1)  # Vermelho para mensagens de erro
        )
        self.main_layout.add_widget(self.error_label)
        
        # Área de scroll para a lista de tarefas
        scroll = ScrollView(size_hint=(1, 0.7))
        self.tasks_layout = BoxLayout(orientation='vertical', size_hint_y=None)
        self.tasks_layout.bind(minimum_height=self.tasks_layout.setter('height'))
        scroll.add_widget(self.tasks_layout)
        self.main_layout.add_widget(scroll)
        
        # Botão para limpar todas as tarefas
        clear_button = Button(
            text="Limpar Lista",
            size_hint=(1, 0.1),
            background_color=(0.8, 0, 0, 0.9)  # Vermelho com transparência
        )
        clear_button.bind(on_press=self.clear_tasks)
        self.main_layout.add_widget(clear_button)
        
        # Adicionar a interface sobre a imagem de fundo
        root_layout.add_widget(self.main_layout)
        
        # Carregar a imagem de fundo em segundo plano
        Clock.schedule_once(self.load_background, 0.1)
        
        return root_layout
    
    def load_background(self, dt):
        try:
            # Tentar carregar a imagem da URL
            response = requests.get('https://i.pinimg.com/736x/60/9b/6b/609b6bdda7afb8ce6949cbfe2d320548.jpg')
            image_data = BytesIO(response.content)
            texture = CoreImage(image_data, ext='jpg').texture
            self.main_layout.set_background_texture(texture)
        except:
            # Se não conseguir carregar da URL, usar um fundo colorido
            with self.main_layout.canvas.before:
                Color(0.9, 0.95, 1, 1)  # Azul claro
                self.main_layout.bg_rect = Rectangle(size=self.main_layout.size, pos=self.main_layout.pos)
                Color(1, 1, 1, 0.8)  # Branco com 80% de opacidade
                self.main_layout.rect = Rectangle(size=self.main_layout.size, pos=self.main_layout.pos)
            
            # Atualizar o retângulo quando o tamanho mudar
            self.main_layout.bind(size=self._update_bg_rect, pos=self._update_bg_rect)
    
    def _update_bg_rect(self, instance, value):
        instance.bg_rect.size = instance.size
        instance.bg_rect.pos = instance.pos
        instance.rect.size = instance.size
        instance.rect.pos = instance.pos
    
    def add_task(self, instance):
        task_text = self.task_input.text.strip()
        
        if task_text:
            # Criar um layout horizontal para cada tarefa
            task_row = BoxLayout(orientation='horizontal', 
                                size_hint_y=None, 
                                height=dp(40))
            
            # Adicionar fundo semi-transparente à tarefa
            with task_row.canvas.before:
                Color(1, 1, 1, 0.7)  # Branco com 70% de opacidade
                task_row.rect = Rectangle(size=task_row.size, pos=task_row.pos)
            task_row.bind(size=self._update_task_rect, pos=self._update_task_rect)
            
            # Label com a tarefa
            task_label = Label(
                text=task_text,
                size_hint=(0.8, 1),
                text_size=(None, None),
                halign='left',
                valign='middle',
                color=(0, 0, 0, 1)  # Texto preto para melhor contraste
            )
            task_label.bind(texture_size=task_label.setter('size'))
            task_row.add_widget(task_label)
            
            # Botão para remover a tarefa individualmente
            remove_button = Button(
                text="X",
                size_hint=(0.2, 1),
                background_color=(0.8, 0, 0, 0.9)  # Vermelho com transparência
            )
            remove_button.task_text = task_text  # Armazenar o texto da tarefa no botão
            remove_button.bind(on_press=self.remove_task)
            task_row.add_widget(remove_button)
            
            # Adicionar a tarefa à lista
            self.tasks_layout.add_widget(task_row)
            
            # Limpar o campo de entrada
            self.task_input.text = ""
            self.error_label.text = ""
        else:
            self.error_label.text = "Insira uma tarefa válida"
    
    def _update_task_rect(self, instance, value):
        instance.rect.size = instance.size
        instance.rect.pos = instance.pos
    
    def remove_task(self, instance):
        # Remover a tarefa específica
        self.tasks_layout.remove_widget(instance.parent)
    
    def clear_tasks(self, instance):
        # Limpar todas as tarefas
        self.tasks_layout.clear_widgets()
        self.error_label.text = ""

if __name__ == '__main__':
    # Configurar o tamanho da janela para melhor visualização
    Window.size = (400, 600)
    TaskApp().run()