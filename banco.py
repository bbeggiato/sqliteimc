import sqlite3
from sqlite3 import Error
import os

pastaApp = os.path.dirname(__file__)
nomeBanco = pastaApp+"\\academia.db"

def ConexaoBanco():
    conexao = None
    try:
        conexao = sqlite3.connect(nomeBanco)
    except Error as ex:
        print(ex)
    return conexao

def dql(query): #select
    varConexao = ConexaoBanco()
    ponteiro = varConexao.cursor()
    ponteiro.execute(query)
    res = ponteiro.fetchall()
    varConexao.close()
    return res

def dml(query): #insert,update,delete
    try:
        varConexao = ConexaoBanco()
        ponteiro = varConexao.cursor()
        ponteiro.execute(query)
        varConexao.commit()  # select não faz alteração na tabela
        varConexao.close()
    except Error as ex:
        print(ex)

