# Importa o conector do MySQL.
import mysql.connector

#* Função que faz a conexão com o banco de dados MySQL.
def open_connection():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='SENAIplus',
    )

#cursor.lastrowid
# Função para comunicação com o banco de dados MySQL.
def consultaBD(SQL, opcao=0, valor=None):
    resultado = None
    connection = open_connection()
    cursor = connection.cursor()

    try:
        if valor:
            cursor.execute(SQL, valor)
        else:
            cursor.execute(SQL)

        match opcao:
            case 0:
                connection.commit()
            case 1:
                resultado = cursor.fetchone()
            case 2:
                resultado = cursor.fetchall()
            case 3:
                connection.commit()
                resultado = cursor.lastrowid  

    finally:
        cursor.close()
        connection.close()

    return resultado