import os
from ftputil import FTPHost

hostname = ''
username = ''
password = ''
ftp_envio = '/Envio/'
pasta_local = r'C:\FSJEDI\Processamento'

def conectar_ftp_baixar_arquivos():
    try:
        # Conectando ao servidor FTP
        with FTPHost(hostname, username, password) as ftp:
            print('Conectou no FTP.\n')

            # Navegando para o diretório remoto
            ftp.chdir(ftp_envio)

            # Obtendo a lista de arquivos no diretório remoto
            lista_arquivos = ftp.listdir(ftp.curdir)

            # Obtém a quantidade de arquivos na pasta
            quantidade_arquivos = len(lista_arquivos)

            if quantidade_arquivos == 0:
                print('A pasta está vazia\n')
            else:
                try:
                    print(f"Número de arquivos na pasta: {quantidade_arquivos}\n")
                    cont = 0
                    # Movendo os arquivos para a pasta local
                    for arquivo in lista_arquivos:
                        caminho_local = os.path.join(pasta_local, arquivo)
                        ftp.download(arquivo, caminho_local)
                        ftp.remove(arquivo)
                        cont += 1

                    print(f'Foram importados {cont} arquivos.\n')
                except Exception as e:
                    print(f"Ocorreu uma exceção: {str(e)}")

    except Exception as e:
        print(f"Ocorreu uma exceção: {str(e)}")

#conectar_ftp_baixar_arquivos()
