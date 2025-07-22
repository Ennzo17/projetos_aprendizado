import kivy
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.graphics import Color, Ellipse, Line
import random # Importa o módulo random

class PaintWidget(Widget):
    def on_touch_down(self, touch):
        with self.canvas:
            # Modificação: Gera cores RGB aleatórias
            r = random.random()
            g = random.random()
            b = random.random()
            color = Color(r, g, b)

            d = 30
            ellipse = Ellipse(pos=(touch.x - d / 2, touch.y - d / 2), size=(d, d))
            touch.ud['line'] = Line(points=(touch.x, touch.y))

    def on_touch_move(self, touch):
        if 'line' in touch.ud: # Adicionando verificação para garantir que 'line' existe
            touch.ud['line'].points += [touch.x, touch.y]