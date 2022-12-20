import menu

def cadastro_cliente(connection):

  nm_cliente = str(input('Informe o seu nome completo: '))
  if (nm_cliente == ''):
    print(' Por favor prencher todos os campos! ')
    cadastro_cliente(connection)
  
  dt_nascimento = str(input('Informe sua data de nascimento: '))
  if (dt_nascimento == ''):
    print(' Por favor prencher todos os campos! ')
    cadastro_cliente(connection)
  
  cpf_cliente = str(input('Informe o seu cpf: Obs. somente numeros  :'))
  if (cpf_cliente == ''):
    print(' Por favor prencher todos os campos! ')
    cadastro_cliente(connection)
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
    cadastro_cliente(connection)


  ec_cliente = str(input('Informe o seu estado civil: (S - SOLTEIRO, C - CASADO, V - VIÚVO)  : '))

  if (ec_cliente.upper() == 'S') or (ec_cliente.upper() == 'C') or (ec_cliente.upper() == 'V'):
    pass
  else:
    print(' Por favor selecione uma opção valida! ')
    cadastro_cliente(connection)

  if (ec_cliente == ''):
    print(' Por favor prencher todos os campos! ')
    cadastro_cliente(connection)

  sx_cliente = str(input('Informe o seu sexo: M - Masculino, F - Feminino   :'))
  if (sx_cliente == ''):
    print(' Por favor prencher todos os campos! ')
    cadastro_cliente(connection)
  
  if(sx_cliente.upper() == 'F') or (sx_cliente.upper() == 'M'):
    if(sx_cliente.upper() == 'F'):
      tp_sexo = 1
    else:
      tp_sexo = 0
  else: 
    print('Informe um sexo valido!')


  
  sql = ("Insert into cliente values ('',%s,%s,%s,%s,%s)")

  print(' Nome:',nm_cliente ,' Data nascimento:',dt_nascimento ,' CPF:',cpf_formatado, ' Estado civil:',ec_cliente , ' Sexo:',sx_cliente)
  opcion = str(input('Deseja realmente cadastrar esse usuário: S - SIM, N - NÃO :  '))

  if (opcion.upper() == 'S'):
    try:
      cur1 = connection.cursor()
      cur1.execute(sql, (nm_cliente, dt_nascimento, cpf_formatado, ec_cliente, tp_sexo))
      cur1.execute('Commit')
      print('Usuario cadastro com sucesso!!!')
      cur1.close()
      menu.menu(connection)
    except:
      print('Erro no cadastro de cliente')
  else:
    print('Cadastro abortado!! ')
    menu.menu(connection)


