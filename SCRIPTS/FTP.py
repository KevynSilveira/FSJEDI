import os
import time
from ftputil import FTPHost
from tkinter import messagebox

hostname = ''
username = ''
password = ''
ftp_request_folder = '/Envio/'
ftp_return_folder = '/Retorno'
receive_local_folder = r'C:\FSJEDI\Recebimento'
upload_local_folder_sc = r'C:\FSJEDI\Envio'
upload_local_folder_rs = r'C:\FSJEDI\Envio'

def connect(): # Faz a conexão com o FTP
    try: # Conectando ao servidor FTP

        ftp = FTPHost(hostname, username, password)
        print('Conectou no FTP.')

        return ftp

    except Exception as e: # Exibi o erro na tela
        print(f"Ocorreu uma exceção ao conectar: {str(e)}")
        return None

def close_connection(ftp): # Fecha a conexão de com o FTP
    try:

        if ftp is not None:
            ftp.close()
            print('Conexão FTP fechada.')

    except Exception as e: # Exibi o erro na tela
        print(f"Ocorreu uma exceção ao fechar a conexão: {str(e)}")

def download_file(): # Baixa os arquivos do FTP e recebe como parâmetro a conexão
    ftp = connect()
    try:

        if ftp is not None:

            ftp.chdir(ftp_request_folder) # Navegando para o diretório remoto
            lista_arquivos = ftp.listdir(ftp.curdir) # Obtendo a lista de arquivos no diretório remoto
            quantidade_arquivos = len(lista_arquivos) # Obtém a quantidade de arquivos na pasta

            if quantidade_arquivos == 0:
                print('A pasta está vazia.')

            else:
                print(f"Número de arquivos na pasta: {quantidade_arquivos}")
                cont = 0

                for arquivo in lista_arquivos: # Movendo os arquivos para a pasta local
                    caminho_local = os.path.join(receive_local_folder, arquivo)
                    ftp.download(arquivo, caminho_local)
                    ftp.remove(arquivo)
                    cont += 1
                print(f'Foram importados {cont} arquivos.')

    except Exception as e: # Exibi o erro na tela
        print(f"Ocorreu uma exceção processar os arquivos no FTP: {str(e)}")


def upload_file(): # Envia os retorno para o ftp

    ftp = connect()  # Establish FTP connection
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

            ftp.cwd(ftp_return_folder)

            for filename in os.listdir(upload_local_folder):
                if filename.endswith(".txt"):
                    local_path = os.path.join(upload_local_folder, filename)
                    remote_path = os.path.join(ftp_return_folder, filename)

                    with open(local_path, "rb") as file:
                        ftp.storbinary(f"STOR {remote_path}", file)

                    os.remove(local_path)
                    print(f"Arquivo '{filename}' enviado e removido localmente.")

                time.sleep(180)  # Delay of 3 minutes (180 seconds)

        messagebox.showinfo("CONCLUÍDO", "Todos os retornos foram enviados com sucesso!")

    except Exception as e:
        messagebox.showerror("ATENÇÃO", f"Ocorreu uma exceção: {str(e)}")




