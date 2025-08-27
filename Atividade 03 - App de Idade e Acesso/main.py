from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.core.window import Window
from kivy.uix.popup import Popup
from kivy.properties import StringProperty, ListProperty
from kivy.metrics import sp, dp
from kivy.uix.image import Image
from kivy.graphics import Rectangle


# ==============================================================
# CLASSE STYLE - Centraliza todas as configurações de aparência
# ==============================================================
class Style:
    # Cores RGBA [R, G, B, Alpha] para consistência visual
    PRIMARY_COLOR = [0.2, 0.6, 0.8, 1]      # Azul principal para botões
    SECONDARY_COLOR = [0.3, 0.3, 0.3, 1]    # Cinza para textos secundários
    BACKGROUND_COLOR = [0.98, 0.98, 0.98, 1] # Cor de fundo clara
    ERROR_COLOR = [0.8, 0.2, 0.2, 1]        # Vermelho para erros
    SUCCESS_COLOR = [0.2, 0.6, 0.2, 1]      # Verde para sucesso
    WARNING_COLOR = [0.8, 0.5, 0.2, 1]      # Laranja para avisos
    INPUT_BG_COLOR = [0.95, 0.95, 0.95, 1]  # Cor de fundo dos campos
    TEXT_COLOR = [0.2, 0.2, 0.2, 1]         # Cor do texto principal

    # Tamanhos de fonte escaláveis (sp = scale-independent pixels)
    TITLE_FONT_SIZE = sp(24)    # Título grande e destacado
    LABEL_FONT_SIZE = sp(18)    # Texto dos rótulos (Nome:, Idade:)
    INPUT_FONT_SIZE = sp(18)    # Texto dentro dos campos de entrada
    BUTTON_FONT_SIZE = sp(18)   # Texto do botão
    RESULT_FONT_SIZE = sp(20)   # Texto do resultado (maior para destaque)

    # Espaçamentos e tamanhos em pixels densidade-independentes (dp)
    PADDING = dp(50)           # Espaço interno ao redor do layout
    SPACING = dp(20)           # Espaço entre os widgets
    INPUT_HEIGHT = dp(50)      # Altura dos campos de texto
    BUTTON_HEIGHT = dp(60)     # Altura do botão (maior para fácil clique)
    TITLE_HEIGHT = dp(50)      # Altura do título
    LABEL_HEIGHT = dp(30)      # Altura dos rótulos
    RESULT_HEIGHT = dp(80)     # Altura da área de resultado

    # Mensagens de erro e feedback para o usuário
    ERROR_EMPTY_NAME = "Por favor, digite seu nome."
    ERROR_EMPTY_AGE = "Por favor, digite sua idade."
    ERROR_INVALID_AGE = "Por favor, digite uma idade válida (apenas números)."
    ERROR_NEGATIVE_AGE = "Idade não pode ser negativa."
    ERROR_MAX_AGE = "Idade inválida. Por favor, verifique."
    
    # Mensagens personalizadas baseadas na faixa etária
    ELDERLY_MESSAGE = "Olá, {nome}! Você é idoso e merece muito respeito!!"
    ADULT_MESSAGE = "Olá, {nome}! Você é maior de idade."
    MINOR_MESSAGE = "Olá, {nome}! Você é menor de idade."


# ==============================================================
# CLASSE AGEVALIDATOR - Lógica de validação e classificação
# ==============================================================
class AgeValidator:
    @staticmethod
    def validate_age(age_text):
        """Valida a idade digitada e retorna (idade, erro) ou (idade, None)"""
        if not age_text:
            return None, Style.ERROR_EMPTY_AGE  # Campo vazio
        try:
            idade = int(age_text)
            if idade < 0:
                return None, Style.ERROR_NEGATIVE_AGE  # Idade negativa
            if idade > 120:
                return None, Style.ERROR_MAX_AGE  # Idade acima do limite
            return idade, None  # Idade válida
        except ValueError:
            return None, Style.ERROR_INVALID_AGE  # Não é número

    @staticmethod
    def get_age_message(nome, idade):
        """Retorna mensagem e cor baseada na faixa etária"""
        if idade >= 60:
            return Style.ELDERLY_MESSAGE.format(nome=nome), Style.SUCCESS_COLOR
        elif idade >= 18:
            return Style.ADULT_MESSAGE.format(nome=nome), Style.SUCCESS_COLOR
        else:
            return Style.MINOR_MESSAGE.format(nome=nome), Style.WARNING_COLOR


# ==============================================================
# CLASSE ERRORPOPUP - Popup de erro personalizado
# ==============================================================
class ErrorPopup(Popup):
    def __init__(self, message, **kwargs):
        super().__init__(
            title='Erro',  # Título da janela popup
            content=Label(text=message, font_size=sp(16)),  # Conteúdo da mensagem
            size_hint=(0.8, 0.4),  # Tamanho relativo à janela (80% largura, 40% altura)
            **kwargs
        )


# ==============================================================
# COMPONENTES VISUAIS PERSONALIZADOS
# ==============================================================

# RÓTULO PERSONALIZADO - Exibe textos informativos
class CustomLabel(Label):
    def __init__(self, **kwargs):
        kwargs.setdefault('font_size', Style.LABEL_FONT_SIZE)  # Tamanho padrão
        kwargs.setdefault('color', Style.SECONDARY_COLOR)      # Cor padrão
        kwargs.setdefault('size_hint_y', None)                 # Altura fixa
        kwargs.setdefault('height', Style.LABEL_HEIGHT)        # Altura definida
        super().__init__(**kwargs)

