# main.py

import kivy
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.properties import NumericProperty, ReferenceListProperty, ObjectProperty
from kivy.vector import Vector
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.core.window import Window

# Requisita versão mínima do Kivy
kivy.require('1.11.1')

# Carrega o layout do arquivo pong.kv
Builder.load_file("pong.kv")


class PongBall(Widget):
    """Classe da bola do jogo. Controla sua velocidade e movimentação."""

    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)
    velocity = ReferenceListProperty(velocity_x, velocity_y)

    def move(self):
        """Atualiza a posição da bola com base em sua velocidade."""
        self.pos = Vector(*self.velocity) + self.pos

    def bounce_paddle(self, paddle):
        """Faz a bola rebater ao colidir com uma raquete."""
        if self.collide_widget(paddle):
            self.velocity_x *= -1
            offset = (self.center_y - paddle.center_y) / (paddle.height / 2)
            self.velocity_y += offset


class PongPaddle(Widget):
    """Classe das raquetes dos jogadores."""
    
    score = NumericProperty(0)

    def move_up(self):
        """Move a raquete para cima, respeitando o limite superior."""
        if self.top < self.parent.height:
            self.y += 20

    def move_down(self):
        """Move a raquete para baixo, respeitando o limite inferior."""
        if self.y > 0:
            self.y -= 20


class PongGame(Widget):
    """Classe principal do jogo, que coordena os elementos."""

    ball = ObjectProperty(None)
    player1 = ObjectProperty(None)
    player2 = ObjectProperty(None)

    def serve_ball(self, vel=(4, 0)):
        """Posiciona e lança a bola do centro com velocidade inicial."""
        self.ball.center = self.center
        self.ball.velocity = Vector(*vel).rotate(10)

    def update(self, dt):
        """Atualiza o estado do jogo a cada frame (60 FPS)."""
        self.ball.move()

        # Rebater nas bordas superior/inferior
        if self.ball.y < 0 or self.ball.top > self.height:
            self.ball.velocity_y *= -1

        # Rebater nas raquetes
        self.ball.bounce_paddle(self.player1)
        self.ball.bounce_paddle(self.player2)

        # Pontuação e reset da bola
        if self.ball.x < self.x:  # Player 1 errou
            self.player2.score += 1
            self.serve_ball(vel=(4, 0))

        if self.ball.right > self.width:  # Player 2 errou
            self.player1.score += 1
            self.serve_ball(vel=(-4, 0))

    def on_touch_move(self, touch):
        """Permite controlar as raquetes por toque na tela."""
        if touch.x < self.width / 3:
            self.player1.center_y = touch.y
        elif touch.x > self.width * 2 / 3:
            self.player2.center_y = touch.y


class PongApp(App):
    """App principal que inicializa o jogo."""

    def build(self):
        game = PongGame()
        game.serve_ball()
        Clock.schedule_interval(game.update, 1.0 / 60.0)  # 60 FPS
        Window.bind(on_key_down=self.on_key_down)  # Ativa teclado
        self.game = game
        return game

    def on_key_down(self, *args):
        """Controla as raquetes pelo teclado."""
        key = args[1]
        if key == 119:  # W
            self.game.player1.move_up()
        elif key == 115:  # S
            self.game.player1.move_down()
        elif key == 273:  # Seta ↑
            self.game.player2.move_up()
        elif key == 274:  # Seta ↓
            self.game.player2.move_down()


if __name__ == '__main__':
    PongApp().run()
