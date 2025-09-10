import sqlite3
import os
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner
from kivy.core.window import Window
from kivy.utils import get_color_from_hex
from kivy.metrics import dp
from kivy.uix.scrollview import ScrollView
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.gridlayout import GridLayout

# Função para inicializar o banco de dados
def init_db():
    # Obter o diretório do aplicativo
    db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "filmes.db")
    
    con = sqlite3.connect(db_path)
    cur = con.cursor()
    cur.execute("""
     CREATE TABLE IF NOT EXISTS filmes (
     id INTEGER PRIMARY KEY AUTOINCREMENT,
     titulo TEXT, 
     genero TEXT,
     ano INTEGER
     )
    """)
    con.commit()
    con.close()
    return db_path

# Inicializar o banco de dados
DB_PATH = init_db()

class CadastroScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = "cadastro"
        
        layout = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(15))
        
        # Título
        titulo = Label(
            text="Cadastro de Filmes",
            font_size=dp(20),
            bold=True,
            color=get_color_from_hex('#ecf0f1'),
            size_hint_y=None,
            height=dp(40)
        )
        layout.add_widget(titulo)
        
        # Campo título
        lbl_titulo = Label(
            text="Título do Filme:",
            font_size=dp(16),
            color=get_color_from_hex('#bdc3c7'),
            size_hint_y=None,
            height=dp(30)
        )
        self.input_titulo = TextInput(
            multiline=False,
            size_hint_y=None,
            height=dp(40),
            background_color=get_color_from_hex('#ecf0f1'),
            foreground_color=get_color_from_hex('#2c3e50'),
            hint_text="Digite o título do filme...",
            padding=dp(10)
        )
        layout.add_widget(lbl_titulo)
        layout.add_widget(self.input_titulo)
        
        # Campo gênero
        lbl_genero = Label(
            text="Gênero:",
            font_size=dp(16),
            color=get_color_from_hex('#bdc3c7'),
            size_hint_y=None,
            height=dp(30)
        )
        self.spinner_genero = Spinner(
            text='Selecione um gênero',
            values=['Ação', 'Drama', 'Comédia', 'Ficção Científica', 'Animação'],
            size_hint_y=None,
            height=dp(40),
            background_color=get_color_from_hex('#ecf0f1'),
            color=get_color_from_hex('#2c3e50')
        )
        layout.add_widget(lbl_genero)
        layout.add_widget(self.spinner_genero)
        
        # Campo ano
        lbl_ano = Label(
            text="Ano de Lançamento:",
            font_size=dp(16),
            color=get_color_from_hex('#bdc3c7'),
            size_hint_y=None,
            height=dp(30)
        )
        self.input_ano = TextInput(
            multiline=False,
            size_hint_y=None,
            height=dp(40),
            background_color=get_color_from_hex('#ecf0f1'),
            foreground_color=get_color_from_hex('#2c3e50'),
            hint_text="Digite o ano...",
            padding=dp(10),
            input_filter='int'
        )
        layout.add_widget(lbl_ano)
        layout.add_widget(self.input_ano)
        
        # Botões
        botoes_layout = BoxLayout(size_hint_y=None, height=dp(50), spacing=dp(10))
        
        btn_salvar = Button(
            text="Salvar",
            background_color=get_color_from_hex('#27ae60'),
            color=get_color_from_hex('#ecf0f1'),
            bold=True
        )
        btn_salvar.bind(on_press=self.salvar_filme)
        
        btn_listar = Button(
            text="Ver Lista",
            background_color=get_color_from_hex('#3498db'),
            color=get_color_from_hex('#ecf0f1'),
            bold=True
        )
        btn_listar.bind(on_press=self.ir_para_lista)
        
        botoes_layout.add_widget(btn_salvar)
        botoes_layout.add_widget(btn_listar)
        
        layout.add_widget(botoes_layout)
        
        self.add_widget(layout)
    
    def salvar_filme(self, instance):
        titulo = self.input_titulo.text.strip()
        genero = self.spinner_genero.text
        ano = self.input_ano.text.strip()
        
        if not titulo:
            self.mostrar_popup("Erro", "Por favor, digite o título do filme.")
            return
            
        if genero == 'Selecione um gênero':
            self.mostrar_popup("Erro", "Por favor, selecione um gênero.")
            return
            
        if not ano:
            self.mostrar_popup("Erro", "Por favor, digite o ano de lançamento.")
            return
        
        try:
            ano = int(ano)
        except ValueError:
            self.mostrar_popup("Erro", "Por favor, digite um ano válido.")
            return
        
        # Salvar no banco de dados
        try:
            con = sqlite3.connect(DB_PATH)
            cur = con.cursor()
            cur.execute("INSERT INTO filmes (titulo, genero, ano) VALUES (?, ?, ?)", 
                       (titulo, genero, ano))
            con.commit()
            con.close()
            
            # Limpar campos
            self.input_titulo.text = ""
            self.spinner_genero.text = 'Selecione um gênero'
            self.input_ano.text = ""
            
            self.mostrar_popup("Sucesso", "Filme cadastrado com sucesso!")
        except Exception as e:
            self.mostrar_popup("Erro", f"Erro ao salvar no banco de dados: {str(e)}")
    
    def ir_para_lista(self, instance):
        self.manager.current = "lista"
        self.manager.get_screen("lista").carregar_filmes()
    
    def mostrar_popup(self, titulo, mensagem):
        popup_layout = BoxLayout(orientation='vertical', padding=dp(10), spacing=dp(10))
        popup_layout.add_widget(Label(text=mensagem))
        
        btn_fechar = Button(text="Fechar", size_hint_y=None, height=dp(40))
        popup_layout.add_widget(btn_fechar)
        
        popup = Popup(title=titulo, content=popup_layout, size_hint=(0.8, 0.4))
        btn_fechar.bind(on_press=popup.dismiss)
        popup.open()

class ListaScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = "lista"
        
        self.layout = BoxLayout(orientation='vertical', padding=dp(10), spacing=dp(10))
        
        # Título
        titulo = Label(
            text="Lista de Filmes",
            font_size=dp(20),
            bold=True,
            color=get_color_from_hex('#ecf0f1'),
            size_hint_y=None,
            height=dp(40)
        )
        self.layout.add_widget(titulo)
        
        # Campo de busca
        busca_layout = BoxLayout(size_hint_y=None, height=dp(40), spacing=dp(10))
        lbl_busca = Label(
            text="Buscar:",
            size_hint_x=0.3,
            color=get_color_from_hex('#bdc3c7')
        )
        self.input_busca = TextInput(
            multiline=False,
            size_hint_x=0.5,
            hint_text="Digite o título...",
            background_color=get_color_from_hex('#ecf0f1'),
            foreground_color=get_color_from_hex('#2c3e50')
        )
        btn_buscar = Button(
            text="Buscar",
            size_hint_x=0.2,
            background_color=get_color_from_hex('#3498db'),
            color=get_color_from_hex('#ecf0f1')
        )
        btn_buscar.bind(on_press=self.buscar_filmes)
        
        busca_layout.add_widget(lbl_busca)
        busca_layout.add_widget(self.input_busca)
        busca_layout.add_widget(btn_buscar)
        self.layout.add_widget(busca_layout)
        
        # Opções de ordenação
        ordenacao_layout = BoxLayout(size_hint_y=None, height=dp(40), spacing=dp(10))
        lbl_ordenar = Label(
            text="Ordenar por:",
            size_hint_x=0.4,
            color=get_color_from_hex('#bdc3c7')
        )
        self.spinner_ordenacao = Spinner(
            text='Título',
            values=['Título', 'Ano', 'Gênero'],
            size_hint_x=0.4,
            background_color=get_color_from_hex('#ecf0f1'),
            color=get_color_from_hex('#2c3e50')
        )
        btn_ordenar = Button(
            text="Aplicar",
            size_hint_x=0.2,
            background_color=get_color_from_hex('#3498db'),
            color=get_color_from_hex('#ecf0f1')
        )
        btn_ordenar.bind(on_press=self.ordenar_filmes)
        
        ordenacao_layout.add_widget(lbl_ordenar)
        ordenacao_layout.add_widget(self.spinner_ordenacao)
        ordenacao_layout.add_widget(btn_ordenar)
        self.layout.add_widget(ordenacao_layout)
        
        # Botão voltar
        btn_voltar = Button(
            text="Voltar ao Cadastro",
            size_hint_y=None,
            height=dp(40),
            background_color=get_color_from_hex('#e74c3c'),
            color=get_color_from_hex('#ecf0f1'),
            bold=True
        )
        btn_voltar.bind(on_press=self.ir_para_cadastro)
        self.layout.add_widget(btn_voltar)
        
        # ScrollView para a lista
        self.scroll = ScrollView()
        self.lista_container = GridLayout(cols=1, spacing=dp(10), size_hint_y=None)
        self.lista_container.bind(minimum_height=self.lista_container.setter('height'))
        self.scroll.add_widget(self.lista_container)
        self.layout.add_widget(self.scroll)
        
        self.add_widget(self.layout)
    
    def carregar_filmes(self, criterio_ordenacao="titulo"):
        # Limpar lista atual
        self.lista_container.clear_widgets()
        
        # Definir ordenação
        if criterio_ordenacao == "Título":
            order_by = "titulo"
        elif criterio_ordenacao == "Ano":
            order_by = "ano"
        elif criterio_ordenacao == "Gênero":
            order_by = "genero, titulo"
        else:
            order_by = "titulo"
        
        # Buscar filmes no banco de dados
        try:
            con = sqlite3.connect(DB_PATH)
            cur = con.cursor()
            cur.execute(f"SELECT * FROM filmes ORDER BY {order_by}")
            filmes = cur.fetchall()
            con.close()
            
            if not filmes:
                sem_registros = Label(
                    text="Nenhum filme cadastrado.",
                    font_size=dp(16),
                    color=get_color_from_hex('#bdc3c7'),
                    size_hint_y=None,
                    height=dp(40)
                )
                self.lista_container.add_widget(sem_registros)
            else:
                for filme in filmes:
                    self.adicionar_item_lista(filme)
        except Exception as e:
            erro = Label(
                text=f"Erro ao carregar filmes: {str(e)}",
                font_size=dp(16),
                color=get_color_from_hex('#e74c3c'),
                size_hint_y=None,
                height=dp(40)
            )
            self.lista_container.add_widget(erro)
    
    def adicionar_item_lista(self, filme):
        item = BoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=dp(60),
            spacing=dp(10)
        )
        
        info = Label(
            text=f"{filme[1]} ({filme[3]}) - {filme[2]}",
            font_size=dp(14),
            color=get_color_from_hex('#ecf0f1'),
            size_hint_x=0.7,
            text_size=(None, None),
            halign='left',
            valign='middle'
        )
        info.bind(texture_size=info.setter('size'))
        
        botoes = BoxLayout(size_hint_x=0.3, spacing=dp(5))
        
        btn_editar = Button(
            text="Editar",
            size_hint_x=0.5,
            background_color=get_color_from_hex('#f39c12'),
            color=get_color_from_hex('#ecf0f1'),
            font_size=dp(12)
        )
        btn_editar.filme_id = filme[0]
        btn_editar.bind(on_press=self.editar_filme)
        
        btn_excluir = Button(
            text="Excluir",
            size_hint_x=0.5,
            background_color=get_color_from_hex('#e74c3c'),
            color=get_color_from_hex('#ecf0f1'),
            font_size=dp(12)
        )
        btn_excluir.filme_id = filme[0]
        btn_excluir.bind(on_press=self.excluir_filme)
        
        botoes.add_widget(btn_editar)
        botoes.add_widget(btn_excluir)
        
        item.add_widget(info)
        item.add_widget(botoes)
        
        self.lista_container.add_widget(item)
    
    def buscar_filmes(self, instance):
        termo_busca = self.input_busca.text.strip()
        
        if not termo_busca:
            self.carregar_filmes()
            return
        
        # Limpar lista atual
        self.lista_container.clear_widgets()
        
        # Buscar filmes no banco de dados
        try:
            con = sqlite3.connect(DB_PATH)
            cur = con.cursor()
            cur.execute("SELECT * FROM filmes WHERE titulo LIKE ? ORDER BY titulo", (f'%{termo_busca}%',))
            filmes = cur.fetchall()
            con.close()
            
            if not filmes:
                sem_resultados = Label(
                    text="Nenhum filme encontrado.",
                    font_size=dp(16),
                    color=get_color_from_hex('#bdc3c7'),
                    size_hint_y=None,
                    height=dp(40)
                )
                self.lista_container.add_widget(sem_resultados)
            else:
                for filme in filmes:
                    self.adicionar_item_lista(filme)
        except Exception as e:
            erro = Label(
                text=f"Erro na busca: {str(e)}",
                font_size=dp(16),
                color=get_color_from_hex('#e74c3c'),
                size_hint_y=None,
                height=dp(40)
            )
            self.lista_container.add_widget(erro)
    
    def ordenar_filmes(self, instance):
        criterio = self.spinner_ordenacao.text
        self.carregar_filmes(criterio)
    
    def editar_filme(self, instance):
        filme_id = instance.filme_id
        
        # Buscar dados do filme
        try:
            con = sqlite3.connect(DB_PATH)
            cur = con.cursor()
            cur.execute("SELECT * FROM filmes WHERE id = ?", (filme_id,))
            filme = cur.fetchone()
            con.close()
            
            # Criar popup de edição
            popup_layout = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(15))
            
            popup_layout.add_widget(Label(text="Editar Filme", font_size=dp(18), bold=True))
            
            # Campo título
            lbl_titulo = Label(text="Título:", size_hint_y=None, height=dp(30))
            input_titulo = TextInput(
                text=filme[1],
                multiline=False,
                size_hint_y=None,
                height=dp(40)
            )
            popup_layout.add_widget(lbl_titulo)
            popup_layout.add_widget(input_titulo)
            
            # Campo gênero
            lbl_genero = Label(text="Gênero:", size_hint_y=None, height=dp(30))
            spinner_genero = Spinner(
                text=filme[2],
                values=['Ação', 'Drama', 'Comédia', 'Ficção Científica', 'Animação'],
                size_hint_y=None,
                height=dp(40)
            )
            popup_layout.add_widget(lbl_genero)
            popup_layout.add_widget(spinner_genero)
            
            # Campo ano
            lbl_ano = Label(text="Ano:", size_hint_y=None, height=dp(30))
            input_ano = TextInput(
                text=str(filme[3]),
                multiline=False,
                size_hint_y=None,
                height=dp(40),
                input_filter='int'
            )
            popup_layout.add_widget(lbl_ano)
            popup_layout.add_widget(input_ano)
            
            # Botões
            botoes_layout = BoxLayout(size_hint_y=None, height=dp(40), spacing=dp(10))
            
            btn_salvar = Button(text="Salvar")
            btn_cancelar = Button(text="Cancelar")
            
            botoes_layout.add_widget(btn_salvar)
            botoes_layout.add_widget(btn_cancelar)
            popup_layout.add_widget(botoes_layout)
            
            popup = Popup(
                title="",
                content=popup_layout,
                size_hint=(0.9, 0.7)
            )
            
            def salvar_edicao(instance):
                novo_titulo = input_titulo.text.strip()
                novo_genero = spinner_genero.text
                novo_ano = input_ano.text.strip()
                
                if not novo_titulo or not novo_ano:
                    return
                
                try:
                    novo_ano = int(novo_ano)
                except ValueError:
                    return
                
                try:
                    con = sqlite3.connect(DB_PATH)
                    cur = con.cursor()
                    cur.execute("UPDATE filmes SET titulo = ?, genero = ?, ano = ? WHERE id = ?", 
                               (novo_titulo, novo_genero, novo_ano, filme_id))
                    con.commit()
                    con.close()
                    
                    popup.dismiss()
                    self.carregar_filmes()
                except Exception as e:
                    popup.dismiss()
                    self.mostrar_popup("Erro", f"Erro ao editar filme: {str(e)}")
            
            btn_salvar.bind(on_press=salvar_edicao)
            btn_cancelar.bind(on_press=popup.dismiss)
            
            popup.open()
        except Exception as e:
            self.mostrar_popup("Erro", f"Erro ao carregar filme: {str(e)}")
    
    def excluir_filme(self, instance):
        filme_id = instance.filme_id
        
        # Popup de confirmação
        popup_layout = BoxLayout(orientation='vertical', padding=dp(10), spacing=dp(10))
        popup_layout.add_widget(Label(text="Tem certeza que deseja excluir este filme?"))
        
        botoes_layout = BoxLayout(size_hint_y=None, height=dp(40), spacing=dp(10))
        
        btn_confirmar = Button(text="Sim")
        btn_cancelar = Button(text="Cancelar")
        
        botoes_layout.add_widget(btn_confirmar)
        botoes_layout.add_widget(btn_cancelar)
        popup_layout.add_widget(botoes_layout)
        
        popup = Popup(
            title="Confirmar Exclusão",
            content=popup_layout,
            size_hint=(0.8, 0.4)
        )
        
        def confirmar_exclusao(instance):
            try:
                con = sqlite3.connect(DB_PATH)
                cur = con.cursor()
                cur.execute("DELETE FROM filmes WHERE id = ?", (filme_id,))
                con.commit()
                con.close()
                
                popup.dismiss()
                self.carregar_filmes()
            except Exception as e:
                popup.dismiss()
                self.mostrar_popup("Erro", f"Erro ao excluir filme: {str(e)}")
        
        btn_confirmar.bind(on_press=confirmar_exclusao)
        btn_cancelar.bind(on_press=popup.dismiss)
        
        popup.open()
    
    def mostrar_popup(self, titulo, mensagem):
        popup_layout = BoxLayout(orientation='vertical', padding=dp(10), spacing=dp(10))
        popup_layout.add_widget(Label(text=mensagem))
        
        btn_fechar = Button(text="Fechar", size_hint_y=None, height=dp(40))
        popup_layout.add_widget(btn_fechar)
        
        popup = Popup(title=titulo, content=popup_layout, size_hint=(0.8, 0.4))
        btn_fechar.bind(on_press=popup.dismiss)
        popup.open()
    
    def ir_para_cadastro(self, instance):
        self.manager.current = "cadastro"

class GerenciadorFilmesApp(App):
    def build(self):
        Window.clearcolor = get_color_from_hex('#2c3e50')
        self.title = "Gerenciador de Filmes"
        Window.size = (400, 600)
        
        # Gerenciador de telas
        sm = ScreenManager()
        sm.add_widget(CadastroScreen())
        sm.add_widget(ListaScreen())
        
        return sm

if __name__ == '__main__':
    GerenciadorFilmesApp().run()