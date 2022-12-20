from datetime import date 
import menu

def cadastrar_agendamento(con):
    cpf_cliente = str(input('Informe o cpf do cliente, a qual o agendamento está sendo realizado:  '))

    if (cpf_cliente == ''):
        print(' Por favor prencher todos os campos! ')
        cadastrar_agendamento(con)
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
        cadastrar_agendamento(con)

    elementos = {
        'cpf': cpf_formatado,
    }
    


    # Achar se o cliente existe, fazendo uma busca pelo cpf.

    sql = ('select count(cd_cliente) from cliente where cpf_cliente = %(cpf)s')
    cursor_cpf = con.cursor()
    cursor_cpf.execute(sql, elementos)
    cpfs = cursor_cpf.fetchall()

    for i in cpfs:
        qntd_clientes = i[0]

    
    if (qntd_clientes > 1):
        print('Achamos ', qntd_clientes, ' Clientes!')
        print('Informe o codigo do cliente que deseja realizar o agendamento')
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
        opcao = str(input('Deseja mesmo cadastrar o agendamento nesse cpf: S-SIM, N-NÃO'))
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
            menu.menu(con)

        else:
             print('Informe uma opção valida !!')
             cadastrar_agendamento(con)
        
    
    if (qntd_clientes == 0):
        print('Informe um cpf valido!')
        cadastrar_agendamento(con)

    elementos = {
        'cd': cd_cliente,
        'cpf': cpf_formatado,
    }
    


    ds_agedamento = str(input('Informe a descrição do agendamento: '))

    data = str(input('Informe a data do agendamento: '))
    if (data == ''):
        print(' Por favor prencher todos os campos! ')
        cadastrar_agendamento(con)
    
    # Formatando data para cadastar no banco 
    dia = int(data[:2])
    mes = int(data[3:5])
    ano = int(data[6:])
    data_formatada = date(ano, mes, dia)


    dia_semana = str(input('Informe o dia da semana do agendamento ex.segunda : '))
    if (dia_semana.upper() == 'SEGUNDA') or (dia_semana.upper() == 'TERÇA') or (dia_semana.upper() == 'TERÇA') or (dia_semana.upper() == 'QUARTA') or (dia_semana.upper() == 'QUINTA') or (dia_semana.upper() == 'SEXTA'):
        pass
    else:
        print(' Os Agendamentos deverão ser feitos somente em dia de semana!! ')
        cadastrar_agendamento(con)
    
    
    elementos_agendamento = {
        'cd': '',
        'ds': ds_agedamento,
        'st': 'A',
        'cd_cliente': cd_cliente,
        'preco': 0,
    }

    
    
    try:
        sql = "INSERT into agendamento values (%(cd)s,%(ds)s,%(st)s,%(cd_cliente)s,%(preco)s)"
        cursor_agedamento = con.cursor()
        cursor_agedamento.execute(sql, elementos_agendamento)
        cursor_agedamento.execute('Commit')
    except:
        print('Erro ao cadastrar o agendamento')
    
    cursor_agedamento = con.cursor()
    cursor_agedamento.execute('select * from agendamento where cd_cliente = %(cd_cliente)s', elementos_agendamento)
    agendamentos = cursor_cliente.fetchall()
    for i in agendamentos:
        cd_agendamento = i[0]

    #Elementos para cadastrar
    elementos_data = {
        'cd': '',
        'data': data_formatada,
        'dia': 'Terça',
        'cd_agendamento': cd_agendamento,
    }
    # Cadastrar a Data
    try:
        sql = ('Insert into datas values (%(cd)s,%(data)s,%(dia)s,%(cd_agendamento)s)')
        cursor_data = con.cursor()
        cursor_data.execute(sql, elementos_data)
        cursor_data.execute('Commit')
    except:
        print('Erro para cadastar a data')
    
    # Pegando o codigo da data
    try:
        sql = ('select cd_data from datas')
        cursor_data = con.cursor()
        cursor_data.execute(sql)
        linhas = cursor_data.fetchall()
        for i in linhas:
            cd_data = i[0]
    except:
        print('Erro para achar o código da data')
        
    # Vendo quando horas existem nessa data, para o programa criar caso não exista. Foi a solução mais simples que encontrei sem ter que adicionar todas as horas para todas as datas.
    try:
        sql = ("select count(h.cd_horario) from horarios h right join datas d on h.cd_data = d.cd_data where d.data = %(data)s")
        cursor_hora = con.cursor()
        elementos_data={
            'data': data_formatada,
        }
        cursor_hora.execute(sql, elementos_data)
        resultados = cursor_hora.fetchall()
        for i in resultados:
            qnt_hora = i[0]


        if (qnt_hora == 0):
            elementos_hora = {
                'cd': '',
                'st': 'L',
                'cd_a': cd_data,
            }
            sql = ("insert into horarios values (%(cd)s,8,%(st)s,%(cd_a)s),(%(cd)s,9,%(st)s,%(cd_a)s),(%(cd)s,10,%(st)s,%(cd_a)s),(%(cd)s,11,%(st)s,%(cd_a)s),(%(cd)s,13,%(st)s,%(cd_a)s),(%(cd)s,14,%(st)s,%(cd_a)s),(%(cd)s,15,%(st)s,%(cd_a)s),(%(cd)s,16,%(st)s,%(cd_a)s)")
            cur_hora = con.cursor()
            cur_hora.execute(sql, elementos_hora)
            cur_hora.execute('Commit')
            cur_hora.close()
        else:
            cur_hora.close()
    except:
        print('Erro ao buscar as datas')

    #Mostrando as datas que estão disponíveis
    try:
        sql= ("select h.cd_horario,h.hora,h.status_horario from horarios h right join datas d on h.cd_data = d.cd_data where d.data = %(data)s and h.status_horario = 'L'")
        cur_hora = con.cursor()
        cur_hora.execute(sql, elementos_data)
        horas = cur_hora.fetchall()
        print('Horario disponivéis do dia: ')
        cur_hora.close()
        for i in horas:
            print('Horarios: ',i[1])
        
        hora_selecionada = int(input('Selecione um horario disponível para o agendamento: '))
    except:
        print('Erro ao buscar as datas disponíveis')

    
    #Achando o código da hora selecionada
    try:
        sql = ('Select h.cd_horario from horarios h right join datas d on h.cd_data = d.cd_data where d.data = %(data)s and h.hora = %(hora)s')
        cur_hora = con.cursor()
        elementos_hora_selecionada = {
            'data': data_formatada,
            'hora': hora_selecionada,
        }
        cur_hora.execute(sql, elementos_hora_selecionada)
        linha = cur_hora.fetchall()
        
        for i in linha:
            cd_hora_cli = i[0]        
    except:
        print('Erro ao encontrar a hora')
    
    #Aleterando o status da hora selecionada   
    try:
        sql = ('Update horarios set status_horario = "O",cd_data = %(cd_d)s where cd_horario = %(cd)s')
        elementos_statushora = {
            'cd': cd_hora_cli,
            'cd_d': cd_data,
        }
        cur_hora = con.cursor()
        cur_hora.execute(sql, elementos_statushora)
        cur_hora.execute('Commit')
        print('Agendamento cadastrado ao cliente com id:',cd_cliente)
        menu.menu(con)

    except:
       print('Erro ao mudar o status do horairo')

def cancelar_agendamento(con):
    cpf_cliente = str(input('Informe o cpf do cliente, a qual deseja buscar o agendamento:  '))

    if (cpf_cliente == ''):
        print(' Por favor prencher todos os campos! ')
        cancelar_agendamento(con)
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
        cancelar_agendamento(con)

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
             cancelar_agendamento(con)
        
    
    if (qntd_clientes == 0):
        print('Informe um cpf valido!')
        cancelar_agendamento(con)

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
    
    cd_agendamento = int(input('Informe o nº do agendamento que deseja cancelar: '))

    elementos_agendamento = {
        'cd': cd_agendamento,
        'st': 'D'
    }
    try:
        sql = ('Update agendamento set status_agendamento = %(st)s where cd_agendamento = %(cd)s')
        cur_agendamento = con.cursor()
        cur_agendamento.execute(sql, elementos_agendamento)
        cur_agendamento.execute('Commit')
        print('Agendamento nº', cd_agendamento, ' cancelado!')
        cur_agendamento.close()
        menu.menu(con)

    except:
        print('Erro ao cancelar o agendamento')