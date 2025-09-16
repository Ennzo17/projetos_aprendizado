from datetime import datetime

class sistemaUsuario:
    def __init__(self):
        self.usuarios = {}
        self.log = []  # agora temos um log de ações para saber quando usuários foram adicionados

    def adicionar_usuario(self, nome, email):
        if not "@" in email:  # uma forma simples de validação de email
            raise ValueError("Email inválido.")
        
        if email in self.usuarios:  # evitar duplicatas
            raise ValueError("EI!! Usuário já cadastrado.")

        self.usuarios[email] = nome
        self.log.append(f"Usuário {nome} ({email}) adicionado em {self.obter_data()}") # registra acao no log

    def listar_usuarios(self):
        return list(self.usuarios.items())

    def obter_log(self):
        return self.log
    
    def obter_data(self):
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S") # data e hora - Year-month-day Hour:Minute:Second
    
    def exportar_usuarios(self, arquivo):
        # exporta a lista de usuários para um arquivo de texto
        with open(arquivo, 'w', encoding='utf-8') as f:  
            # 'w' para escrita, 'utf-8' para suportar caracteres especiais
            # with garante que o arquivo será fechado corretamente e open abre o arquivo
            # "as f" é uma convenção para referenciar o arquivo aberto tipo "file"

            f.write("Usuários do sistema:\n") # cabeçalho do arquivo o \n é quebra de linha
            f.write("====================\n") # linha de separação
            for email, nome in self.usuarios.items():
                f.write(f"{nome} - {email}\n")
        self.log.append(f"Usuários exportados para {arquivo} em {self.obter_data()}")

    def visualizar_log(self):
        return "\n".join(self.log)  # retorna o log como uma string formatada

    def limpar_log(self):
        self.log = []  # limpa o log de ações

    def limpar_usuarios(self): 
        self.usuarios.clear()  # limpa a lista de usuários
        self.log.append(f"Lista de usuários limpa em {self.obter_data()}")

if __name__ == "__main__":
    print("Cadastro de usuários (após a refatoração)")
    sistema = sistemaUsuario()

    try: #'tenta adicionar usuarios
        sistema.adicionar_usuario("Aninha coder", "aninhacoder@example.com")
        sistema.adicionar_usuario("Maninhos dev", "maninhosdev@example.com")

        sistema.adicionar_usuario("Aninha coder", "aninhacoder@example.com")  # tenta adicionar duplicata
    except ValueError as e:
        print(f"Erro: {e}")

    try: # tenta adicionar email inválido outro try para o segundo exception para não dar erro
        sistema.adicionar_usuario("Usuario", "usuario.com")  # tenta adicionar email inválido
    except ValueError as e:
        print(f"Erro: {e}")

    print("\nLista de usuários:") # \n pulando linha
    usuarios = sistema.listar_usuarios() # retorna a lista de usuarios caada usuario é uma tupla (email, nome) 
    for email, nome in usuarios:
        print(f"Nome: {nome}, Email: {email}") # f string para formatar a string

    # ver o log de ações
    print("\nLog:")
    print(sistema.visualizar_log())

    # exportar usuários para um determinado arquivo
    sistema.exportar_usuarios("usuarios.txt") # nome do arquivo
    print("\nUsuários exportados para 'usuarios.txt'.")

    # ver o log atualizado
    print("\nLog atualizado:")
    print(sistema.visualizar_log())

    