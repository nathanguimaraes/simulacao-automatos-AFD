# Certifique-se de ter o módulo necessário para a interface de usuário
#!pip install ipywidgets

#execute no google colab
import ipywidgets as widgets
from IPython.display import display, Markdown

# Classe da Máquina de Bombom
class MaquinaDeBombom:
    def __init__(self):
        # Estado inicial: sem moedas inseridas
        self.moedas_inseridas = 0
        # Dicionário representando os preços dos bombons (os estados de aceitação)
        self.precos_bombons = {10: "Bombom A", 15: "Bombom B", 20: "Bombom C"}
        # Conjunto de moedas aceitas (alfabeto de entrada)
        self.moedas_aceitas = [5, 10, 25]

    # Função que representa a transição de estado ao inserir uma moeda
    def inserir_moeda(self, moeda):
        if moeda in self.moedas_aceitas:
            # Verifica se a inserção da moeda faria o total ultrapassar 25 centavos
            if self.moedas_inseridas + moeda > 25:
                return f"Moeda não aceita. Total inserido: {self.moedas_inseridas} centavos. Só é possível inserir {25 - self.moedas_inseridas} centavos."
            
            # Transição de estado: acumula o valor da moeda inserida
            self.moedas_inseridas += moeda
            
            # Verifica se o total atingiu 25 centavos
            if self.moedas_inseridas >= 25:
                botao_inserir.layout.display = 'none'
                return f"Você inseriu {moeda} centavos. Total inserido: {self.moedas_inseridas} centavos. Valor máximo atingido."
            
            return f"Você inseriu {moeda} centavos. Total inserido: {self.moedas_inseridas} centavos."
        else:
            # Se a moeda não for aceita, a máquina permanece no mesmo estado
            return "Moeda não aceita"

    # Função que representa a verificação e transição para o estado de aceitação (entrega do bombom)
    def selecionar_bombom(self, preco_bombom):
        if preco_bombom in self.precos_bombons:
            # Verifica se o estado atual (total inserido) é suficiente para o estado de aceitação (preço do bombom)
            if self.moedas_inseridas >= preco_bombom:
                troco = self.moedas_inseridas - preco_bombom
                bombom = self.precos_bombons[preco_bombom]
                # Estado de aceitação: entrega o bombom e retorna ao estado inicial
                self.moedas_inseridas = 0
                botao_inserir.layout.display = 'inline-block'
                moeda_selecionada.options = [5, 10, 25]
                return f"Entregando {bombom}. Troco: {troco} centavos." if troco > 0 else f"Entregando {bombom}. Sem troco."
            else:
                # Se o valor inserido for insuficiente, permanece no estado atual aguardando mais entradas
                return "Valor insuficiente. Insira mais moedas."
        else:
            # Se o preço do bombom for inválido, a máquina permanece no estado atual
            return "Preço inválido."

# Instância da Máquina de Bombom (AFD)
maquina = MaquinaDeBombom()

# Funções para os botões (simulando entradas no AFD)
def inserir_moeda_func(moeda):
    resultado = maquina.inserir_moeda(int(moeda))
    output.append_stdout(resultado)
    
    # Atualiza as opções de moedas disponíveis
    if maquina.moedas_inseridas + 25 > 25:
        moeda_selecionada.options = [m for m in maquina.moedas_aceitas if m <= 25 - maquina.moedas_inseridas]
    if maquina.moedas_inseridas == 25:
        botao_inserir.layout.display = 'none'

def selecionar_bombom_func(preco_bombom):
    # Verifica se a transição para o estado de aceitação é possível (compra do bombom)
    output.append_stdout(maquina.selecionar_bombom(int(preco_bombom)))

# Variável para controlar a exibição da documentação
documentacao_visivel = False

# Função para mostrar/ocultar a documentação na interface
def toggle_documentacao(_):
    global documentacao_visivel
    if documentacao_visivel:
        output.clear_output()  # Oculta a documentação
    else:
        documentacao = """
        **Documentação da Máquina de Bombom como Autômato Finito Determinístico (AFD):**

        Este código implementa uma máquina de venda de bombons que pode ser vista como um Autômato Finito Determinístico (AFD).

        **Componentes do AFD:**

        - **Estados:**
          - `self.moedas_inseridas`: Representa o estado atual da máquina, ou seja, o valor total das moedas inseridas.
          - `self.moedas_inseridas = 0`: Representa o estado inicial, onde a máquina não possui moedas inseridas.
          - Estados de aceitação são representados por situações em que `self.moedas_inseridas` é suficiente para comprar um bombom.

        - **Alfabeto de Entrada:**
          - Moedas de 5, 10 e 25 centavos (`self.moedas_aceitas`) e a escolha de um bombom (valores de 10, 15 e 20 centavos).
          - As entradas que não pertencem ao alfabeto (moedas não aceitas ou preços inválidos) resultam na permanência no estado atual.

        - **Função de Transição:**
          - A função `inserir_moeda` simula a transição de estado ao inserir uma moeda.
          - A função `selecionar_bombom` verifica se a máquina pode realizar a transição para o estado de aceitação (entrega do bombom).

        - **Estado de Aceitação:**
          - Quando o valor inserido (`self.moedas_inseridas`) é suficiente para o preço do bombom escolhido, a máquina entrega o bombom, retorna ao estado inicial (`self.moedas_inseridas = 0`), e calcula o troco (se houver).

        - **Saída:**
          - O autômato gera uma saída (entrega de bombom ou mensagem) dependendo das transições e do estado atual.

        **Como usar a interface:**
        1. Escolha uma moeda no menu suspenso e clique em "Inserir Moeda".
        2. Selecione o preço do bombom desejado e clique em "Comprar Bombom".
        3. As interações e resultados serão mostrados na interface abaixo dos botões.
        """
        output.append_display_data(Markdown(documentacao))  # Exibe a documentação
    documentacao_visivel = not documentacao_visivel  # Alterna o estado da exibição

# Widgets para inserir moedas (simulação de entradas)
moeda_selecionada = widgets.Dropdown(
    options=[5, 10, 25],
    value=5,
    description='Moeda:',
)

botao_inserir = widgets.Button(
    description="Inserir Moeda",
    button_style='info',
)

# Vinculando a função ao botão (entrada no AFD)
botao_inserir.on_click(lambda x: inserir_moeda_func(moeda_selecionada.value))

# Widget para selecionar bombom (simulação de entrada)
bombom_selecionado = widgets.Dropdown(
    options=[10, 15, 20],
    value=10,
    description='Preço Bombom:',
)

botao_comprar = widgets.Button(
    description="Comprar Bombom",
    button_style='success',
)

# Vinculando a função ao botão (entrada no AFD)
botao_comprar.on_click(lambda x: selecionar_bombom_func(bombom_selecionado.value))

# Botão para mostrar/ocultar a documentação
botao_documentacao = widgets.Button(
    description="Documentação",
    button_style='warning',
)

# Vinculando a função ao botão de documentação
botao_documentacao.on_click(toggle_documentacao)

# Output widget para mostrar os resultados (saída do AFD)
output = widgets.Output()

# Exibir a interface (interface de interação do AFD)
display(moeda_selecionada, botao_inserir, bombom_selecionado, botao_comprar, botao_documentacao, output)