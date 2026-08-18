# CONEXÃO COM BANCO #

import mysql.connector


def conectar():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="roo123",
        database="sistema_escolar"
    )