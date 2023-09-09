import os
import pandas as pd
import pytest
from your_module import Database  # substitua "your_module" pelo nome real do seu módulo

def setup_module(module):
    """ Setup para o módulo de teste, configurando as variáveis de ambiente """
    os.environ['server_address'] = 'localhost'  # Substitua conforme necessário
    os.environ['database_name'] = 'test_db'  # Substitua conforme necessário
    os.environ['db_username'] = 'test_user'  # Substitua conforme necessário
    os.environ['password'] = 'test_password'  # Substitua conforme necessário


def test_connect():
    """ Teste para o método connect """
    db = Database()
    db.connect()

    assert db.connection is not None
    assert db.constring is not None


def test_dataframe_to_table():
    """ Teste para o método dataframe_to_table """
    db = Database()
    db.connect()

    # Criar um DataFrame de exemplo
    data = {'Name': ['John', 'Anna'], 'Age': [28, 22]}
    df = pd.DataFrame(data)

    # Executando o método e verificando se a tabela é criada sem lançar exceções
    db.dataframe_to_table(df, 'test_table')

    # Você poderia adicionar mais verificações aqui, tal como consultar a tabela para verificar se os dados foram inseridos corretamente
