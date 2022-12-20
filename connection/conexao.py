import mysql.connector as sql


def conexao(host, usuario, senha, db):

  try:
    connection = sql.connect(host=host,
                             user=usuario,
                             password=senha,
                             database=db)
    print('Conexão bem sucedida!')
    return connection
    
  except:
    print('Erro na conexão!')

def close_connection(con):
  try:
    con.close()
    print('Conexão fechada com sucesso.')
  except:
    print('Erro ao fechar a conexão.')