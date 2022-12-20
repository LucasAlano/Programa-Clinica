from connection import conexao
import menu

host = 'localhost'
usuario = 'root'
senha = 'satc@2022'
db = 'bancoclinica'


con = conexao.conexao(host,usuario,senha,db)

menu.menu(con)