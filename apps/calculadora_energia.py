
import datetime


def obter_numero_mes_atual():
    data_atual = datetime.datetime.now()
    numero_mes = data_atual.month
    return numero_mes

def calculadora_de_energia(tabela_energia):
    mes = None
    mes_atual = obter_numero_mes_atual()
    if 1 <= mes_atual <= 4:
        if mes_atual == 1:
            mes = tabela_energia[0]
        elif mes_atual == 2:
            mes = tabela_energia[1]
        elif mes_atual == 3:
            mes = tabela_energia[2]
        else:
            mes = tabela_energia[3]
    elif 4 < mes_atual <= 8:
        if mes_atual == 5:
            mes = tabela_energia[4]
        elif mes_atual == 6:
            mes = tabela_energia[5]
        elif mes_atual == 7:
            mes = tabela_energia[6]
        else:
            mes = tabela_energia[7]
    else:
        if mes_atual == 9:
            mes = tabela_energia[8]
        elif mes_atual == 10:
            mes = tabela_energia[9]
        elif mes_atual == 11:
            mes = tabela_energia[10]
        else:
            mes = tabela_energia[11]

    return mes


