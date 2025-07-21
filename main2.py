from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import Color, Ellipse, Line
from kivy.uix.floatlayout import FloatLayout


class MeuPaintWidget(Widget):
    def __init__(self, **kwargs):
        super(MeuPaintWidget, self).__init__(**kwargs)
        self.current_color = (1, 1, 0)  # Cor padrão: amarelo

    def on_touch_down(self, touch):
        with self.canvas:
            Color(*self.current_color)
            d = 30.
            Ellipse(pos=(touch.x - d / 2, touch.y - d / 2), size=(d, d))
            touch.ud['line'] = Line(points=(touch.x, touch.y))

    def on_touch_move(self, touch):
        touch.ud['line'].points += [touch.x, touch.y]

    def set_color(self, r, g, b):
        self.current_color = (r, g, b)


class MeuPaintApp(App):
    def build(self):
        root = FloatLayout()
        self.painter = MeuPaintWidget()
        root.add_widget(self.painter)

        # Layout de botões
        btn_layout = BoxLayout(size_hint=(1, None), height=50, pos_hint={'top': 1})

        # Botão Apagar
        clearbtn = Button(text='Apagar')
        clearbtn.bind(on_release=self.clear_canvas)
        btn_layout.add_widget(clearbtn)

        # Botões de cor
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
            btn_layout.add_widget(btn)

        root.add_widget(btn_layout)
        return root

    def clear_canvas(self, instance):
        self.painter.canvas.clear()

MeuPaintApp().run()
