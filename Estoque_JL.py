import json

class EstoqueRoupas:
    def __init__(self, arquivo_dados="estoqueJL_novo.json"):
        self.arquivo_dados = arquivo_dados
        self.estoque = {}
        self.vendas = []
        self.lucro_total = 0.0
        self.carregar_dados()

    def salvar_dados(self):
        dados = {
            'estoque': self.estoque,
            'vendas': self.vendas,
            'lucro_total': self.lucro_total
        }
        with open(self.arquivo_dados, 'w') as f:
            json.dump(dados, f, indent=4)
            print("Dados salvos com sucesso!\n")

    def carregar_dados(self):
        try:
            with open(self.arquivo_dados, 'r') as f:
                dados = json.load(f)
                self.estoque = dados.get('estoque', {})
                self.vendas = dados.get('vendas', [])
                self.lucro_total = dados.get('lucro_total', 0.0)
            print("Dados carregados com sucesso!\n")
        except FileNotFoundError:
            print("Nenhum arquivo de dados encontrado. Iniciando com estoque vazio.\n")

    def adicionar_produto(self, nome_produto, quantidade, preco_custo):
        if nome_produto in self.estoque:
            self.estoque[nome_produto]['quantidade'] += quantidade
        else:
            self.estoque[nome_produto] = {
                'quantidade': quantidade,
                'preco_custo': preco_custo
            }
        print(f"Produto '{nome_produto}' adicionado com sucesso!\n")
        print()
        self.salvar_dados()


    def remover_produto(self, nome_produto):
        if nome_produto in self.estoque:
            del self.estoque[nome_produto]
            print(f"Produto '{nome_produto}' removido do estoque.\n")
        else:
            print(f"Produto '{nome_produto}' não encontrado no estoque.\n")
        self.salvar_dados()

    def registrar_venda(self, nome_produto, quantidade, preco_venda):
        if nome_produto in self.estoque and self.estoque[nome_produto]['quantidade'] >= quantidade:
            self.estoque[nome_produto]['quantidade'] -= quantidade
            preco_custo = self.estoque[nome_produto]['preco_custo']
            lucro = (preco_venda - preco_custo) * quantidade
            self.lucro_total += lucro
            self.vendas.append({
                'nome_produto': nome_produto,
                'quantidade': quantidade,
                'preco_venda': preco_venda,
                'lucro': lucro
            })
            print(f"Venda registrada: {quantidade} unidades do produto '{nome_produto}' por R${preco_venda:.2f} cada.\n")
        else:
            print(f"Venda não realizada: estoque insuficiente para o produto '{nome_produto}'.\n")
        self.salvar_dados()

    def limpar_historico_vendas(self):
        self.vendas = []
        self.lucro_total = 0.0
        print ("Histórico de vendas e lucro total removidos com sucesso.")
        self.salvar_dados()

    def exibir_estoque(self):
        if not self.estoque:
            print("Estoque vazio.\n")
        else:
            print("Estoque atual:")
            for produto, detalhes in self.estoque.items():
                print(f"Produto: {produto} | Quantidade: {detalhes['quantidade']} | Preço de Custo: R${detalhes['preco_custo']:.2f}")
            print("---------------------------")

    def exibir_vendas(self):
        if not self.vendas:
            print("Nenhuma venda registrada.\n")
        else:
            print("Vendas registradas:")
            for venda in self.vendas:
                print(f"Produto: {venda['nome_produto']} | Quantidade: {venda['quantidade']} | Preço de Venda: R${venda['preco_venda']:.2f} | Lucro: R${venda['lucro']:.2f}")
            print()

    def exibir_lucro_total(self):
        print(f"Lucro total: R${self.lucro_total:.2f}\n")

def menu():
    estoque = EstoqueRoupas()
    print("Olá, seja bem-vindo(a) ao controle de estoque e vendas de J/L Moda e Acessórios! Como posso ajudá-lo(a)?\n")

    while True:
        print("----- Menu de controle do estoque -----")
        print("1. Adicionar produto")
        print("2. Remover produto")
        print("3. Registrar venda")
        print("4. Exibir estoque")
        print("5. Exibir vendas")
        print("6. Exibir lucro total")
        print("7. Limpar histórico mensal de vendas")
        print("0. Sair")

        opcao = input("Escolha uma opção: ")

        if opcao == '1':
            nome_produto = input("Nome do produto: ")
            quantidade = int(input("Quantidade: "))
            preco_custo = float(input("Preço de custo: "))
            estoque.adicionar_produto(nome_produto, quantidade, preco_custo)

        elif opcao == '2':
            nome_produto = input("Nome do produto: ")
            estoque.remover_produto(nome_produto)

        elif opcao == '3':
            nome_produto = input("Nome do produto: ")
            quantidade = int(input("Quantidade vendida: "))
            preco_venda = float(input("Preço de venda por unidade: "))
            estoque.registrar_venda(nome_produto, quantidade, preco_venda)

        elif opcao == '4':
            estoque.exibir_estoque()

        elif opcao == '5':
            estoque.exibir_vendas()

        elif opcao == '6':
            estoque.exibir_lucro_total()

        elif opcao == '7':
            estoque.limpar_historico_vendas()

        elif opcao == '0':
            print("Saindo do programa... Até logo!\n")
            break

        else:
            print("Opção inválida, tente novamente.\n")

if __name__ == "__main__":
    menu()
