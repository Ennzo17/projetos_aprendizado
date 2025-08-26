import random
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner
from kivy.uix.image import AsyncImage
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle
from kivy.utils import get_color_from_hex
from kivy.metrics import dp

# Lista de filmes por gênero com URLs de imagens reais
filmes_por_genero = {
    "Ação": [
        {"titulo": "Matrix", "ano": 1999, "imagem": "https://m.media-amazon.com/images/M/MV5BNzQzOTk3OTAtNDQ0Zi00ZTVkLWI0MTEtMDllZjNkYzNjNTc4L2ltYWdlXkEyXkFqcGdeQXVyNjU0OTQ0OTY@._V1_FMjpg_UX1000_.jpg"},
        {"titulo": "Mad Max: Estrada da Fúria", "ano": 2015, "imagem": "https://m.media-amazon.com/images/M/MV5BN2EwM2I5OWMtMGQyMi00Zjg1LWJkNTctZTdjYTA4OGUwZjMyXkEyXkFqcGdeQXVyMTMxODk2OTU@._V1_FMjpg_UX1000_.jpg"},
        {"titulo": "John Wick", "ano": 2014, "imagem": "https://m.media-amazon.com/images/M/MV5BMTU2NjA1ODgzMF5BMl5BanBnXkFtZTgwMTM2MTI4MjE@._V1_FMjpg_UX1000_.jpg"},
        {"titulo": "Duro de Matar", "ano": 1988, "imagem": "https://m.media-amazon.com/images/M/MV5BZjRlNDUxZjAtOGQ4OC00OTNlLTgxNmQtYTBmMDgwZmNmNjkxXkEyXkFqcGdeQXVyNzkwMjQ5NzM@._V1_FMjpg_UX1000_.jpg"},
        {"titulo": "Missão Impossível", "ano": 1996, "imagem": "https://m.media-amazon.com/images/M/MV5BMTc3NjI2MjU0Nl5BMl5BanBnXkFtZTgwNDk3ODYxMTE@._V1_FMjpg_UX1000_.jpg"}
    ],
    "Drama": [
        {"titulo": "O Poderoso Chefão", "ano": 1972, "imagem": "https://m.media-amazon.com/images/M/MV5BM2MyNjYxNmUtYTAwNi00MTYxLWJmNWYtYzZlODY3ZTk3OTFlXkEyXkFqcGdeQXVyNzkwMjQ5NzM@._V1_FMjpg_UX1000_.jpg"},
        {"titulo": "Forrest Gump", "ano": 1994, "imagem": "https://m.media-amazon.com/images/M/MV5BNWIwODRlZTUtY2U3ZS00Yzg1LWJhNzYtMmZiYmEyNmU1NjMzXkEyXkFqcGdeQXVyMTQxNzMzNDI@._V1_FMjpg_UX1000_.jpg"},
        {"titulo": "Cidade de Deus", "ano": 2002, "imagem": "https://m.media-amazon.com/images/M/MV5BOTMwYjc5ZmItYTFjZC00ZGQ3LTlkNTMtMjZiNTZlMWQzNzI5XkEyXkFqcGdeQXVyNzkwMjQ5NzM@._V1_FMjpg_UX1000_.jpg"},
        {"titulo": "Parasita", "ano": 2019, "imagem": "https://m.media-amazon.com/images/M/MV5BYWZjMjk3ZTItODQ2ZC00NTY5LWE0ZDYtZTI3MjcwN2Q5NTVkXkEyXkFqcGdeQXVyODk4OTc3MTY@._V1_FMjpg_UX1000_.jpg"},
        {"titulo": "Clube de Compra Dallas", "ano": 2013, "imagem": "https://m.media-amazon.com/images/M/MV5BMTcyMzc2Nzk5MF5BMl5BanBnXkFtZTcwNzQ2NDcxOQ@@._V1_FMjpg_UX1000_.jpg"}
    ],
    "Comédia": [
        {"titulo": "Se Beber, Não Case", "ano": 2009, "imagem": "https://m.media-amazon.com/images/M/MV5BMTUxMzExMzM3NF5BMl5BanBnXkFtZTcwNzg0NjYxMw@@._V1_FMjpg_UX1000_.jpg"},
        {"titulo": "As Branquelas", "ano": 2004, "imagem": "https://m.media-amazon.com/images/M/MV5BMTY2MDkxNzMzN15BMl5BanBnXkFtZTYwMTc5MDM5._V1_FMjpg_UX1000_.jpg"},
        {"titulo": "Escola de Rock", "ano": 2003, "imagem": "https://m.media-amazon.com/images/M/MV5BMTM0MDg5MzkyMV5BMl5BanBnXkFtZTcwMzk4Mzg4NA@@._V1_FMjpg_UX1000_.jpg"},
        {"titulo": "Todo Mundo Quase em Pânico", "ano": 2000, "imagem": "https://m.media-amazon.com/images/M/MV5BNDhjMzc3ZTgtY2Y4MC00Y2U3LWFiMDctZGM3MmM4N2YzNDQ5XkEyXkFqcGdeQXVyMTQxNzMzNDI@._V1_FMjpg_UX1000_.jpg"},
        {"titulo": "Superbad", "ano": 2007, "imagem": "https://m.media-amazon.com/images/M/MV5BMTc0NjIyMjA2OF5BMl5BanBnXkFtZTcwMzIxNDE1MQ@@._V1_FMjpg_UX1000_.jpg"}
    ],
    "Ficção Científica": [
        {"titulo": "Interestelar", "ano": 2014, "imagem": "https://m.media-amazon.com/images/M/MV5BZjdkOTU3MDktN2IxOS00OGEyLWFmMjktY2FiMmZkNWIyODZiXkEyXkFqcGdeQXVyMTMxODk2OTU@._V1_FMjpg_UX1000_.jpg"},
        {"titulo": "Blade Runner 2049", "ano": 2017, "imagem": "https://m.media-amazon.com/images/M/MV5BNzA1Njg4NzYxOV5BMl5BanBnXkFtZTgwODk5NjU3MzI@._V1_FMjpg_UX1000_.jpg"},
        {"titulo": "Avatar", "ano": 2009, "imagem": "https://m.media-amazon.com/images/M/MV5BZDA0OGQxNTItMDZkMC00N2UyLTg3MzMtYTJmNjg3Nzk5MzRiXkEyXkFqcGdeQXVyMjUzOTY1NTc@._V1_FMjpg_UX1000_.jpg"},
        {"titulo": "Distrito 9", "ano": 2009, "imagem": "https://m.media-amazon.com/images/M/MV5BYmQ5MzFjYWMtMTMwNC00ZGU5LWI3YTQtYzhkMGExNGFlY2Q0XkEyXkFqcGdeQXVyNTIzOTk5ODM@._V1_FMjpg_UX1000_.jpg"},
        {"titulo": "Ex Machina", "ano": 2014, "imagem": "https://m.media-amazon.com/images/M/MV5BMTUxNzc0OTIxMV5BMl5BanBnXkFtZTgwNDI3NzU2NDE@._V1_FMjpg_UX1000_.jpg"}
    ],
    "Animação": [
        {"titulo": "Toy Story", "ano": 1995, "imagem": "https://m.media-amazon.com/images/M/MV5BMDU2ZWJlMjktMTRhMy00ZTA5LWEzNDgtYmNmZTEwZTViZWJkXkEyXkFqcGdeQXVyNDQ2OTk4MzI@._V1_FMjpg_UX1000_.jpg"},
        {"titulo": "O Rei Leão", "ano": 1994, "imagem": "https://m.media-amazon.com/images/M/MV5BYTYxNGMyZTYtMjE3MS00MzNjLWFjNmYtMDk3N2FmM2JiM2M1XkEyXkFqcGdeQXVyNjY5NDU4NzI@._V1_FMjpg_UX1000_.jpg"},
        {"titulo": "Homem-Aranha: No Aranhaverso", "ano": 2018, "imagem": "https://m.media-amazon.com/images/M/MV5BMjMwNDkxMTgzOF5BMl5BanBnXkFtZTgwNTkwNTQ3NjM@._V1_FMjpg_UX1000_.jpg"},
        {"titulo": "Divertidamente", "ano": 2015, "imagem": "https://m.media-amazon.com/images/M/MV5BOTgxMDQwMDk0OF5BMl5BanBnXkFtZTgwNjU5OTg2NDE@._V1_FMjpg_UX1000_.jpg"},
        {"titulo": "A Viagem de Chihiro", "ano": 2001, "imagem": "https://m.media-amazon.com/images/M/MV5BMjlmZmI5MDctNDE2YS00YWE0LWE5ZWItZDBhYWQ0NTcxNWRhXkEyXkFqcGdeQXVyMTMxODk2OTU@._V1_FMjpg_UX1000_.jpg"}
    ]
}

