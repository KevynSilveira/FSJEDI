import pyodbc

conn = None  # Variável global para armazenar a conexão com o banco de dados
cursor = None  # Variável global para armazenar o cursor

def access_db():
    """Acessa o banco de dados SQL Server usando as configurações do arquivo config.ini."""
    global conn, cursor  # Utiliza as variáveis globais

    try:
        server = ""
        database = ""
        username = ""
        password = ""

        # Monta os dados para enviar para o banco de dados (credenciais)
        conn_string = f'DRIVER={{SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}'
        conn = pyodbc.connect(conn_string)
        cursor = conn.cursor()
        print("Conexão concluida!")

    except:
        print("Erro ao conectar no banco")
    return conn, cursor

def close_db(): # Fecha a conexão com o banco de dados.

    global conn, cursor  # Utiliza as variáveis globais

    if cursor is not None:
        cursor.close()
    if conn is not None:
        conn.close()

def compare_db(cnpj): # Compara o cnpj recebido no banco de dados para identificar o estabelecimento

    global cursor  # Utiliza a variável global
    try:
        query = f"SELECT * FROM CLIEN WHERE Cod_GrpCli IN (145, 146, 147) and Cgc_Cpf = '{cnpj}'"
        cursor.execute(query)
        result = cursor.fetchall()

        for column in result: # Pegar a coluna no banco de dados referente ao valor que quer armazenar nessa variavel
            cgc_cnpj = column[3]
            cod_estado = column[8]

            if cgc_cnpj == cnpj: # Confere se o cnpj está batendo

                if cod_estado == "RS":
                    return 'RS'
                elif cod_estado == "SC" or cod_estado == "PR":
                    return 'SC'

            else: # Caso não volte nenhum retorno o cliente não tem cadastro
                return 'Sem cadastro'

            break

    except pyodbc.Error as e:
        print("Erro ao executar a consulta no banco de dados:", e)
