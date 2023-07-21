import os
from ftputil import FTPHost

hostname = ''
username = ''
password = ''
ftp_envio = '/Envio/'
pasta_local = r'C:\FSJEDI\Processamento'

def connect(): # Faz a conexão com o FTP
    try:
        # Conectando ao servidor FTP
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

def download_file(ftp): # Baixa os arquivos do FTP e recebe como parâmetro a conexão
    try:
        if ftp is not None:

            ftp.chdir(ftp_envio) # Navegando para o diretório remoto
            lista_arquivos = ftp.listdir(ftp.curdir) # Obtendo a lista de arquivos no diretório remoto
            quantidade_arquivos = len(lista_arquivos) # Obtém a quantidade de arquivos na pasta

            if quantidade_arquivos == 0: # Se os
                print('A pasta está vazia.')
            else:
                print(f"Número de arquivos na pasta: {quantidade_arquivos}")
                cont = 0
                # Movendo os arquivos para a pasta local
                for arquivo in lista_arquivos:
                    caminho_local = os.path.join(pasta_local, arquivo)
                    ftp.download(arquivo, caminho_local)
                    ftp.remove(arquivo)
                    cont += 1
                print(f'Foram importados {cont} arquivos.')
    except Exception as e: # Exibi o erro na tela
        print(f"Ocorreu uma exceção processar os arquivos no FTP: {str(e)}")


def run_ftp(): # Executa todos os métodos
    ftp = connect() # Conecta ao FTP

    if ftp is not None:
        download_file(ftp) # Realiza as operações de baixar e deletar arquivos
        close_connection(ftp) # Fecha a conexão ao final das operações
    else:
        print("Conexão com FTP falhou!")


