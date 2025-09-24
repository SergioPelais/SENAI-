# Importa o conector do MySQL.
import mysql.connector

#* Função que faz a conexão com o banco de dados MySQL.
def open_connection():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='Dev@561',
        database='SENAIplus',
    )


# Função para comunicação com o banco de dados MySQL.
def consultaBD(SQL,opcao=0,valor=''):
    consulta = ''
    connection = open_connection()
    cursor = connection.cursor(buffered=True)
    if valor == '':
        cursor.execute(SQL)
    else:
        cursor.execute(SQL,valor)

    match opcao:
        case 0: connection.commit()
        case 1: consulta = cursor.fetchall()
        case 2: consulta = cursor.fetchone()
        
    cursor.close()
    connection.close()
    return consulta