"""
APLICATIVO DE SUGESTÃO DE FILMES POR GÊNERO

Este aplicativo Kivy permite que usuários recebam sugestões aleatórias de filmes
baseadas em seu gênero favorito. Ele inclui funcionalidades para:
- Inserir nome do usuário
- Selecionar um gênero de filme
- Receber sugestões aleatórias com poster do filme
- Manter um histórico de sugestões

Autor: Desconhecido
Data: Desconhecida
Versão: 1.0
"""

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

# =============================================================================
# BASE DE DADOS DE FILMES
# =============================================================================

"""
Dicionário que armazena filmes organizados por gênero.
Cada gênero contém uma lista de dicionários com informações dos filmes:
- titulo: Nome do filme
- ano: Ano de lançamento
- imagem: URL do poster do filme
"""
filmes_por_genero = {
    "Ação": [
        {"titulo": "Matrix", "ano": 1999, "imagem": "https://m.media-amazon.com/images/M/MV5BNzQzOTk3OTAtNDQ0Zi00ZTVkLWI0MTEtMDllZjNkYzNjNTc4L2ltYWdlXkEyXkFqcGdeQXVyNjU0OTQ0OTY@._V1_FMjpg_UX1000_.jpg"},
        # ... outros filmes de ação
    ],
    "Drama": [
        {"titulo": "O Poderoso Chefão", "ano": 1972, "imagem": "https://m.media-amazon.com/images/M/MV5BM2MyNjYxNmUtYTAwNi00MTYxLWJmNWYtYzZlODY3ZTk3OTFlXkEyXkFqcGdeQXVyNzkwMjQ5NzM@._V1_FMjpg_UX1000_.jpg"},
        # ... outros filmes de drama
    ],
    "Comédia": [
        {"titulo": "Se Beber, Não Case", "ano": 2009, "imagem": "https://i.pinimg.com/736x/1f/35/59/1f35591f4bdc22cefc633f98021ac027.jpg"},
        # ... outros filmes de comédia
    ],
    "Ficção Científica": [
        {"titulo": "Interestelar", "ano": 2014, "imagem": "https://m.media-amazon.com/images/M/MV5BZjdkOTU3MDktN2IxOS00OGEyLWFmMjktY2FiMmZkNWIyODZiXkEyXkFqcGdeQXVyMTMxODk2OTU@._V1_FMjpg_UX1000_.jpg"},
        # ... outros filmes de ficção científica
    ],
    "Animação": [
        {"titulo": "Toy Story", "ano": 1995, "imagem": "https://m.media-amazon.com/images/M/MV5BMDU2ZWJlMjktMTRhMy00ZTA5LWEzNDgtYmNmZTEwZTViZWJkXkEyXkFqcGdeQXVyNDQ2OTk4MzI@._V1_FMjpg_UX1000_.jpg"},
        # ... outros filmes de animação
    ]
}

# =============================================================================
# CLASSE PRINCIPAL DO APLICATIVO
# =============================================================================

