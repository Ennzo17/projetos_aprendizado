# Sistema de Gerenciamento de Contatos - Versão 1.0

class Contato:
    def __init__(self, nome, telefone, email):
        self.nome = nome
        self.telefone = telefone
        self.email = email

class GerenciadorContatos:
    def __init__(self):
        self.contatos = []
    
    def adicionar_contato(self, contato):
        self.contatos.append(contato)
        print(f"Contato '{contato.nome}' adicionado com sucesso.")
    
    def listar_contatos(self):
        print("\n--- Lista de Contatos ---")
        if not self.contatos:
            print("Nenhum contato cadastrado.")
        else:
            for contato in self.contatos:
                print(f"Nome: {contato.nome}, Telefone: {contato.telefone}, Email: {contato.email}")
        print("-------------------------\n")