class SugestaoFilmeApp(App):
    def build(self):
        # Configuração da janela
        Window.clearcolor = get_color_from_hex('#2c3e50')
        self.title = "Sugestão de Filmes por Gênero"
        Window.size = (400, 700)
        
        # Layout principal
        layout_principal = BoxLayout(orientation='vertical', padding=0, spacing=0)
        
        # Cabeçalho com barra azul
        cabecalho = BoxLayout(orientation='vertical', size_hint_y=None, height=dp(80))
        with cabecalho.canvas.before:
            Color(rgba=get_color_from_hex('#3498db'))
            Rectangle(pos=cabecalho.pos, size=cabecalho.size)
        
        titulo = Label(
            text="Sugestão de Filmes por Gênero",
            font_size=dp(24),
            bold=True,
            color=get_color_from_hex('#ecf0f1'),
            size_hint_y=None,
            height=dp(80)
        )
        cabecalho.add_widget(titulo)
        layout_principal.add_widget(cabecalho)
        
        # Container para o conteúdo principal
        container_principal = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(15))
        
        # Campo de nome
        container_nome = BoxLayout(orientation='vertical', size_hint_y=None, height=dp(80))
        lbl_nome = Label(
            text="Digite seu nome:",
            font_size=dp(16),
            color=get_color_from_hex('#bdc3c7'),
            size_hint_y=None,
            height=dp(30)
        )
        self.input_nome = TextInput(
            multiline=False,
            size_hint_y=None,
            height=dp(40),
            background_color=get_color_from_hex('#ecf0f1'),
            foreground_color=get_color_from_hex('#2c3e50'),
            hint_text="Seu nome aqui...",
            padding=dp(10),
            write_tab=False,
            halign='center'
        )
        container_nome.add_widget(lbl_nome)
        container_nome.add_widget(self.input_nome)
        container_principal.add_widget(container_nome)
        
        # Campo de gênero
        container_genero = BoxLayout(orientation='vertical', size_hint_y=None, height=dp(80))
        lbl_genero = Label(
            text="Escolha seu gênero favorito:",
            font_size=dp(16),
            color=get_color_from_hex('#bdc3c7'),
            size_hint_y=None,
            height=dp(30)
        )
        self.spinner_genero = Spinner(
            text='Selecione um gênero',
            values=list(filmes_por_genero.keys()),
            size_hint_y=None,
            height=dp(40),
            background_color=get_color_from_hex('#ecf0f1'),
            color=get_color_from_hex('#2c3e50')
        )
        container_genero.add_widget(lbl_genero)
        container_genero.add_widget(self.spinner_genero)
        container_principal.add_widget(container_genero)
        
        # Botão
        botao_sugerir = Button(
            text="Sugerir Filme",
            size_hint_y=None,
            height=dp(50),
            background_color=get_color_from_hex('#e74c3c'),
            color=get_color_from_hex('#ecf0f1'),
            bold=True
        )
        botao_sugerir.bind(on_press=self.sugerir_filme)
        container_principal.add_widget(botao_sugerir)
        
        # Separador
        separador = Label(
            text="─" * 30,
            color=get_color_from_hex('#7f8c8d'),
            size_hint_y=None,
            height=dp(20)
        )
        container_principal.add_widget(separador)
        
        # Container para a imagem do filme
        self.container_imagem = BoxLayout(
            size_hint_y=None,
            height=dp(250),
            padding=(dp(10), 0)
        )
        container_principal.add_widget(self.container_imagem)
        
        # Label para exibir a sugestão
        self.label_sugestao = Label(
            text="",
            font_size=dp(18),
            color=get_color_from_hex('#ecf0f1'),
            text_size=(Window.width - dp(40), None),
            halign='center',
            valign='middle',
            size_hint_y=None,
            height=dp(100)
        )
        self.label_sugestao.bind(texture_size=self.label_sugestao.setter('size'))
        container_principal.add_widget(self.label_sugestao)
        
        # Adiciona o container principal ao layout principal
        layout_principal.add_widget(container_principal)
        
        return layout_principal
    
    def sugerir_filme(self, instance):
        nome = self.input_nome.text.strip()
        genero = self.spinner_genero.text
        
        if not nome:
            self.label_sugestao.text = "Por favor, digite seu nome."
            self.label_sugestao.color = get_color_from_hex('#e74c3c')
            self.container_imagem.clear_widgets()
            return
            
        if genero == 'Selecione um gênero':
            self.label_sugestao.text = "Por favor, selecione um gênero de filme."
            self.label_sugestao.color = get_color_from_hex('#e74c3c')
            self.container_imagem.clear_widgets()
            return
        
        # Sorteia um filme aleatório do gênero selecionado
        filmes_genero = filmes_por_genero[genero]
        filme_sorteado = random.choice(filmes_genero)
        
        # Limpa a imagem anterior
        self.container_imagem.clear_widgets()
        
        # Adiciona a nova imagem
        imagem = AsyncImage(
            source=filme_sorteado['imagem'],
            allow_stretch=True,
            keep_ratio=True,
            size_hint=(1, 1)
        )
        self.container_imagem.add_widget(imagem)
        
        # Formata a mensagem de sugestão
        mensagem = f"Olá, [b]{nome}[/b]!\nPara o gênero [b]{genero}[/b], sua sugestão é:\n[color=#f39c12][b]{filme_sorteado['titulo']}[/b][/color] ({filme_sorteado['ano']})"
        
        self.label_sugestao.text = mensagem
        self.label_sugestao.color = get_color_from_hex('#ecf0f1')
        self.label_sugestao.markup = True

if __name__ == '__main__':
    SugestaoFilmeApp().run()