class SugestaoFilmeApp(App):
    """
    Classe principal do aplicativo que herda de App do Kivy.
    Responsável por construir a interface e gerenciar a lógica do programa.
    """
    
    def build(self):
        """
        Método obrigatório do Kivy que constrói a interface do aplicativo.
        
        Returns:
            BoxLayout: Layout principal contendo todos os elementos da UI
        """
        # Configuração da janela
        Window.clearcolor = get_color_from_hex('#2c3e50')  # Cor de fundo
        self.title = "Sugestão de Filmes por Gênero"
        Window.size = (400, 800)
        
        # Lista para armazenar o histórico de sugestões
        self.historico_sugestoes = []
        
        # Layout principal (vertical)
        layout_principal = BoxLayout(orientation='vertical', padding=0, spacing=0)
        
        # =====================================================================
        # CABEÇALHO
        # =====================================================================
        cabecalho = BoxLayout(orientation='vertical', size_hint_y=None, height=dp(60))
        titulo = Label(
            text="Sugestão de Filmes por Gênero",
            font_size=dp(20),
            bold=True,
            color=get_color_from_hex('#ecf0f1'),
            size_hint_y=None,
            height=dp(60)
        )
        cabecalho.add_widget(titulo)
        layout_principal.add_widget(cabecalho)
        
        # Container para o conteúdo principal
        container_principal = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(15))
        
        # =====================================================================
        # CAMPO DE NOME
        # =====================================================================
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
        
        # =====================================================================
        # CAMPO DE GÊNERO (SPINNER)
        # =====================================================================
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
        
        # =====================================================================
        # BOTÃO DE SUGERIR FILME
        # =====================================================================
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
        
        # Separador visual
        separador = Label(
            text="─" * 30,
            color=get_color_from_hex('#7f8c8d'),
            size_hint_y=None,
            height=dp(20)
        )
        container_principal.add_widget(separador)
        
        # =====================================================================
        # ÁREA DE EXIBIÇÃO DA IMAGEM DO FILME
        # =====================================================================
        self.container_imagem = BoxLayout(
            size_hint_y=None,
            height=dp(200),
            padding=(dp(10), 0)
        )
        container_principal.add_widget(self.container_imagem)
        
        # =====================================================================
        # LABEL PARA EXIBIR A SUGESTÃO
        # =====================================================================
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
        
        # =====================================================================
        # BOTÃO PARA MOSTRAR HISTÓRICO
        # =====================================================================
        botao_historico = Button(
            text="Ver Histórico",
            size_hint_y=None,
            height=dp(40),
            background_color=get_color_from_hex('#3498db'),
            color=get_color_from_hex('#ecf0f1'),
            bold=True
        )
        botao_historico.bind(on_press=self.mostrar_historico)
        container_principal.add_widget(botao_historico)
        
        # Adiciona o container principal ao layout principal
        layout_principal.add_widget(container_principal)
        
        return layout_principal

    # =========================================================================
    # MÉTODOS DA CLASSE
    # =========================================================================

    def sugerir_filme(self, instance):
        """
        Método chamado quando o botão 'Sugerir Filme' é pressionado.
        Gera uma sugestão de filme baseada no gênero selecionado.
        
        Args:
            instance: Referência ao botão que acionou o evento
        """
        nome = self.input_nome.text.strip()
        genero = self.spinner_genero.text
        
        # Validação de entrada
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
        
        # Seleciona um filme aleatório do gênero escolhido
        filmes_genero = filmes_por_genero[genero]
        filme_sorteado = random.choice(filmes_genero)
        
        # Limpa a imagem anterior e exibe a nova
        self.container_imagem.clear_widgets()
        imagem = AsyncImage(
            source=filme_sorteado['imagem'],
            allow_stretch=True,
            keep_ratio=True,
            size_hint=(1, 1)
        )
        self.container_imagem.add_widget(imagem)
        
        # Formata e exibe a mensagem de sugestão
        mensagem = f"Olá, [b]{nome}[/b]!\nPara o gênero [b]{genero}[/b], sua sugestão é:\n[color=#f39c12][b]{filme_sorteado['titulo']}[/b][/color] ({filme_sorteado['ano']})"
        
        self.label_sugestao.text = mensagem
        self.label_sugestao.color = get_color_from_hex('#ecf0f1')
        self.label_sugestao.markup = True
        
        # Adiciona a sugestão ao histórico
        self.historico_sugestoes.append({
            'nome': nome,
            'genero': genero,
            'filme': filme_sorteado['titulo'],
            'ano': filme_sorteado['ano']
        })
    
    def mostrar_historico(self, instance):
        """
        Exibe um popup com o histórico de sugestões de filmes.
        
        Args:
            instance: Referência ao botão que acionou o evento
        """
        # Cria layout para o popup de histórico
        historico_popup = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(10))
        
        # Título do histórico
        titulo_historico = Label(
            text="Histórico de Sugestões",
            font_size=dp(18),
            bold=True,
            color=get_color_from_hex('#ecf0f1'),
            size_hint_y=None,
            height=dp(40)
        )
        historico_popup.add_widget(titulo_historico)
        
        # ScrollView para permitir rolagem do histórico
        scroll = ScrollView()
        historico_container = BoxLayout(orientation='vertical', size_hint_y=None, spacing=dp(10))
        historico_container.bind(minimum_height=historico_container.setter('height'))
        
        # Verifica se há histórico para exibir
        if not self.historico_sugestoes:
            sem_historico = Label(
                text="Nenhuma sugestão ainda.",
                font_size=dp(16),
                color=get_color_from_hex('#bdc3c7'),
                size_hint_y=None,
                height=dp(40)
            )
            historico_container.add_widget(sem_historico)
        else:
            # Adiciona cada item do histórico (do mais recente para o mais antigo)
            for sugestao in reversed(self.historico_sugestoes):
                item_historico = Label(
                    text=f"{sugestao['nome']} - {sugestao['genero']}:\n{sugestao['filme']} ({sugestao['ano']})",
                    font_size=dp(14),
                    color=get_color_from_hex('#ecf0f1'),
                    text_size=(Window.width - dp(60), None),
                    halign='left',
                    size_hint_y=None,
                    height=dp(60)
                )
                item_historico.bind(texture_size=item_historico.setter('size'))
                historico_container.add_widget(item_historico)
        
        scroll.add_widget(historico_container)
        historico_popup.add_widget(scroll)
        
        # Botão para fechar o popup
        botao_fechar = Button(
            text="Fechar",
            size_hint_y=None,
            height=dp(40),
            background_color=get_color_from_hex('#e74c3c'),
            color=get_color_from_hex('#ecf0f1')
        )
        
        # Cria e exibe a popup
        popup = Popup(
            title='',
            content=historico_popup,
            size_hint=(0.9, 0.7),
            auto_dismiss=False
        )
        
        botao_fechar.bind(on_press=popup.dismiss)
        historico_popup.add_widget(botao_fechar)
        
        popup.open()

# =============================================================================
# PONTO DE ENTRADA DO APLICATIVO
# =============================================================================

if __name__ == '__main__':
    """
    Ponto de entrada principal do aplicativo.
    Instancia e executa a aplicação Kivy.
    """
    SugestaoFilmeApp().run()