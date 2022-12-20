import menu

def adicionar_preco(con):

    cpf_cliente = str(input('Informe o cpf do cliente, a qual deseja buscar o agendamento:  '))

    if (cpf_cliente == ''):
        print(' Por favor prencher todos os campos! ')
        adicionar_preco(con)
    if (len(cpf_cliente) == 11):
        fatia_1 = cpf_cliente[:3]
        fatia_2 = cpf_cliente[3:6]
        fatia_3 = cpf_cliente[6:9]
        fatia_4 = cpf_cliente[9:]

        cpf_formatado = "{}.{}.{}-{}".format(
        fatia_1,
        fatia_2,
        fatia_3,
        fatia_4
        ) 
    else:
        print('Informe o seu cpf completo por favor!')
        adicionar_preco(con)

    elementos = {
        'cpf': cpf_formatado,
    }

    try:
        sql = ('select count(cd_cliente) from cliente where cpf_cliente = %(cpf)s')
        cursor_cpf = con.cursor()
        cursor_cpf.execute(sql, elementos)
        cpfs = cursor_cpf.fetchall()

        for i in cpfs:
            qntd_clientes = i[0]
    except:
        print('Erro ao buscar o cliente')

    
    if (qntd_clientes > 1):
        print('Achamos ', qntd_clientes, ' Clientes!')
        print('Informe o codigo do cliente que deseja buscar o agendamento')
        try: 
            cursor_cliente = con.cursor()
            cursor_cliente.execute('SELECT * from Cliente where cpf_cliente = %(cpf)s', elementos)
            clientes = cursor_cliente.fetchall()
            for i in clientes:
                print(i)
        except:
            print('Erro ao procurar os clientes')
    
        cd_cliente = int(input('Informe o código do cliente desejado: '))
    
    if (qntd_clientes == 1):
        print('Cpf selecionado: ', elementos['cpf'])
        opcao = str(input('Deseja mesmo buscar o agendamento nesse cpf: S-SIM, N-NÃO'))
        if (opcao.upper() == 'S'):
            try: 
                cursor_cliente = con.cursor()
                cursor_cliente.execute('select * from cliente where cpf_cliente = %(cpf)s', elementos)
                cliente = cursor_cliente.fetchall()
                for i in cliente:
                    print(i)
                    cd_cliente = i[0] 
            except:
                print('Erro ao procurar o codigo do cliente')
            
            #cd_cliente = int(input('Informe o código do cliente desejado: '))
        elif (opcao.upper() == 'N'):
            print('Opcão abortada!')
        else:
             print('Informe uma opção valida !!')
             adicionar_preco(con)
        
    
    if (qntd_clientes == 0):
        print('Informe um cpf valido!')
        adicionar_preco(con)

    elementos_busca = {
        'cd_c':cd_cliente,
        'st': 'A',
    }

    # Mostrando os agendamentos desse cpf (Data, dia hora etc.):
    try: 
        sql = ("""Select c.cpf_cliente, a.cd_agendamento, a.descricao, d.data, d.dia_semana, h.hora 
            from cliente c inner join agendamento a on c.cd_cliente = a.cd_cliente 
            inner join datas d on a.cd_agendamento = d.cd_agendamento 
            inner join horarios h on d.cd_data = h.cd_data 
            where c.cd_cliente = %(cd_c)s and a.status_agendamento = %(st)s and h.status_horario = 'O'""")
        cur_cliente = con.cursor()
        cur_cliente.execute(sql, elementos_busca)
        linhas = cur_cliente.fetchall()
        if (len(linhas) == 0):
            print('Nenhum agendamento resultante ao cpf nº', cpf_formatado)
        else:
            for i in linhas:
                print('---'*20)
                print('Agendamento nº: ',i[1]) 
                print('cadastrado no cpf nº: ',i[0])
                print('com descrição: ',i[2])
                print('na data :',i[3])
                print('na: ',i[4], 'feira')
                print('na hora: ',i[5])
                print('---'*20)
    except:
        print('Erro ao achar agendamento')
    
    cd_agendamento = int(input('Informe o nº do agendamento que deseja cadastrar o serviço: '))

    #Mostrando os preços
    print("""
            Opções de serviços
            1 - Clínica Geral, preço R$ 150
            2 - Clareamento, preço R$ 250
            3 - Clareamento de canal, preço R$ 350
            4 - Implante Dentário, preço R$ 500""")
    cd_servico = int(input('Seleciona UMA das opções: '))
    
    # Alterando e botando o preço do serviço
    if (cd_servico == 1):
        preco_servico = 150
    elif(cd_servico == 2):
        preco_servico = 250
    elif(cd_servico == 3):
        preco_servico = 350
    elif(cd_servico == 4):
        preco_servico = 500
    else:
        print('Informe um código valido!')
        adicionar_preco(con)
    
   
    #Acremento o preço do serviço com o existente, (Cada agendamento pode ter + de 1 serviço)
    try:
        sql = ('Select preco_agendamento from agendamento where cd_agendamento = %(cd)s')
        elementos = {
            'cd': cd_agendamento
        }
        cur_preco = con.cursor()
        cur_preco.execute(sql, elementos)
        linha = cur_preco.fetchall()
        preco_servico_ant = 0
        for i in linha:
            preco_servico_ant = i[0]

        cur_preco.close()
    except:
        print('Erro ao procurar o preço do serviço')
    
    preco_total = preco_servico_ant + preco_servico

    # Alterando os preço do serviço
    try:
        sql = ("update agendamento set preco_agendamento = %(preco)s where cd_agendamento = %(cd)s")
        elementos_alterar = {
        'cd': cd_agendamento,
        'preco': preco_total,
        }
        cur_update = con.cursor()
        cur_update.execute(sql, elementos_alterar)
        cur_update.execute('Commit')
        print('Serviço cadastrado com sucesso, o novo valor do agendamento é :', elementos_alterar['preco'])
        cur_update.close()
    except:
       print('Erro ao atualizar o preço do serviço ')

    #Opção para adicionar mais serviços
    opcao = str(input('Cadastar mais um serviço ? S-SIM N-NÃO'))
    if (opcao.upper() == 'S'):
        adicionar_preco(con)
    else:
        menu.menu(con)
