from connection import conexao
from connection import user
from connection import schedule
from connection import price_shcedule
from reports import reports


def menu(con):
    opcao = int(input("""
    --------------------------------------
    Escolha algumas das opções:
        1 - Cadastrar cliente
        2 - Realizar Agendamento
        3 - Cancelar Agendamento
        4 - Cadastro de serviço
        5 - Relatórios
        6 - Sair

    Opção desejada: """))

    if (opcao == 1):
        user.cadastro_cliente(con)
    elif (opcao == 2):
        schedule.cadastrar_agendamento(con)
    elif(opcao == 3):
        schedule.cancelar_agendamento(con)
    elif(opcao == 4):
        price_shcedule.adicionar_preco(con)
    elif(opcao == 5):
        reports.menu_relatorio(con)
    elif(opcao == 6):
        print('Programa encerrado')
        quit()
        