import os
import shutil
from CONSULTA import compare_db
from CONSULTA import access_db
from CONSULTA import close_db
import time
from BOTAO import status, stop_processing


# Variaveis global
file_client = "" # Armazena o arquivo do cliente
cnpj_client = "" # Armazena o cnpj do cliente
establishment = ""
directory_origin = r"C:\FSJEDI\Processamento" # Diretório local
directory_sc = r"C:\Users\Kevyn\Documents\Destino\SC" # Diretório de envio sc
directory_rs = r"C:\Users\Kevyn\Documents\Destino\RS" # Diretório de envio rs

total_processed_files = 0 # Total de arquivos processados

def separate_file(): # Separa e envia os arquivos por estabelecimento
    # Chama as variaveis globais
    global cnpj_client, file_client, directory_rs, directory_sc, directory_origin, total_processed_files, establishment, status
    access_db()
    try:
        file_list = os.listdir(directory_origin) # Armazena a lista dos arquivos presente na pasta
        for file in file_list: # Faz uma varredura da lista de arquivo, acessando arquivo por arquivo

            if stop_processing:
                break

            if file.endswith('.txt'): # Verifica se é um arquivo .txt
                origin_file_path = os.path.join(directory_origin, file) # Cria um caminho do arquivo

                if os.path.exists(os.path.join(directory_rs, file) or os.path.join(directory_sc, file)): # Verifica se o arquivo ja existe no diretorio de envio
                    os.remove(origin_file_path) # Remove o arquivo, para evitar duplicidade de pedido
                    continue

                with open(origin_file_path, 'r') as file_txt: # Abre os arquivos para leitura
                    file_client = file_txt.readline() # Armazena a primeira linha do arquivo
                    cnpj_client = file_client[1:15] # Pega o CNPJ do cliente no arquivo
                    establishment = compare_db(cnpj_client) # Compara o cnpj no banco de dados

                destination_directory_sc = os.path.join(directory_sc, file) # Cria o caminho para envio dos arquivos de sc
                destination_directory_rs = os.path.join(directory_rs, file) # Cria o caminho para envio dos arquivos de rs

                if establishment == "RS": # Verifica se o arquivo é do rs
                    shutil.move(origin_file_path, destination_directory_rs)
                elif establishment == "SC": # Verifica se o arquivo é do rs
                    shutil.move(origin_file_path, destination_directory_sc)
                else: # Retorno caso o termo SC ou RS não seja armazenado corretamente na variavel
                    print("Retorno esta incorreto")

                total_processed_files += 1 # Soma mais um em arquivos processados

                print(f"O arquivo {file} foi processado!")

            print(f"Total de arquivos processados {total_processed_files}")
        close_db()
        time.sleep(300)  # Pausa de 5 minutos antes da próxima verificação
    except FileNotFoundError:
        print("O arquivo não foi encontrado!")
