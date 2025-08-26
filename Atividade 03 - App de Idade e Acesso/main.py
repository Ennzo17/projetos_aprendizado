from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.core.window import Window
from kivy.uix.popup import Popup
from kivy.properties import StringProperty, ListProperty, NumericProperty
from kivy.metrics import sp, dp


# Centralização de estilos e mensagens
class Style:
    # Cores
    PRIMARY_COLOR = [0.2, 0.6, 0.8, 1]
    SECONDARY_COLOR = [0.3, 0.3, 0.3, 1]
    BACKGROUND_COLOR = [0.98, 0.98, 0.98, 1]
    ERROR_COLOR = [0.8, 0.2, 0.2, 1]
    SUCCESS_COLOR = [0.2, 0.6, 0.2, 1]
    WARNING_COLOR = [0.8, 0.5, 0.2, 1]
    INPUT_BG_COLOR = [0.95, 0.95, 0.95, 1]
    TEXT_COLOR = [0.2, 0.2, 0.2, 1]
    
    # Tamanhos de fonte
    TITLE_FONT_SIZE = sp(24)
    LABEL_FONT_SIZE = sp(18)
    INPUT_FONT_SIZE = sp(18)
    BUTTON_FONT_SIZE = sp(18)
    RESULT_FONT_SIZE = sp(20)
    
    # Espaçamentos
    PADDING = dp(50)
    SPACING = dp(20)
    INPUT_HEIGHT = dp(50)
    BUTTON_HEIGHT = dp(60)
    TITLE_HEIGHT = dp(50)
    LABEL_HEIGHT = dp(30)
    RESULT_HEIGHT = dp(80)
    
    # Mensagens
    ERROR_EMPTY_NAME = "Por favor, digite seu nome."
    ERROR_EMPTY_AGE = "Por favor, digite sua idade."
    ERROR_INVALID_AGE = "Por favor, digite uma idade válida (apenas números)."
    ERROR_NEGATIVE_AGE = "Idade não pode ser negativa."
    ERROR_MAX_AGE = "Idade inválida. Por favor, verifique."
    ELDERLY_MESSAGE = "Olá, {nome}! Você é idoso e merece muito respeito!!."
    ADULT_MESSAGE = "Olá, {nome}! Você é maior de idade."
    MINOR_MESSAGE = "Olá, {nome}! Você é menor de idade."


class AgeValidator:
    """Classe separada para validação de idade, permitindo reuso"""
    
    @staticmethod
    def validate_age(age_text):
        """Valida a idade e retorna (idade, erro)"""
        if not age_text:
            return None, Style.ERROR_EMPTY_AGE
        
        try:
            idade = int(age_text)
            
            if idade < 0:
                return None, Style.ERROR_NEGATIVE_AGE
                
            if idade > 120:
                return None, Style.ERROR_MAX_AGE
                
            return idade, None
            
        except ValueError:
            return None, Style.ERROR_INVALID_AGE
    
    @staticmethod
    def get_age_message(nome, idade):
        """Retorna a mensagem apropriada baseada na idade"""
        if idade >= 60:
            return Style.ELDERLY_MESSAGE.format(nome=nome), Style.ERROR_COLOR
        elif idade >= 18:
            return Style.ADULT_MESSAGE.format(nome=nome), Style.SUCCESS_COLOR
        else:
            return Style.MINOR_MESSAGE.format(nome=nome), Style.WARNING_COLOR


class ErrorPopup(Popup):
    """Popup de erro reutilizável"""
    def __init__(self, message, **kwargs):
        super().__init__(
            title='Erro',
            content=Label(text=message, font_size=sp(16)),
            size_hint=(0.8, 0.4),
            background_color=Style.ERROR_COLOR,
            **kwargs
        )