# CAMPO DE TEXTO PERSONALIZADO - Para entrada de dados do usuário
class CustomTextInput(TextInput):
    def __init__(self, **kwargs):
        kwargs.setdefault('multiline', False)                  # Apenas uma linha
        kwargs.setdefault('font_size', Style.INPUT_FONT_SIZE)  # Tamanho da fonte
        kwargs.setdefault('size_hint_y', None)                 # Altura fixa
        kwargs.setdefault('height', Style.INPUT_HEIGHT)        # Altura definida
        kwargs.setdefault('background_color', Style.INPUT_BG_COLOR)  # Cor de fundo
        kwargs.setdefault('foreground_color', Style.TEXT_COLOR)      # Cor do texto
        super().__init__(**kwargs)

# BOTÃO PERSONALIZADO - Para ações do usuário
class CustomButton(Button):
    def __init__(self, **kwargs):
        kwargs.setdefault('font_size', Style.BUTTON_FONT_SIZE)  # Tamanho do texto
        kwargs.setdefault('size_hint_y', None)                  # Altura fixa
        kwargs.setdefault('height', Style.BUTTON_HEIGHT)        # Altura definida
        kwargs.setdefault('background_color', Style.PRIMARY_COLOR)  # Cor azul
        kwargs.setdefault('color', [1, 1, 1, 1])               # Texto branco
        super().__init__(**kwargs)


# ==============================================================
# CLASSE PRINCIPAL DO LAYOUT - MEUAPP
# ==============================================================
class MeuApp(BoxLayout):
    resultado_texto = StringProperty('')        # Propriedade observável para texto do resultado
    resultado_cor = ListProperty(Style.TEXT_COLOR)  # Propriedade observável para cor do resultado
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'           # Layout vertical (um abaixo do outro)
        self.padding = Style.PADDING            # Espaçamento interno
        self.spacing = Style.SPACING            # Espaço entre widgets

        # PLANO DE FUNDO COM IMAGEM - Decoração visual
        with self.canvas.before:
            self.bg_rect = Rectangle(source="background.jpg", pos=self.pos, size=self.size)
        self.bind(pos=self._update_bg, size=self._update_bg)

        # TÍTULO DA APLICAÇÃO - Texto destacado com markup
        titulo = Label(
            text='[b]Verificador de Idade[/b]',  # Texto em negrito
            markup=True,                         # Habilita formatação
            font_size=Style.TITLE_FONT_SIZE,     # Tamanho grande
            color=Style.PRIMARY_COLOR,           # Cor azul
            size_hint_y=None,                    # Altura fixa
            height=Style.TITLE_HEIGHT            # Altura definida
        )
        self.add_widget(titulo)  # Adiciona à interface

        # CAMPO NOME - Rótulo + Campo de entrada
        self.nome_label = CustomLabel(text='Nome:')  # Rótulo "Nome:"
        self.add_widget(self.nome_label)
        self.nome_input = CustomTextInput()          # Campo para digitar nome
        self.add_widget(self.nome_input)

        # CAMPO IDADE - Rótulo + Campo de entrada
        self.idade_label = CustomLabel(text='Idade:')  # Rótulo "Idade:"
        self.add_widget(self.idade_label)
        self.idade_input = CustomTextInput(input_filter='int')  # Campo apenas números
        self.add_widget(self.idade_input)

        # BOTÃO ENVIAR - Aciona a verificação
        self.botao_enviar = CustomButton(text='Enviar')
        self.botao_enviar.bind(on_press=self.verificar_idade)  # Vincula função ao clique
        self.add_widget(self.botao_enviar)

        # ÁREA DE RESULTADO - Exibe a mensagem final
        self.resultado_label = Label(
            text=self.resultado_texto,                # Texto inicial vazio
            font_size=Style.RESULT_FONT_SIZE,         # Tamanho maior
            color=self.resultado_cor,                 # Cor dinâmica
            size_hint_y=None,                         # Altura fixa
            height=Style.RESULT_HEIGHT,               # Altura definida
            text_size=(Window.width - Style.PADDING * 2, Style.RESULT_HEIGHT),  # Quebra de texto
            halign='center',                          # Alinhamento horizontal central
            valign='middle'                           # Alinhamento vertical central
        )
        # Vincula propriedades observáveis para atualização automática
        self.bind(resultado_texto=self.resultado_label.setter('text'))
        self.bind(resultado_cor=self.resultado_label.setter('color'))
        self.add_widget(self.resultado_label)

    def _update_bg(self, *args):
        """Atualiza o plano de fundo quando a janela é redimensionada"""
        self.bg_rect.pos = self.pos    # Posição atualizada
        self.bg_rect.size = self.size  # Tamanho atualizado

    def verificar_idade(self, instance):
        """Função principal que valida e classifica a idade"""
        nome = self.nome_input.text.strip()  # Remove espaços em branco
        if not nome:
            ErrorPopup(Style.ERROR_EMPTY_NAME).open()  # Popup se nome vazio
            return

        idade, erro = AgeValidator.validate_age(self.idade_input.text.strip())
        if erro:
            ErrorPopup(erro).open()  # Popup se erro na idade
            return

        # Obtém mensagem e cor apropriadas
        mensagem, cor = AgeValidator.get_age_message(nome, idade)
        self.resultado_texto = mensagem  # Atualiza texto do resultado
        self.resultado_cor = cor         # Atualiza cor do resultado


# ==============================================================
# CLASSE PRINCIPAL DA APLICAÇÃO - IDADEAPP
# ==============================================================
class IdadeApp(App):
    def build(self):
        """Método obrigatório que constrói a aplicação"""
        Window.clearcolor = Style.BACKGROUND_COLOR  # Define cor de fundo da janela
        return MeuApp()  # Retorna o layout principal


# ==============================================================
# PONTO DE ENTRADA DA APLICAÇÃO
# ==============================================================
if __name__ == '__main__':
    IdadeApp().run()  # Inicia o loop principal da aplicação