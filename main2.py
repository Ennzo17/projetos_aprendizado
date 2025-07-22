from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.slider import Slider
from kivy.graphics import Color, Ellipse, Line, Rectangle
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label


class MeuPaintWidget(Widget):
    def __init__(self, **kwargs):
        super(MeuPaintWidget, self).__init__(**kwargs)
        self.current_color = (1, 1, 0)  # Cor padrão: amarelo
        self.brush_size = 5            # Tamanho do traço
        self.brush_shape = "linha"     # Formas: linha, círculo, retângulo
        self.start_pos = None          # Usado para início do retângulo

    def on_touch_down(self, touch):
        with self.canvas:
            Color(*self.current_color)
            if self.brush_shape == "círculo":
                d = self.brush_size
                Ellipse(pos=(touch.x - d / 2, touch.y - d / 2), size=(d, d))
            elif self.brush_shape == "linha":
                touch.ud['line'] = Line(points=(touch.x, touch.y), width=float(self.brush_size))
            elif self.brush_shape == "retângulo":
                self.start_pos = (touch.x, touch.y)  # salva o ponto inicial

    def on_touch_move(self, touch):
        if self.brush_shape == "linha" and 'line' in touch.ud:
            touch.ud['line'].points += [touch.x, touch.y]
        elif self.brush_shape == "círculo":
            with self.canvas:
                d = self.brush_size
                Ellipse(pos=(touch.x - d / 2, touch.y - d / 2), size=(d, d))

    def on_touch_up(self, touch):
        if self.brush_shape == "retângulo" and self.start_pos:
            x1, y1 = self.start_pos
            x2, y2 = touch.x, touch.y
            width = abs(x2 - x1)
            height = abs(y2 - y1)
            pos = (min(x1, x2), min(y1, y2))
            with self.canvas:
                Color(*self.current_color)
                Rectangle(pos=pos, size=(width, height))
            self.start_pos = None  # limpa a posição inicial

    def set_color(self, r, g, b):
        self.current_color = (r, g, b)

    def set_brush_size(self, value):
        self.brush_size = float(value)

    def set_brush_shape(self, shape):
        self.brush_shape = shape


class MeuPaintApp(App):
    def build(self):
        root = FloatLayout()
        self.painter = MeuPaintWidget()
        root.add_widget(self.painter)

        # Layout superior (cores + apagar)
        top_layout = BoxLayout(size_hint=(1, None), height=50, pos_hint={'top': 1})

        clearbtn = Button(text='Apagar')
        clearbtn.bind(on_release=self.clear_canvas)
        top_layout.add_widget(clearbtn)

        colors = {
            'Vermelho': (1, 0, 0),
            'Verde': (0, 1, 0),
            'Azul': (0, 0, 1),
            'Branco': (1, 1, 1),
            'Amarelo': (1, 1, 0),
        }

        for nome, rgb in colors.items():
            btn = Button(text=nome, background_color=(*rgb, 1))
            btn.bind(on_release=lambda btn, cor=rgb: self.painter.set_color(*cor))
            top_layout.add_widget(btn)

        root.add_widget(top_layout)

        # Layout inferior (formas + tamanho)
        bottom_layout = BoxLayout(size_hint=(1, None), height=50, pos_hint={'y': 0})

        slider_label = Label(text='Tamanho:', size_hint=(None, 1), width=80)
        size_slider = Slider(min=1, max=50, value=5)
        size_slider.bind(value=lambda instance, value: self.painter.set_brush_size(value))
        bottom_layout.add_widget(slider_label)
        bottom_layout.add_widget(size_slider)

        # Botões de forma
        btn_linha = Button(text='Linha')
        btn_circulo = Button(text='Círculo')
        btn_retangulo = Button(text='Retângulo')

        btn_linha.bind(on_release=lambda x: self.painter.set_brush_shape("linha"))
        btn_circulo.bind(on_release=lambda x: self.painter.set_brush_shape("círculo"))
        btn_retangulo.bind(on_release=lambda x: self.painter.set_brush_shape("retângulo"))

        bottom_layout.add_widget(btn_linha)
        bottom_layout.add_widget(btn_circulo)
        bottom_layout.add_widget(btn_retangulo)

        root.add_widget(bottom_layout)

        return root

    def clear_canvas(self, instance):
        self.painter.canvas.clear()


MeuPaintApp().run()
