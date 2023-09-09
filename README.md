
# Projeto Gupy API

Este projeto facilita a interação com a API da Gupy, recuperando e organizando dados em dataframes pandas para posterior armazenamento em um banco de dados.

## Estrutura do Projeto

O projeto contém os seguintes arquivos principais:

- `gupy.py`: Este script contém a classe `Gupy` que facilita a interação com a API da Gupy.
- `main.py`: Este script usa a classe `Gupy` para buscar dados da API da Gupy e armazená-los em um banco de dados.
- `dbapp.py`: (Nota: Este arquivo não foi fornecido, presumimos que ele contém a classe `Database` para interagir com o banco de dados)
- `Dockerfile`: Este arquivo contém instruções para construir uma imagem Docker para a aplicação.
- `odbcinst.ini`: Este arquivo contém configurações para o driver ODBC utilizado pela aplicação.
- `requirements.txt`: Este arquivo lista todas as dependências Python necessárias para executar a aplicação.

## Configuração de Variáveis de Ambiente

As seguintes variáveis de ambiente precisam ser configuradas no arquivo `Dockerfile`:

- `server_address`: O endereço do seu servidor de banco de dados.
- `database_name`: O nome do seu banco de dados.
- `db_username`: O nome de usuário para acessar seu banco de dados.
- `password`: A senha para acessar seu banco de dados.

Você pode definir estas variáveis no `Dockerfile` da seguinte maneira:


ENV server_address='seu_endereço_aqui'
ENV database_name='seu_nome_aqui'
ENV db_username='seu_usuário_aqui'
ENV password='sua_senha_aqui'


### Descrição dos Arquivos

#### `dbapp.py`

Este arquivo contém a classe `Database`, que é um singleton usado para gerenciar conexões com um banco de dados MySQL através dos módulos `pyodbc` e `sqlalchemy`. A classe utiliza variáveis de ambiente para obter as credenciais e detalhes necessários para estabelecer a conexão com o banco de dados.

Aqui está uma visão geral dos métodos da classe `Database`:

- `__new__`: Garante que apenas uma instância de `Database` seja criada, seguindo o padrão singleton.
- `__init__`: Inicializa os atributos de conexão do banco de dados usando as variáveis de ambiente: 'server_address', 'database_name', 'db_username', e 'password'.
- `connect`: Estabelece uma conexão com o banco de dados MySQL e constrói uma string de conexão para o engine `sqlalchemy`.
- `dataframe_to_table`: Este método aceita um DataFrame pandas e um nome de tabela como parâmetros e cria (ou substitui se já existir) uma tabela no banco de dados MySQL a partir do DataFrame fornecido.

A classe também contém vários atributos para armazenar detalhes da conexão, como o endereço do servidor, nome do banco de dados, nome de usuário e senha.


#### `gupy.py`

Este arquivo contém a classe `Gupy`, que facilita a interação com a API da Gupy, permitindo buscar e organizar dados em DataFrames do pandas. Abaixo, estão detalhadas as funcionalidades dos principais métodos:

- `__init__`: Inicializa uma nova instância da classe Gupy, definindo os headers para as requisições HTTP feitas à API da Gupy.
- `fetch_requests`: Busca dados de um endpoint específico da API da Gupy e retorna uma lista de dicionários contendo os dados da resposta JSON da API.
- `__dict_to_dataframe`: Um método privado que converte um dicionário em um DataFrame pandas.
- `call_to_api`: Realiza uma chamada API para um endpoint específico da API da Gupy. Este método lida com vários tipos de erros e gerencia os limites de taxa, pausando o tempo necessário antes de fazer uma nova solicitação.
- `gupy_applications`: Recupera dados de candidaturas para um ID de trabalho específico da API da Gupy e retorna como um DataFrame pandas.
- `gupy_comments`: Busca dados de comentários para um trabalho específico e ID de aplicativo da API da Gupy e retorna como um DataFrame pandas.
- `gupy_jobs`: Busca dados de empregos da API da Gupy e retorna como um DataFrame pandas.
- `gupy_steps`: Recupera dados dos passos de um trabalho específico da API da Gupy e retorna como um DataFrame pandas.

No bloco `if __name__ == "__main__"` no final do script, há um exemplo de como instanciar a classe Gupy e utilizar seus métodos para recuperar dados de trabalhos, candidaturas e passos, e armazená-los em DataFrames pandas.

**Observação**: No método `__init__`, o token de autorização está hard-coded. Para manter a segurança, é recomendado substituir isso por uma variável de ambiente ou algum outro método seguro de armazenamento e acesso a informações sensíveis.

Se houver mais detalhes específicos que você gostaria de incluir ou modificar, me avise. Depois de revisar e confirmar, podemos passar para a descrição do próximo arquivo.


