import os
import shutil
from CONSULTA import compare_db

# Variaveis global
file_client = ""
cnpj_client = ""
directory_origin = ""
directory_sc = ""
directory_rs = ""
total_processed_files = 0

def separate_file(): # Separa e envia os arquivos por estabelecimento

    file_list = os.listdir(directory_origin)
    for file in file_list:

        if file.endswith('.txt'): # Verifica se é um arquivo .txt

            origin_file_path = os.path.join(directory_origin, file) # Cria um caminho do arquivo

            if os.path.exists(os.path.join(directory_rs, file) or os.path.join(directory_sc, file)): # Verifica se o arquivo ja existe no diretorio de envio
                os.remove(origin_file_path)
                continue

            with open(origin_file_path, 'r') as file_txt: # Abre os arquivos para leitura
                nonlocal cnpj_client, file_client # Chama as variaveis global
                file_client = file_txt.readline() # Armazena a primeira linha do arquivo
                cnpj_client = file_client[1:15] # Pega o CNPJ do cliente no arquivo
                compare_db(cnpj_client) # Compara o cnpj no banco de dados

