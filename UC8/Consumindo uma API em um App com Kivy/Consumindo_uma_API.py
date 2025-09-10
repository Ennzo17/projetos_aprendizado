import requests
import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.graphics import Color, Rectangle
from kivy.animation import Animation
import random

class JokeApp(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.spacing = 15
        self.padding = 30
        
        # Configurar fundo gradiente
        with self.canvas.before:
            Color(0.95, 0.95, 0.98, 1)
            self.rect = Rectangle(size=Window.size, pos=self.pos)
        self.bind(size=self._update_rect, pos=self._update_rect)
        
        # Logo/Ícone
        self.logo = Label(
            text='😂',
            font_size='40sp',
            size_hint=(1, 0.2)
        )
        self.add_widget(self.logo)
        
        # Título
        self.title_label = Label(
            text='[b]App de Piadas[/b]',
            markup=True,
            font_size='28sp',
            size_hint=(1, 0.15),
            color=(0.2, 0.2, 0.4, 1)
        )
        self.add_widget(self.title_label)
        
        # Container para a piada com fundo destacado
        self.joke_container = BoxLayout(
            orientation='vertical',
            size_hint=(1, 0.5),
            padding=20,
            spacing=10
        )
        with self.joke_container.canvas.before:
            Color(1, 1, 1, 1)
            self.joke_bg = Rectangle(pos=self.joke_container.pos, size=self.joke_container.size)
        self.joke_container.bind(size=self._update_joke_bg, pos=self._update_joke_bg)
        
        # Label para exibir a piada
        self.joke_label = Label(
            text='Clique no botão para ver uma piada!',
            font_size='18sp',
            size_hint=(1, 1),
            text_size=(Window.width - 100, None),
            halign='center',
            valign='middle',
            color=(0.1, 0.1, 0.1, 1),
            padding=(10, 10),
            markup=True
        )
        self.joke_label.bind(texture_size=self.joke_label.setter('size'))
        self.joke_container.add_widget(self.joke_label)
        self.add_widget(self.joke_container)
        
        # Botão para buscar piada
        self.joke_button = Button(
            text='Nova Piada',
            size_hint=(1, 0.15),
            background_color=(0.25, 0.6, 0.85, 1),
            background_normal='',
            color=(1, 1, 1, 1),
            font_size='20sp',
            bold=True
        )
        self.joke_button.bind(on_press=self.get_joke)
        self.add_widget(self.joke_button)
        
        # Status label
        self.status_label = Label(
            text='Pronto para rir!',
            font_size='14sp',
            size_hint=(1, 0.1),
            color=(0.4, 0.4, 0.4, 1)
        )
        self.add_widget(self.status_label)
        
        # Buscar primeira piada após 1 segundo
        Clock.schedule_once(lambda dt: self.get_joke(None), 1)

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size
        
    def _update_joke_bg(self, instance, value):
        self.joke_bg.pos = instance.pos
        self.joke_bg.size = instance.size

    def get_joke(self, instance):
        # Animação no botão
        anim = Animation(background_color=(0.2, 0.5, 0.75, 1), duration=0.1) + \
               Animation(background_color=(0.25, 0.6, 0.85, 1), duration=0.1)
        anim.start(self.joke_button)
        
        self.status_label.text = 'Buscando piada...'
        
        try:
            # Tentar primeiro uma API em português
            response = requests.get('https://piadas.deno.dev/random', timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                joke_text = f"{data.get('pergunta', '')}\n\n[color=#1a5fb4][b]{data.get('resposta', '')}[/b][/color]"
                self.display_joke(joke_text)
                self.status_label.text = 'Piada carregada!'
            else:
                # Se falhar, usar piadas locais em português
                self.status_label.text = 'Usando piadas locais...'
                self.show_portuguese_joke()
                
        except requests.exceptions.RequestException:
            # Sem conexão, usar piadas locais
            self.status_label.text = 'Sem conexão, usando piadas locais...'
            self.show_portuguese_joke()
        except Exception as e:
            self.status_label.text = f'Erro: {str(e)}'
            self.show_portuguese_joke()

    def display_joke(self, joke_text):
        # Animação para mostrar a piada
        anim = Animation(opacity=0, duration=0.3) + \
               Animation(opacity=1, duration=0.3)
        anim.start(self.joke_label)
        
        self.joke_label.text = joke_text

    def show_portuguese_joke(self):
        # Lista de piadas em português (pergunta e resposta)
        portuguese_jokes = [
            {
                "pergunta": "O professor disse que ninguém é inútil.",
                "resposta": "Aí eu lembrei do controle remoto que só aumenta o volume."
            },
            {
                "pergunta": "Qual é o café preferido do desenvolvedor?",
                "resposta": "Java!"
            },
            {
                "pergunta": "Por que os programadores preferem o modo escuro?",
                "resposta": "Porque a luz atrai bugs!"
            },
            {
                "pergunta": "Quantos programadores são necessários para trocar uma lâmpada?",
                "resposta": "Nenhum, é um problema de hardware!"
            },
            {
                "pergunta": "Ontem acordei tão feio…",
                "resposta": "Que meu espelho piscou a tela azul."
            },
            {
                "pergunta": "O professor pediu: “Escreva uma frase com ‘se’.",
                "resposta": "Se eu estudar, eu passo. Se eu não estudar… também não passo."
            },
            {
                "pergunta": "Por que a matemática é tão dramática?",
                "resposta": "Porque tem muitos problemas!"
            },
            {
                "pergunta": "O que um átomo disse para o outro?",
                "resposta": "Acho que perdemos um elétron!"
            },
            {
                "pergunta": "A Alexa da minha casa é igual minha ex.",
                "resposta": "Me ignora… mas quando eu falo errado, responde na hora."
            },
            {
                "pergunta": "Qual é o contrário de volátil?",
                "resposta": "Vem cá sobrinho!"
            }
        ]
        
        joke = random.choice(portuguese_jokes)
        joke_text = f"{joke['pergunta']}\n\n[color=#1a5fb4][b]{joke['resposta']}[/b][/color]"
        self.display_joke(joke_text)

class JokeAppMain(App):
    def build(self):
        self.title = 'App de Piadas em Português'
        Window.clearcolor = (0.95, 0.95, 0.98, 1)
        return JokeApp()

if __name__ == '__main__':
    JokeAppMain().run()