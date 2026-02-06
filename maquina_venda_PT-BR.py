import customtkinter as ctk
from tkinter import messagebox as mb
import random

# Lista de nomes e preços dos produtos disponíveis na máquina de venda
produto_nome = ['Coca-cola', 'Fanta', 'Sprite', 'Água tônica', 'Itubaina', 'Suco de maracujá']
produto_preco = [14.09, 9.49, 6.87, 7.99, 6.99, 7.79]

# Dicionário para armazenar informações dos produtos: nome, preço, quantidade no carrinho e estoque
produtos = {}
for i in range(len(produto_nome)):
    produtos[f'Produto_{i+1}'] = {
        'nome': produto_nome[i],
        'preco': produto_preco[i],
        'quantidade': 0,  # Quantidade do produto no carrinho
        'estoque': random.randint(5, 10)  # Estoque inicial aleatório entre 5 e 10 unidades
    }

def so_numero(char):
    """
    Valida se o caractere inserido é um número ou vírgula (para valores decimais).
    Args:
        char (str): Caractere a ser validado.
    Returns:
        bool: True se o caractere for válido, False caso contrário.
    """
    if char == '':
        return True
    if char.count(',') > 1:  # Permite apenas uma vírgula (para valores decimais)
        return False
    if all(c in '0123456789,' for c in char):  # Verifica se todos os caracteres são números ou vírgulas
        return True
    return False

def saida_troco(valor_nota, qntd):
    """
    Formata a mensagem de saída para notas e moedas do troco.
    Args:
        valor_nota (str): Tipo da nota ou moeda (ex: "100 reais").
        qntd (int): Quantidade de notas ou moedas.
    Returns:
        str: Mensagem formatada para o troco.
    """
    saida = ''
    if not 'centavo' in valor_nota and qntd == 1:
        saida += f'-> {qntd} nota de {valor_nota}\n'
    elif 'centavo' in valor_nota and qntd == 1:
        saida += f'-> {qntd} moeda de {valor_nota}\n'
    elif 'centavo' in valor_nota and qntd > 1:
        saida += f'-> {qntd} moedas de {valor_nota}\n'
    elif qntd == 0:
        return ''
    else:
        saida += f'-> {qntd} notas de {valor_nota}\n'
    return saida

def contagem_nota(troco_total, valor_da_nota):
    """
    Calcula quantas notas ou moedas de um determinado valor cabem no troco total.
    Args:
        troco_total (float): Valor total do troco a ser dado.
        valor_da_nota (float): Valor da nota ou moeda.
    Returns:
        int: Quantidade de notas ou moedas do valor especificado.
    """
    qntd_nota = 0
    while troco_total != 0:
        if troco_total >= valor_da_nota:
            troco_total = round(troco_total, 2) - valor_da_nota
            qntd_nota += 1
        else:
            break
    return qntd_nota

def conta_troco(troco_real, qntd_nota, valor_da_nota):
    """
    Atualiza o valor do troco após subtrair o valor das notas ou moedas.
    Args:
        troco_real (float): Valor atual do troco.
        qntd_nota (int): Quantidade de notas ou moedas.
        valor_da_nota (float): Valor da nota ou moeda.
    Returns:
        float: Valor atualizado do troco.
    """
    troco_real = troco_real - (qntd_nota * valor_da_nota)
    return troco_real

def quantidade_produto(num, sinal):
    """
    Atualiza a quantidade de um produto no carrinho e seu estoque.
    Args:
        num (int): Número do produto.
        sinal (str): '+' para adicionar ao carrinho, '-' para remover do carrinho.
    """
    if sinal == '-':
        produtos[f'Produto_{num}']['quantidade'] -= 1
        produtos[f'Produto_{num}']['estoque'] += 1
        botoes[num-1].configure(text=f'{produtos[f"Produto_{num}"]["nome"]}\nR$ {str(produtos[f"Produto_{num}"]["preco"]).replace(".",",")}\nEstoque: {produtos[f"Produto_{num}"]["estoque"]}')
        botoes[num-1].configure(state='normal')  # Reativa o botão se o produto foi removido do carrinho
    else:
        if produtos[f'Produto_{num}']['estoque'] == 0:
            pass  # Não faz nada se o produto estiver fora de estoque
        else:
            produtos[f'Produto_{num}']['quantidade'] += 1
            produtos[f'Produto_{num}']['estoque'] -= 1
            botoes[num-1].configure(text=f'{produtos[f"Produto_{num}"]["nome"]}\nR$ {str(produtos[f"Produto_{num}"]["preco"]).replace(".",",")}\nEstoque: {produtos[f"Produto_{num}"]["estoque"]}')

    # Calcula o valor total do carrinho
    valores = []
    for i in range(len(produtos)):
        valores.append(produtos[f'Produto_{i+1}']['preco'] * produtos[f'Produto_{i+1}']['quantidade'])
    total.configure(text=f'Total: R$ {str(round(float(sum(valores)), 2)).replace(".", ",")}')

    # Atualiza a exibição do carrinho
    if produtos[f'Produto_{num}']['quantidade'] == 0:
        texto_qntd[num-1].grid_forget()
        botao_menos[num-1].grid_forget()
    elif produtos[f'Produto_{num}']['estoque'] == 0:
        texto_qntd[num-1].configure(text=f'{produtos[f"Produto_{num}"]["quantidade"]} {produtos[f"Produto_{num}"]["nome"]}')
        mb.showwarning('Acabou o estoque', f'Acabou o estoque de {produtos[f"Produto_{num}"]["nome"]}')
        botoes[num-1].configure(state='disabled')  # Desativa o botão se o produto estiver fora de estoque
    else:
        texto_qntd[num-1].configure(text=f'{produtos[f"Produto_{num}"]["quantidade"]} {produtos[f"Produto_{num}"]["nome"]}')
        texto_qntd[num-1].grid(row=num-1, column=0, pady=2)
        botao_menos[num-1].grid(row=num-1, column=1, padx=10)