class CustomLabel(Label):
    """Label personalizada com estilos padrão"""
    def __init__(self, **kwargs):
        kwargs.setdefault('font_size', Style.LABEL_FONT_SIZE)
        kwargs.setdefault('color', Style.SECONDARY_COLOR)
        kwargs.setdefault('size_hint_y', None)
        kwargs.setdefault('height', Style.LABEL_HEIGHT)
        super().__init__(**kwargs)


class CustomTextInput(TextInput):
    """TextInput personalizado com estilos padrão"""
    def __init__(self, **kwargs):
        kwargs.setdefault('multiline', False)
        kwargs.setdefault('font_size', Style.INPUT_FONT_SIZE)
        kwargs.setdefault('size_hint_y', None)
        kwargs.setdefault('height', Style.INPUT_HEIGHT)
        kwargs.setdefault('background_color', Style.INPUT_BG_COLOR)
        kwargs.setdefault('foreground_color', Style.TEXT_COLOR)
        super().__init__(**kwargs)


class CustomButton(Button):
    """Button personalizado com estilos padrão"""
    def __init__(self, **kwargs):
        kwargs.setdefault('font_size', Style.BUTTON_FONT_SIZE)
        kwargs.setdefault('size_hint_y', None)
        kwargs.setdefault('height', Style.BUTTON_HEIGHT)
        kwargs.setdefault('background_color', Style.PRIMARY_COLOR)
        kwargs.setdefault('color', [1, 1, 1, 1])
        kwargs.setdefault('bold', True)
        super().__init__(**kwargs)


class MeuApp(BoxLayout):
    # Propriedades para vincular com a interface
    resultado_texto = StringProperty('')
    resultado_cor = ListProperty(Style.TEXT_COLOR)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = Style.PADDING
        self.spacing = Style.SPACING
        
        # Título
        titulo = Label(
            text='Verificador de Idade',
            font_size=Style.TITLE_FONT_SIZE,
            bold=True,
            color=Style.PRIMARY_COLOR,
            size_hint_y=None,
            height=Style.TITLE_HEIGHT
        )
        self.add_widget(titulo)
        
        # Campo para nome
        self.nome_label = CustomLabel(text='Nome:')
        self.add_widget(self.nome_label)
        
        self.nome_input = CustomTextInput()
        self.add_widget(self.nome_input)
        
        # Campo para idade
        self.idade_label = CustomLabel(text='Idade:')
        self.add_widget(self.idade_label)
        
        self.idade_input = CustomTextInput(input_filter='int')
        self.add_widget(self.idade_input)
        
        # Botão enviar
        self.botao_enviar = CustomButton(text='Enviar')
        self.botao_enviar.bind(on_press=self.verificar_idade)
        self.add_widget(self.botao_enviar)
        
        # Label para resultado
        self.resultado_label = Label(
            text=self.resultado_texto,
            font_size=Style.RESULT_FONT_SIZE,
            color=self.resultado_cor,
            size_hint_y=None,
            height=Style.RESULT_HEIGHT,
            text_size=(Window.width - Style.PADDING * 2, None),
            halign='center',
            valign='middle'
        )
        self.bind(resultado_texto=self.resultado_label.setter('text'))
        self.bind(resultado_cor=self.resultado_label.setter('color'))
        self.add_widget(self.resultado_label)
    
    def verificar_idade(self, instance):
        nome = self.nome_input.text.strip()
        
        # Validação do nome
        if not nome:
            ErrorPopup(Style.ERROR_EMPTY_NAME).open()
            return
        
        # Validação da idade
        idade, erro = AgeValidator.validate_age(self.idade_input.text.strip())
        if erro:
            ErrorPopup(erro).open()
            return
        
        # Obter mensagem baseada na idade
        mensagem, cor = AgeValidator.get_age_message(nome, idade)
        
        # Exibir resultado
        self.resultado_texto = mensagem
        self.resultado_cor = cor


class IdadeApp(App):
    def build(self):
        Window.clearcolor = Style.BACKGROUND_COLOR
        return MeuApp()

if __name__ == '__main__':
    IdadeApp().run()