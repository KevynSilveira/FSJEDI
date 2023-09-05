import os
import time
from ftputil import FTPHost
from tkinter import messagebox

hostname = ''
username = ''
password = ''
ftp_request_folder = '/Envio/'
ftp_return_folder = '/Retorno'
receive_local_folder = r'C:\FSJEDI\Processamento'
upload_local_folder_sc = r'D:\MEDMAIS\São João\SC\Retorno'
upload_local_folder_rs = r'D:\MEDMAIS\São João\RS\Retorno'

def connect(): # Faz a conexão com o FTP
    try: # Conectando ao servidor FTP
        ftp = FTPHost(hostname, username, password)
        return ftp

    except Exception as e: # Exibi o erro na tela
        messagebox.showerror("ATENÇÃO", f"Ocorreu uma exceção ao conectar: {str(e)}")
        return None

def close_connection(ftp): # Fecha a conexão de com o FTP
    try:
        if ftp is not None:
            ftp.close()
            print('\nEncerrado a conexão com o FTP.\n')

    except Exception as e: # Exibi o erro na tela
        messagebox.showerror("ATENÇÃO",f"Ocorreu uma exceção ao fechar a conexão: {str(e)}")

def download_file(): # Baixa os arquivos do FTP e recebe como parâmetro a conexão
    ftp = connect()
    try:
        if ftp is not None:
            ftp.chdir(ftp_request_folder) # Navegando para o diretório remoto
            lista_arquivos = ftp.listdir(ftp.curdir) # Obtendo a lista de arquivos no diretório remoto
            quantidade_arquivos = len(lista_arquivos) # Obtém a quantidade de arquivos na pasta

            if quantidade_arquivos == 0:
                print('\nA pasta está vazia.')
            else:
                print(f"\nNúmero de arquivos na pasta: {quantidade_arquivos}")
                cont = 0

                for arquivo in lista_arquivos: # Movendo os arquivos para a pasta local
                    caminho_local = os.path.join(receive_local_folder, arquivo)
                    ftp.download(arquivo, caminho_local)
                    ftp.remove(arquivo)
                    cont += 1
                print(f'\nForam importados {cont} arquivos.')

    except Exception as e: # Exibi o erro na tela
        messagebox.showerror("ATENÇÃO", f"Ocorreu uma exceção processar os arquivos no FTP: {str(e)}")


    finally:
        close_connection(ftp)
        last_processing_time = time.strftime("%H:%M:%S")
        print(f"\nÚltimo processamento em: {last_processing_time}")

def upload_file():  # Envia os retornos para o FTP
    ftp = connect()  # Estabelece a conexão FTP
    try:
        global ftp_return_folder, upload_local_folder_sc, upload_local_folder_rs

        if ftp is None:
            messagebox.showerror("Atenção", "Conexão FTP não está disponível.")
            return

        folders_to_upload = [upload_local_folder_sc, upload_local_folder_rs]

        for upload_local_folder in folders_to_upload:
            if not os.path.exists(upload_local_folder):
                messagebox.showerror("Atenção", "Diretório local não existe.")
                continue

            ftp.chdir(ftp_return_folder)

            for filename in os.listdir(upload_local_folder):
                if filename.endswith(".ret"):
                    local_path = os.path.join(upload_local_folder, filename)
                    new_filename = os.path.splitext(filename)[0] + ".RET"  # Troca a extensão para .RET
                    remote_path = os.path.join(ftp_return_folder, new_filename)

                    with open(local_path, "rb") as file:
                        ftp.storbinary(f"STOR {remote_path}", file)

                    os.remove(local_path)
                    print(f"Arquivo '{filename}' enviado como '{new_filename}' e removido localmente.")

                time.sleep(180)  # Delay de 3 minutos (180 segundos)

        print("\nTodos os retornos foram enviados com sucesso!")

    except Exception as e:
        messagebox.showerror("ATENÇÃO", f"Ocorreu uma exceção: {str(e)}")

    finally:
        close_connection(ftp)
        last_processing_time = time.strftime("%H:%M:%S")
        print(f"Último processamento em: {last_processing_time}")



