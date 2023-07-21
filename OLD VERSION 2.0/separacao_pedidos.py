import pyodbc
from configparser import ConfigParser

conn = None  # Variável global para armazenar a conexão com o banco de dados
cursor = None  # Variável global para armazenar o cursor

config = ConfigParser()
config.read('config.ini')

conn = None
cursor = None

def acessar_db():
    """Acessa o banco de dados SQL Server usando as configurações do arquivo config.ini."""
    global conn, cursor  # Utiliza as variáveis globais

    try:
        config = ConfigParser()
        config.read('config.ini')

        server = config.get('BancoDados', 'server')
        database = config.get('BancoDados', 'database')
        username = config.get('BancoDados', 'username')
        password = config.get('BancoDados', 'password')

        conn_string = f'DRIVER={{SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}'

        print("Conectando ao banco de dados...\n")
        conn = pyodbc.connect(conn_string)
        cursor = conn.cursor()

    except (configparser.Error, IOError) as e:
        print("Erro ao ler o arquivo de configuração:", str(e))

    return conn, cursor


def fechar_db():
    """Fecha a conexão com o banco de dados."""
    global conn, cursor  # Utiliza as variáveis globais
    if cursor is not None:
        cursor.close()
    if conn is not None:
        conn.close()


def comparar_db(cnpj):
    """Executa a separação de pedidos com base no CNPJ fornecido."""
    global cursor  # Utiliza a variável global
    try:
        query = f"SELECT * FROM CLIEN WHERE Cod_GrpCli IN (145, 146, 147) and Cgc_Cpf = '{cnpj}'"
        cursor.execute(query)
        resultados = cursor.fetchall()


        for resultado in resultados:

            #Pegar a coluna no banco de dados referente ao valor que quer armazenar nessa variavel
            cgc_cnpj = resultado[3]
            cod_estado = resultado[8]

            #Confere se o cnpj está batendo
            if cgc_cnpj == cnpj:

                if cod_estado == "RS":
                    return 'RS'

                elif cod_estado == "SC" or cod_estado == "PR":
                    return 'SC'

            #Caso não volte nenhum retorno o cliente não tem cadastro
            else:
                return 'Sem cadastro'
            break


    except pyodbc.Error as e:
        print("Erro ao executar a consulta no banco de dados:", e)
