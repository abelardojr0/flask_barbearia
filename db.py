import mysql.connector

def fazerConexao():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='10081995Ab.',
        database='barbearia'
    )
