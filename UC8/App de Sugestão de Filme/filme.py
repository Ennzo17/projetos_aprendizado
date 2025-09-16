import random
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner
from kivy.uix.image import AsyncImage
from kivy.core.window import Window
from kivy.utils import get_color_from_hex
from kivy.metrics import dp
from kivy.uix.scrollview import ScrollView
from kivy.uix.popup import Popup
from kivy.uix.gridlayout import GridLayout
from kivy.clock import Clock
from kivy.graphics import Color, RoundedRectangle
from kivy.properties import ListProperty, StringProperty
from kivy.uix.modalview import ModalView

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
        {"titulo": "Clube de Compra Dallas", "ano": 2013, "imagem": "https://i.pinimg.com/736x/aa/3f/2f/aa3f2ffa0691365486f51b6d0754e312.jpg"}
    ],
    "Comédia": [
        {"titulo": "Se Beber, Não Case", "ano": 2009, "imagem": "https://i.pinimg.com/736x/1f/35/59/1f35591f4bdc22cefc633f98021ac027.jpg"},
        {"titulo": "As Branquelas", "ano": 2004, "imagem": "https://i.pinimg.com/736x/e4/71/2a/e4712ae58795ab898ba239df75db673a.jpg"},
        {"titulo": "Escola de Rock", "ano": 2003, "imagem": "https://i.pinimg.com/1200x/34/0f/b7/340fb73e781ba4676abf64269312af76.jpg"},
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

class RoundedButton(Button):
    bg_color = ListProperty([1, 1, 1, 1])
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.background_normal = ''
        self.background_color = [0, 0, 0, 0]
        with self.canvas.before:
            Color(rgba=self.bg_color)
            self.rect = RoundedRectangle(size=self.size, pos=self.pos, radius=[15])
        
        self.bind(pos=self.update_rect, size=self.update_rect)
    
    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

class FilmeSuggestion(BoxLayout):
    titulo = StringProperty("")
    ano = StringProperty("")
    imagem = StringProperty("")
    
    def __init__(self, titulo, ano, imagem, **kwargs):
        super().__init__(**kwargs)
        self.titulo = titulo
        self.ano = ano
        self.imagem = imagem
        self.orientation = 'horizontal'
        self.size_hint_y = None
        self.height = dp(80)
        self.padding = [dp(10), dp(5)]
        self.spacing = dp(10)
        
        # Imagem do filme
        img = AsyncImage(
            source=imagem,
            size_hint=(None, 1),
            width=dp(60),
            allow_stretch=True,
            keep_ratio=True
        )
        
        # Informações do filme
        info_layout = BoxLayout(orientation='vertical')
        info_layout.add_widget(Label(
            text=titulo, 
            size_hint_y=0.6,
            font_size=dp(16),
            bold=True,
            color=get_color_from_hex('#2c3e50'),
            halign='left'
        ))
        info_layout.add_widget(Label(
            text=f"({ano})", 
            size_hint_y=0.4,
            font_size=dp(14),
            color=get_color_from_hex('#7f8c8d'),
            halign='left'
        ))
        
        self.add_widget(img)
        self.add_widget(info_layout)

class SugestaoFilmeApp(App):
    def build(self):
        # Configuração da janela
        Window.clearcolor = get_color_from_hex('#2c3e50')
        self.title = "Sugestão de Filmes por Gênero"
        Window.size = (400, 700)
        
        # Lista para armazenar o histórico
        self.historico_sugestoes = []
        
        # Layout principal
        layout_principal = BoxLayout(orientation='vertical', padding=0, spacing=0)
        
        # Cabeçalho
        cabecalho = BoxLayout(
            orientation='vertical', 
            size_hint_y=None, 
            height=dp(80),
            padding=[0, dp(10)]
        )
        with cabecalho.canvas.before:
            Color(rgba=get_color_from_hex('#3498db'))
            self.header_rect = RoundedRectangle(size=cabecalho.size, pos=cabecalho.pos, radius=[0, 0, 15, 15])
        cabecalho.bind(size=self.update_header_rect, pos=self.update_header_rect)
        
        titulo = Label(
            text="Sugestão de Filmes",
            font_size=dp(22),
            bold=True,
            color=get_color_from_hex('#ecf0f1'),
        )
        subtitulo = Label(
            text="Descubra seu próximo filme favorito",
            font_size=dp(14),
            color=get_color_from_hex('#ecf0f1'),
        )
        cabecalho.add_widget(titulo)
        cabecalho.add_widget(subtitulo)
        layout_principal.add_widget(cabecalho)
        
        # Container para o conteúdo principal com rolagem
        scroll = ScrollView()
        container_principal = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(15), size_hint_y=None)
        container_principal.bind(minimum_height=container_principal.setter('height'))
        scroll.add_widget(container_principal)
        
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
        botao_sugerir = RoundedButton(
            text="Sugerir Filme",
            size_hint_y=None,
            height=dp(50),
            bg_color=get_color_from_hex('#e74c3c'),
            color=get_color_from_hex('#ecf0f1'),
            bold=True
        )
        botao_sugerir.bind(on_press=self.sugerir_filme)
        container_principal.add_widget(botao_sugerir)
        
        # Separador
        separador = Label(
            text="•" * 20,
            color=get_color_from_hex('#7f8c8d'),
            size_hint_y=None,
            height=dp(20)
        )
        container_principal.add_widget(separador)
        
        # Container para a imagem do filme
        self.container_imagem = BoxLayout(
            size_hint_y=None,
            height=dp(220),
            padding=(dp(10), 0)
        )
        container_principal.add_widget(self.container_imagem)
        
        # Label para exibir a sugestão
        self.label_sugestao = Label(
            text="",
            font_size=dp(16),
            color=get_color_from_hex('#ecf0f1'),
            text_size=(Window.width - dp(40), None),
            halign='center',
            valign='middle',
            size_hint_y=None,
            height=dp(80)
        )
        self.label_sugestao.bind(texture_size=self.label_sugestao.setter('size'))
        container_principal.add_widget(self.label_sugestao)
        
        # Botão para mostrar histórico
        botao_historico = RoundedButton(
            text="Ver Histórico",
            size_hint_y=None,
            height=dp(40),
            bg_color=get_color_from_hex('#3498db'),
            color=get_color_from_hex('#ecf0f1'),
            bold=True
        )
        botao_historico.bind(on_press=self.mostrar_historico)
        container_principal.add_widget(botao_historico)
        
        # Ajusta a altura do container principal
        container_principal.height = (
            container_nome.height + container_genero.height + 
            botao_sugerir.height + separador.height + 
            self.container_imagem.height + self.label_sugestao.height + 
            botao_historico.height + (dp(15) * 6)  # spacing * número de gaps
        )
        
        layout_principal.add_widget(scroll)
        
        return layout_principal
    
    def update_header_rect(self, instance, value):
        self.header_rect.pos = instance.pos
        self.header_rect.size = instance.size
    
    def sugerir_filme(self, instance):
        nome = self.input_nome.text.strip()
        genero = self.spinner_genero.text
        
        if not nome:
            self.mostrar_erro("Por favor, digite seu nome.")
            return
            
        if genero == 'Selecione um gênero':
            self.mostrar_erro("Por favor, selecione um gênero de filme.")
            return
        
        # Mostra indicador de carregamento
        self.label_sugestao.text = "Procurando sugestões..."
        self.label_sugestao.color = get_color_from_hex('#ecf0f1')
        self.container_imagem.clear_widgets()
        
        # Simula um pequeno delay para carregamento (opcional)
        Clock.schedule_once(lambda dt: self._selecionar_filme(nome, genero), 0.5)
    
    def _selecionar_filme(self, nome, genero):
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
        
        # Adiciona ao histórico
        self.historico_sugestoes.append({
            'nome': nome,
            'genero': genero,
            'filme': filme_sorteado['titulo'],
            'ano': filme_sorteado['ano'],
            'imagem': filme_sorteado['imagem']
        })
    
    def mostrar_erro(self, mensagem):
        self.label_sugestao.text = mensagem
        self.label_sugestao.color = get_color_from_hex('#e74c3c')
        self.container_imagem.clear_widgets()
    
    def mostrar_historico(self, instance):
        if not self.historico_sugestoes:
            self.mostrar_popup_simples("Histórico Vazio", "Nenhuma sugestão foi feita ainda.")
            return
            
        # Cria uma popup personalizada para o histórico
        popup = ModalView(size_hint=(0.9, 0.8), background_color=[0, 0, 0, 0])
        
        # Layout principal da popup
        main_layout = BoxLayout(orientation='vertical', padding=dp(10), spacing=dp(10))
        
        # Título
        titulo = Label(
            text="Histórico de Sugestões",
            font_size=dp(20),
            bold=True,
            color=get_color_from_hex('#ecf0f1'),
            size_hint_y=None,
            height=dp(40)
        )
        main_layout.add_widget(titulo)
        
        # ScrollView para o histórico
        scroll = ScrollView()
        historico_container = BoxLayout(orientation='vertical', size_hint_y=None, spacing=dp(10))
        historico_container.bind(minimum_height=historico_container.setter('height'))
        
        # Adiciona cada item do histórico
        for sugestao in reversed(self.historico_sugestoes):
            item = FilmeSuggestion(
                titulo=sugestao['filme'],
                ano=str(sugestao['ano']),
                imagem=sugestao['imagem']
            )
            historico_container.add_widget(item)
        
        scroll.add_widget(historico_container)
        main_layout.add_widget(scroll)
        
        # Botão para fechar
        btn_fechar = RoundedButton(
            text="Fechar",
            size_hint_y=None,
            height=dp(40),
            bg_color=get_color_from_hex('#e74c3c'),
            color=get_color_from_hex('#ecf0f1')
        )
        btn_fechar.bind(on_press=popup.dismiss)
        main_layout.add_widget(btn_fechar)
        
        # Ajusta a altura do container
        historico_container.height = len(self.historico_sugestoes) * dp(90)
        
        popup.add_widget(main_layout)
        popup.open()
    
    def mostrar_popup_simples(self, titulo, mensagem):
        popup = ModalView(size_hint=(0.7, 0.4))
        
        content = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(20))
        content.add_widget(Label(text=titulo, font_size=dp(18), bold=True))
        content.add_widget(Label(text=mensagem, font_size=dp(16)))
        
        btn = RoundedButton(text="OK", size_hint_y=None, height=dp(40))
        btn.bind(on_press=popup.dismiss)
        content.add_widget(btn)
        
        popup.add_widget(content)
        popup.open()

if __name__ == '__main__':
    SugestaoFilmeApp().run()