def maquina_venda():
    """
    Processa a compra: calcula o total, verifica o pagamento e dá o troco, se necessário.
    """
    try:
        valores = []
        for i in range(len(produtos)):
            valores.append(produtos[f'Produto_{i+1}']['preco'] * produtos[f'Produto_{i+1}']['quantidade'])

        if entrada.get() == '':
            mb.showwarning('Sem entrada de dinheiro', 'Por favor, entre com alguma quantia')
        else:
            valor_pago = float(entrada.get().replace(',', '.'))
            valor_total = float(sum(valores))

            if valor_total == 0.00:
                mb.showwarning('Carrinho vazio', 'Seu carrinho está vazio')
            else:
                if valor_pago > valor_total:
                    troco = float(valor_pago) - valor_total
                    saida = f'Troco a receber: R${troco:.2f}\n'

                    # Calcula a quantidade de cada nota e moeda para o troco
                    nota_100 = contagem_nota(troco, 100)
                    troco = conta_troco(troco, nota_100, 100)

                    nota_50 = contagem_nota(troco, 50)
                    troco = conta_troco(troco, nota_50, 50)

                    nota_20 = contagem_nota(troco, 20)
                    troco = conta_troco(troco, nota_20, 20)

                    nota_10 = contagem_nota(troco, 10)
                    troco = conta_troco(troco, nota_10, 10)

                    nota_5 = contagem_nota(troco, 5)
                    troco = conta_troco(troco, nota_5, 5)

                    nota_2 = contagem_nota(troco, 2)
                    troco = conta_troco(troco, nota_2, 2)

                    nota_1 = contagem_nota(troco, 1)
                    troco = conta_troco(troco, nota_1, 1)

                    moeda_50 = contagem_nota(troco, 0.50)
                    troco = conta_troco(troco, moeda_50, 0.50)

                    moeda_25 = contagem_nota(troco, 0.25)
                    troco = conta_troco(troco, moeda_25, 0.25)

                    moeda_10 = contagem_nota(troco, 0.10)
                    troco = conta_troco(troco, moeda_10, 0.10)

                    moeda_5 = contagem_nota(troco, 0.05)
                    troco = conta_troco(troco, moeda_5, 0.05)

                    moeda_1 = contagem_nota(troco, 0.01)
                    troco = conta_troco(troco, moeda_1, 0.01)

                    # Formata a mensagem de saída do troco
                    saida += '\n\nTroco composto por:\n'
                    saida += saida_troco('100 reais', nota_100)
                    saida += saida_troco('50 reais', nota_50)
                    saida += saida_troco('20 reais', nota_20)
                    saida += saida_troco('10 reais', nota_10)
                    saida += saida_troco('5 reais', nota_5)
                    saida += saida_troco('2 reais', nota_2)
                    saida += saida_troco('1 real', nota_1)
                    saida += saida_troco('50 centavos', moeda_50)
                    saida += saida_troco('25 centavos', moeda_25)
                    saida += saida_troco('10 centavos', moeda_10)
                    saida += saida_troco('5 centavos', moeda_5)
                    saida += saida_troco('1 centavo', moeda_1)
                    mb.showinfo('Seu troco', saida)

                    # Reseta o carrinho e o campo de entrada
                    total.configure(text='Total: R$ 0,00')
                    entrada.delete(0, ctk.END)
                    for i in range(6):
                        if produtos[f'Produto_{i+1}']['estoque'] == 0:
                            produtos[f'Produto_{i+1}']['estoque'] = random.randint(5, 10)  # Reabastece o estoque
                            botoes[i].configure(text=f'{produtos[f"Produto_{i+1}"]["nome"]}\nR$ {str(produtos[f"Produto_{i+1}"]["preco"]).replace(".",",")}\nEstoque: {produtos[f"Produto_{i+1}"]["estoque"]}', state='normal')
                        produtos[f'Produto_{i+1}']['quantidade'] = 0
                        texto_qntd[i].grid_forget()
                        botao_menos[i].grid_forget()

                elif valor_pago < valor_total and round(valor_total - valor_pago, 2) == 1:
                    mb.showwarning('Dinheiro insuficiente', f'Ainda falta: R$ {valor_total - valor_pago:.2f} real')
                elif valor_pago < valor_total and round(valor_total - valor_pago, 2) > 1:
                    mb.showwarning('Dinheiro insuficiente', f'Ainda faltam: R$ {valor_total - valor_pago:.2f} reais')
                elif valor_pago < valor_total and round(valor_total - valor_pago, 2) < 1 and round(valor_total - valor_pago, 2) > 0:
                    mb.showwarning('Dinheiro insuficiente', f'Ainda faltam: R$ {valor_total - valor_pago:.2f} centavos')
                else:
                    mb.showinfo('Dinheiro exato', 'Troco não necessário')
    except ValueError:
        mb.showerror('Erro de entrada', 'Erro de Entrada\nValor inválido. Use apenas números e vírgulas')

