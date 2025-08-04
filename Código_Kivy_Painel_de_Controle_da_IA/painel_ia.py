# Importa as bibliotecas principais do Kivy
from kivy.app import App  # Classe base para criar o aplicativo
from kivy.uix.boxlayout import BoxLayout  # Layout em formato de caixa (vertical/horizontal)
from kivy.properties import StringProperty, NumericProperty, BooleanProperty  # Propriedades reativas
from kivy.clock import Clock  # Usado para agendar funções repetidas
from random import randint  # Gera números aleatórios para simular ameaça

# Classe principal do painel
class PainelIA(BoxLayout):
    # Propriedades que serão ligadas ao layout (.kv)
    status_text = StringProperty("IA Desativada")  # Texto de status
    nivel_ameaca = NumericProperty(0)  # Valor da barra de progresso (0 a 100)
    ia_ligada = BooleanProperty(False)  # Estado ON/OFF da IA

    # Alterna o estado da IA (ligar/desligar)
    def alternar_ia(self):
        self.ia_ligada = not self.ia_ligada  # Inverte o estado atual

        if self.ia_ligada:
            # Se a IA foi ligada
            self.status_text = "IA Ativada - Monitorando..."
            # Agendar atualização da ameaça a cada 1 segundo
            Clock.schedule_interval(self.atualizar_ameaca, 1)
        else:
            # Se a IA foi desligada
            self.status_text = "IA Desativada"
            self.nivel_ameaca = 0  # Reseta a barra de progresso
            # Para a função que atualiza a ameaça
            Clock.unschedule(self.atualizar_ameaca)

    # Função que altera o nível de ameaça aleatoriamente
    def atualizar_ameaca(self, dt):
        # Gera um valor aleatório entre 0 e 100
        self.nivel_ameaca = randint(0, 100)

        # Atualiza o status dependendo do nível de ameaça
        if self.nivel_ameaca < 50:
            self.status_text = "⚠ Alerta! Ameaça Alta!"
        elif self.nivel_ameaca > 50:
            self.status_text = "Atenção: Nível Médio"
        else:
            self.status_text = "IA Ativada - Monitorando..."

    # Função que recebe o comando digitado pelo usuário
    def enviar_comando(self):
        comando = self.ids.input_comando.text.strip()  # Lê o texto digitado
        if comando:
            self.status_text = f"Comando recebido: {comando}"  # Mostra no campo de status
            self.ids.input_comando.text = ""  # Limpa o campo de entrada
        else:
            self.status_text = "Nenhum comando inserido."  # Mensagem de erro
    
# Classe principal do aplicativo
class PainelIAApp(App):
    def build(self):
        self.title = "Painel de Controle da IA"  # Define título da janela
        return PainelIA()  # Retorna o layout principal

# Executa o aplicativo
if __name__ == "__main__":
    PainelIAApp().run()