#### `main.py`

O arquivo `main.py` é o script principal que combina funcionalidades dos módulos `dbapp.py` e `gupy.py` para buscar dados da API da Gupy e armazená-los em um banco de dados MySQL. Abaixo está o detalhamento de cada etapa do script:

1. **Importação de Módulos**
   - Importa a classe `Database` do arquivo `dbapp.py`.
   - Importa a classe `Gupy` do arquivo `gupy.py`.
   - Importa o módulo `pandas` como `pd`.

2. **Instanciamento da Classe Gupy**
   - Cria uma nova instância da classe Gupy para interagir com a API da Gupy.

3. **Recuperação de Dados**
   - Recupera a lista de trabalhos disponíveis utilizando o método `gupy_jobs`.
   - Inicia dois DataFrames vazios: `df_app` para armazenar dados de aplicativos e `df_steps` para armazenar dados de passos (steps).
   - Utiliza um loop para iterar sobre todos os IDs de trabalhos e, para cada ID, recupera os dados de aplicativos e passos correspondentes, acumulando-os nos DataFrames criados anteriormente.

4. **Instanciamento e Conexão com o Banco de Dados**
   - Cria uma nova instância da classe Database.
   - Estabelece uma conexão com o banco de dados utilizando o método `connect`.

5. **Carregamento de Dados no Banco de Dados**
   - Utiliza o método `dataframe_to_table` para carregar cada DataFrame (`df_jobs`, `df_app`, `df_steps`) no banco de dados, criando (ou substituindo, se já existirem) as tabelas "Jobs", "Applications" e "Steps", respectivamente.

**Notas Importantes**:

- O script está configurado para substituir as tabelas existentes no banco de dados a cada execução. Se desejar preservar os dados existentes, pode ser necessário ajustar o parâmetro `if_exists` no método `dataframe_to_table`.

### 🐳 Docker

#### `Dockerfile`

O `Dockerfile` especifica as instruções necessárias para criar um ambiente Docker para rodar a aplicação Python. Segue o detalhamento de cada seção e comando usado no Dockerfile:

1. **Imagem Base e Mantenedor**
   - **`FROM python:3.10`**: Define a imagem base como Python 3.10.
   - **`LABEL maintainer = "Gupy"`**: Define o mantenedor da imagem como "Gupy".

2. **Variáveis de Ambiente**
   - **`ENV`** comandos: Define variáveis de ambiente para configuração do banco de dados.

3. **Cópia dos Requisitos**
   - **`COPY ./requirements.txt ./`**: Copia o arquivo `requirements.txt` do diretório atual para o diretório de trabalho no container.

4. **Configuração do ODBC**
   - **`ADD odbcinst.ini /etc/odbcinst.ini`**: Adiciona o arquivo de configuração ODBC ao diretório `/etc` do container.
   - A série de comandos **`RUN`** que seguem instalam o driver ODBC da Microsoft e o MySQL ODBC Connector, permitindo conexões com bancos de dados MySQL e Microsoft SQL Server.

5. **Instalação de Dependências**
   - **`RUN pip3 install --upgrade pip`**: Atualiza o pip para a última versão disponível.
   - **`RUN pip3 --no-cache-dir install -r requirements.txt`**: Instala as bibliotecas Python necessárias para a aplicação, como especificado no arquivo `requirements.txt`.

6. **Definição do Diretório de Trabalho e Cópia dos Arquivos**
   - **`WORKDIR /`**: Define o diretório de trabalho como `/`.
   - **`COPY ./ /`**: Copia todos os arquivos do diretório atual para o diretório de trabalho no container.

7. **Exposição de Portas**
   - **`EXPOSE 9000`**: Expõe a porta 9000, indicando que o aplicativo irá utilizar essa porta.

8. **Comando de Inicialização**
   - **`CMD ["python3", "-u", "-m", "main"]`**: Define o comando para iniciar a aplicação Python ao iniciar o container.

**Nota Importante**:

- **Variáveis de Ambiente**: É fundamental que os valores para as variáveis de ambiente `server_address`, `database_name`, `db_username` e `password` sejam fornecidos corretamente para que a aplicação possa se conectar ao banco de dados. Estas variáveis podem ser configuradas através do Docker ao criar um container, ou através de um arquivo `docker-compose.yml`.

#### `odbcinst.ini`

O arquivo `odbcinst.ini` é utilizado para definir os drivers ODBC que estarão disponíveis no seu sistema. Neste caso, você está definindo um driver para o FreeTDS, que é um conjunto de bibliotecas que permite que seu aplicativo se conecte a servidores de banco de dados que falam o protocolo TDS, como o SQL Server da Microsoft e o Sybase.