# Cria a janela principal da aplicação
janela = ctk.CTk()
ctk.set_appearance_mode("dark")  # Define o modo de aparência como escuro
janela.geometry('360x660')  # Define o tamanho da janela
vcmd = (janela.register(so_numero), '%P')  # Registra a função de validação de entrada
janela.title('Máquina de venda')  # Define o título da janela

# Rótulo do título da máquina de venda
ctk.CTkLabel(janela, text='--- Máquina de venda ---', font=('arial', 22, 'bold')).pack(pady=10)

# Frame para o campo de entrada do valor em dinheiro
Entry = ctk.CTkFrame(janela)
Entry.pack()
ctk.CTkLabel(Entry, text='R$', font=('arial', 16, 'bold')).pack(side=ctk.LEFT)
entrada = ctk.CTkEntry(Entry, width=80, validate='key', validatecommand=vcmd, font=('arial', 16, 'bold'))
entrada.pack(side=ctk.LEFT, pady=5, padx=5)
entrada.focus()

# Frame para exibir os produtos no carrinho
quadro_tela = ctk.CTkFrame(janela, width=100, height=30)
quadro_tela.pack(pady=15)
ctk.CTkLabel(janela, text='Escolha um ou mais produtos:', font=('arial', 18, 'bold')).pack(pady=10)

# Listas para armazenar os rótulos de quantidade e os botões de remover
texto_qntd = [None] * 6
botao_menos = [None] * 6
for i in range(len(texto_qntd)):
    texto_qntd[i] = ctk.CTkLabel(quadro_tela, text='', justify='left', font=('arial', 16, 'bold'))
    botao_menos[i] = ctk.CTkButton(quadro_tela, width=30, text='-1', command=lambda i=i: quantidade_produto(i+1, '-'), font=('arial', 12, 'bold'))

# Frame para os botões dos produtos
linha = ctk.CTkFrame(janela)
linha.pack(pady=5)
botoes = [None] * 6
for i in range(len(botoes)):
    botoes[i] = ctk.CTkButton(
        linha,
        font=('arial', 16),
        text=f'{produtos[f"Produto_{i+1}"]["nome"]}\nR$ {str(produtos[f"Produto_{i+1}"]["preco"]).replace(".",",")}\nEstoque: {produtos[f"Produto_{i+1}"]["estoque"]}',
        command=lambda i=i: quantidade_produto(i+1, '+'),
        width=150
    )
    botoes[i].grid(pady=5, padx=5)
    if i < 2:
        botoes[i].grid(row=0)
    elif i < 4:
        botoes[i].grid(row=1)
    else:
        botoes[i].grid(row=2)
    if i % 2 == 1:
        botoes[i].grid(column=1)
    elif i % 2 == 0:
        botoes[i].grid(column=0)

# Rótulo para exibir o valor total do carrinho
total = ctk.CTkLabel(janela, text='Total: R$ 0,00', font=('arial', 22, 'bold'))
total.pack()

# Botão para finalizar a compra
finalizar = ctk.CTkButton(janela, text='FINALIZAR COMPRA', anchor='center', command=maquina_venda, width=350, height=50, font=('arial', 20, 'bold'))
finalizar.pack()

janela.mainloop()
