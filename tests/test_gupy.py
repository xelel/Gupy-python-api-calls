import os
import pytest
from your_module import Gupy # Substitua 'your_module' pelo nome do seu arquivo de script Python

def test_init():
    gupy = Gupy()
    assert gupy.token == os.environ['gupy_token']
    assert gupy.headers['Authorization'] == f"Bearer {os.environ['gupy_token']}"

def test_dict_to_dataframe():
    gupy = Gupy()
    data = [{"a": 1, "b": 2}, {"a": 3, "b": 4}]
    df = gupy._Gupy__dict_to_dataframe(data) # Notar a sintaxe de acesso a um método privado
    assert df.loc[0, "a"] == 1
    assert df.loc[1, "b"] == 4

def test_call_to_api(mocker):
    gupy = Gupy()
    url = "https://api.gupy.io/api/v1/jobs" # Substitua por um endpoint válido
    
    mocker.patch('requests.get')
    response = gupy.call_to_api(url, {})
    
    # Se a chamada à função 'requests.get' foi bem-sucedida, o método 'call_to_api' 
    # deveria retornar a resposta dessa função. Aqui verificamos se 'requests.get' foi chamado uma vez.
    requests.get.assert_called_once()

def test_fetch_requests(mocker):
    gupy = Gupy()
    url = "https://api.gupy.io/api/v1/jobs" # Substitua por um endpoint válido

    mocker.patch('requests.get')
    data = gupy.fetch_requests(url)
    
    # Você vai querer adicionar verificações adicionais aqui para garantir 
    # que a função 'fetch_requests' está processando a resposta da API corretamente.
    assert isinstance(data, list)

# Você vai querer escrever testes semelhantes para os outros métodos da classe 'Gupy'.

if __name__ == "__main__":
    pytest.main()
