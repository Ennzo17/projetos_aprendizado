from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty, ObjectProperty
from kivy.event import EventDispatcher
from kivy.lang import Builder

# Carrega o KV
Builder.load_file("event_comm.kv")


# Estado global compartilhado
class GlobalState(EventDispatcher):
    current_status = StringProperty("Inicial")

# Widget que exibe o status
class StatusDisplayWidget(BoxLayout):
    global_state_obj = ObjectProperty(None)


# Widget que altera o status
class StatusChangerWidget(BoxLayout):
    global_state_obj = ObjectProperty(None)

    def update_status(self, new_text):
        if self.global_state_obj:
            self.global_state_obj.current_status = new_text


# Widget principal que organiza os dois
class RootWidget(BoxLayout):
    pass


class EventCommApp(App):
    def build(self):
        # Instancia o estado compartilhado
        shared_state = GlobalState()

        # Cria o layout principal e injeta o estado em ambos os widgets
        root = RootWidget()
        root.ids.status_display.global_state_obj = shared_state
        root.ids.status_changer.global_state_obj = shared_state
        return root


if __name__ == '__main__':
    EventCommApp().run()