Vamos analisar o conteúdo desse arquivo:

Este arquivo configura o driver ODBC para o FreeTDS no seu sistema. Aqui estão os detalhes dos parâmetros configurados:

- **`[FreeTDS]`**:
  - Esta é a definição do nome do DSN (Data Source Name) que será usado para referenciar esta configuração específica de conexão.
   
- **`Description=FreeTDS Driver`**:
  - Define uma descrição amigável para identificar o driver ODBC no sistema.
  
- **`Driver=/usr/lib/x86_64-linux-gnu/odbc/libtdsodbc.so`**:
  - Especifica o caminho completo para o arquivo de biblioteca do driver ODBC. Este é o driver que implementa as funções ODBC para este DSN.

- **`Setup=/usr/lib/x86_64-linux-gnu/odbc/libtdsS.so`**:
  - Define o caminho para o arquivo de configuração de setup do driver. Este arquivo auxilia na configuração do DSN e geralmente é fornecido junto com o driver.


### 📋 Requisitos

#### `requirements.txt`

- **Bibliotecas**: Lista de todas as bibliotecas Python necessárias para o projeto.

## 🔧 Como Usar

### Pré-requisitos

- Python 3.10
- Docker

### Instruções

1. Clone o repositório para o seu ambiente local.
2. Navegue até o diretório do projeto.
3. Construa a imagem Docker usando o seguinte comando:

```sh
docker build -t gupy-api .
```

4. Após construir a imagem, inicie um container Docker usando o seguinte comando:

```sh
docker run -p 9000:9000 gupy-api
```

O aplicativo agora deve estar rodando e acessível através da porta 9000.

## 📚 Dependências

### Descrição das Bibliotecas

- **`pymysql`**:
  - É um cliente MySQL para Python. Esta biblioteca permite que você se conecte a um banco de dados MySQL a partir de um aplicativo Python.
  
- **`sqlalchemy`**:
  - É um toolkit SQL e Object-Relational Mapping (ORM) para Python. Ele permite trabalhar com banco de dados de uma maneira pythonic, além de fornecer uma API de baixo nível para trabalhar diretamente com SQL puro, se necessário.
  
- **`pyodbc`**:
  - É uma biblioteca Python que facilita o acesso a bancos de dados através de conexões ODBC, uma especificação padrão para conexões de banco de dados.

- **`numpy`**:
  - É uma biblioteca fundamental para computação científica em Python. Ele oferece suporte para arrays, matrizes e funções matemáticas para manipulação dessas estruturas de dados.

- **`pandas`**:
  - É uma biblioteca de análise de dados de código aberto rápida, poderosa, flexível e fácil de usar. É construída sobre a biblioteca `numpy`.

- **`requests`**:
  - É uma biblioteca HTTP para Python, lançada sob a licença Apache2. É uma biblioteca fácil de usar para fazer solicitações HTTP (GET, POST, etc.) em Python.

### Uso no seu Projeto

- **`pandas`** e **`numpy`**:
  - No script `gupy.py`, você está usando pandas para manipular e estruturar os dados que você está recuperando da API Gupy.
  
- **`requests`**:
  - Também em `gupy.py`, você está usando a biblioteca requests para fazer chamadas API para a API Gupy.

- **`pyodbc`, `sqlalchemy`** e **`pymysql`**:
  - Essas bibliotecas provavelmente são usadas em `dbapp.py` (não fornecido) para manipular conexões de banco de dados e operações relacionadas ao banco de dados.

Certifique-se de que todas as versões das bibliotecas que você está usando são compatíveis entre si para evitar problemas de dependência. Se você sabe que precisa de versões específicas de algumas dessas bibliotecas, você pode especificar a versão ao lado do nome da biblioteca no `requirements.txt`, como por exemplo:

```plaintext
numpy==1.21.0
```

Isso garantirá que a versão 1.21.0 da biblioteca numpy seja instalada.


# Guia de Testes para o Módulo Gupy

Este guia oferece instruções para executar os testes unitários para o módulo Gupy.

## Pré-requisitos

Certifique-se de ter as seguintes ferramentas e bibliotecas instaladas em seu ambiente de desenvolvimento:

- Python 3.8 ou superior
- pytest
- pytest-mock

Para instalar `pytest` e `pytest-mock`, use os seguintes comandos:

```bash
pip install pytest
pip install pytest-mock
```

## 🤝 Contribuições

Sinta-se à vontade para abrir issues ou pull requests para contribuir com o projeto!

## 📧 Contato

Para qualquer dúvida ou feedback, entre em contato através de [marcell.leao@gmail.com](mailto:seu@email.com).



