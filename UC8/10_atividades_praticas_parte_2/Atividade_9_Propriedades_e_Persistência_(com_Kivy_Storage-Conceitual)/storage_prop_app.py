from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import NumericProperty
from kivy.storage.jsonstore import JsonStore
from kivy.lang import Builder

# Carrega o arquivo KV
Builder.load_file("storage_prop.kv")

# Arquivo para armazenar os dados
store = JsonStore('counter.json')


class PersistentCounter(BoxLayout):
    count = NumericProperty(0)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Recupera o valor salvo (se existir)
        if store.exists('contador'):
            self.count = store.get('contador')['value']

    def increment(self):
        self.count += 1


class StoragePropApp(App):
    def build(self):
        return PersistentCounter()

    def on_stop(self):
        # Salva o valor atual quando o app é fechado
        store.put('contador', value=self.root.count)


if __name__ == '__main__':
    StoragePropApp().run()
