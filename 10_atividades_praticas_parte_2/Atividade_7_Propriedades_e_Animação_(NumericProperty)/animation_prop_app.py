from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import NumericProperty
from kivy.animation import Animation
from kivy.lang import Builder

# Carrega o .kv
Builder.load_file("animation_prop.kv")


class AnimatedBox(BoxLayout):
    # Propriedade numérica que será animada
    box_size = NumericProperty(100)

    def animate_box(self):
        # Alterna entre 100 e 200
        new_size = 200 if self.box_size == 100 else 100
        anim = Animation(box_size=new_size, duration=0.5)
        anim.start(self)


class AnimationPropApp(App):
    def build(self):
        return AnimatedBox()


if __name__ == '__main__':
    AnimationPropApp().run()
