from time import sleep
import sqlalchemy
import pyodbc
import os
import pandas as pd

#%%

class Database:
    """
    A singleton class to establish and manage a database connection.
    
    This class leverages pyodbc and sqlalchemy to establish a connection to a MySQL database,
    and offers a method to create a table from a pandas dataframe.
    
    Attributes
    ----------
    _instance : Database, optional
        Stores the singleton instance, by default None
    connection : pyodbc.Connection, optional
        Holds the database connection object, by default None
    constring : str, optional
        The connection string for the sqlalchemy engine, by default None
    server_address : str
        The server address for the database, fetched from environment variables.
    database_name : str
        The name of the database, fetched from environment variables.
    username : str
        The username to authenticate the database connection, fetched from environment variables.
    password : str
        The password to authenticate the database connection, fetched from environment variables.
    """
    _instance = None
    connection = None
    constring = None

    def __new__(cls, *args, **kwargs):
        """
        Ensure a single instance of Database is created. A new instance is created on the 
        first call and returned. Subsequent calls return the existing instance.
        
        Returns
        -------
        Database
            The singleton instance of the Database class.
        """
        if not Database._instance:
            Database._instance = super(Database, cls).__new__(cls, *args, **kwargs)
        return Database._instance

    def __init__(self):
        """
        Initialize the database connection attributes using environment variables.
        The environment variables used are: 'server_address', 'database_name', 'db_username', and 'password'.
        """
        self.server_address = os.environ['server_address']
        self.database_name = os.environ['database_name']
        self.username = os.environ['db_username']
        self.password = os.environ['password']
        

    def connect(self):
        """
        Establish a connection to a MySQL database using pyodbc. Constructs a connection string
        for sqlalchemy engine using the previously initialized attributes.
        
        Raises
        ------
        pyodbc.Error
            If the connection to the database could not be established.
        """
        if self.connection is None:
            self.connection = pyodbc.connect(
                'DRIVER={MySQL ODBC 8.0 Driver};SERVER=' +
                self.server_address + ';DATABASE=' + self.database_name + ';UID='
                + self.username + ';PWD=' + self.password)

            self.constring = f"mysql+pymysql://{self.username}:{self.password}@{self.server_address}/{self.database_name}"

    def dataframe_to_table(self, df: pd.DataFrame, table_name: str):
        """
        Create a table in the MySQL database from a pandas DataFrame. 
        If a table with the specified name already exists, it will be replaced.
        
        Parameters
        ----------
        df : pd.DataFrame
            The dataframe to be converted to a database table.
        table_name : str
            The name for the database table.
        
        Raises
        ------
        sqlalchemy.exc.SQLAlchemyError
            If there was an issue creating the engine or writing to the database.
        """


        cursor = self.connection.cursor()

        sql_query = f"CREATE TABLE if not exists {table_name}(id INT not NULL);"

        cursor.execute(sql_query)

        dbEngine = sqlalchemy.create_engine(self.constring,
                                            connect_args={'connect_timeout': 60},
                                            pool_recycle=3600,
                                            echo=False)
        df=df.astype(str)
        df.replace('None','',inplace=True)
        df.replace('nan','',inplace=True)
        df.replace('[]','',inplace=True)
        df.to_sql(con=dbEngine, name=table_name, if_exists="replace", index=True)
        
# if __name__=="__main__":

# database=Database()
# database.connect()
# df=pd.DataFrame(index=[0,1,2,3,4,5],columns=['teste'])
# database.dataframe_to_table(df,'teste')
