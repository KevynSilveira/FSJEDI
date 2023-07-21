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

    try:
        file_list = os.listdir(directory_origin) # Armazena a lista dos arquivos presente na pasta
        for file in file_list: # Faz uma varredura da lista de arquivo, acessando arquivo por arquivo

            if file.endswith('.txt'): # Verifica se é um arquivo .txt
                origin_file_path = os.path.join(directory_origin, file) # Cria um caminho do arquivo

                global directory_sc, directory_rs # Chama a variavel global
                if os.path.exists(os.path.join(directory_rs, file) or os.path.join(directory_sc, file)): # Verifica se o arquivo ja existe no diretorio de envio
                    os.remove(origin_file_path) # Remove o arquivo, para evitar duplicidade de pedido
                    continue

                with open(origin_file_path, 'r') as file_txt: # Abre os arquivos para leitura
                    global cnpj_client, file_client # Chama as variaveis global
                    file_client = file_txt.readline() # Armazena a primeira linha do arquivo
                    cnpj_client = file_client[1:15] # Pega o CNPJ do cliente no arquivo
                    establishment = compare_db(cnpj_client) # Compara o cnpj no banco de dados

                global directory_sc, directory_rs # Chama as variaveis global
                destination_directory_sc = os.path.join(directory_sc, file) # Cria o caminho para envio dos arquivos de sc
                destination_directory_rs = os.path.join(directory_rs, file) # Cria o caminho para envio dos arquivos de rs

                if establishment == "RS": # Verifica se o arquivo é do rs
                    shutil.move(origin_file_path, destination_directory_rs)
                elif establishment == "SC": # Verifica se o arquivo é do rs
                    shutil.move(origin_file_path, destination_directory_sc)
                else: # Retorno caso o termo SC ou RS não seja armazenado corretamente na variavel
                    print("Retorno esta incorreto")

                global total_processed_files # Chama a variavel global
                total_processed_files += 1 # Soma mais um em arquivos processados

                print(f"O arquivo {file} foi processado!")

            global total_processed_files # Chama a variavel global
            print(f"Total de arquivos processados {total_processed_files}")

    except FileNotFoundError:
        print("O arquivo não foi encontrado!")
