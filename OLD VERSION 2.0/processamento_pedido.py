import os
import configparser
import shutil


from separacao_pedidos import comparar_db

def processamento_pedidos():
    try:
        # Lê as configurações do arquivo config.ini
        config = configparser.ConfigParser()
        config.read('config.ini')

        # Obtém os diretórios de origem, destino RS e SC do arquivo config.ini
        diretorio_origem = "C:\FSJEDI\Processamento"
        diretorio_destino_rs = "D:\MEDMAIS\São João\RS\Envio"
        diretorio_destino_sc = "D:\MEDMAIS\São João\SC\Envio"

        # Obtém o CNPJ RS e CNPJ SC do arquivo config.ini
        cnpj_sc = config.get('CNPJs', 'cnpj_sc')
        cnpj_rs = config.get('CNPJs', 'cnpj_rs')

        # Obtém a lista de arquivos no diretório de origem
        arquivos = os.listdir(diretorio_origem)

        # Inicializa o contador de arquivos processados
        total_arquivos_processados = 0

        # Itera sobre os arquivos no diretório de origem
        for arquivo in arquivos:

            # Verifica se o arquivo é um arquivo TXT
            if arquivo.endswith('.txt'):

                # Cria o caminho completo do arquivo txt
                caminho_arquivo = os.path.join(diretorio_origem, arquivo)

                # Verifica se o arquivo já existe no diretório de destino RS
                if os.path.exists(os.path.join(diretorio_destino_rs, arquivo)):
                    # Remove o arquivo da pasta de origem
                    os.remove(caminho_arquivo)
                    continue  # Pula para o próximo arquivo

                with open(caminho_arquivo, 'r') as arquivo_txt:
                    # Pega o CNPJ do cliente do arquivo de pedido
                    cnpj_cliente = arquivo_txt.readline()
                    cnpj = cnpj_cliente[1:15]

                # Chama a função comparar_db do separacao_pedidos.py
                resultado = comparar_db(cnpj)

                # Cria o caminho de destino do arquivo corrigido
                caminho_destino_rs = os.path.join(diretorio_destino_rs, arquivo)
                caminho_destino_sc = os.path.join(diretorio_destino_sc, arquivo)

                if resultado == "RS":
                    # Abre o arquivo temporário para leitura
                    with open(caminho_arquivo, 'r') as arquivo_origem:
                        conteudo = arquivo_origem.read()

                    # Substitui o número antigo pelo número novo
                    correcao_cnpj = conteudo.replace(cnpj_sc, cnpj_rs)

                    # Cria o caminho do arquivo para envio dos arquivos do RS editados
                    caminho_arquivo_destino = os.path.join(diretorio_destino_rs, arquivo)

                    # Abre o arquivo temporário para escrita
                    with open(caminho_arquivo, 'w') as arquivo_destino:
                        arquivo_destino.write(correcao_cnpj)

                    # Move o arquivo diretamente para o diretório de destino RS
                    shutil.move(caminho_arquivo, caminho_arquivo_destino)

                elif resultado == "SC":
                    # Move o arquivo diretamente para o diretório de destino SC
                    shutil.move(caminho_arquivo, caminho_destino_sc)

                else:
                    # Move o arquivo diretamente para o diretório de destino RS
                    shutil.move(caminho_arquivo, caminho_destino_rs)

                # Incrementa o contador de arquivos processados
                total_arquivos_processados += 1

                # Imprime o nome do arquivo processado
                print(f"Arquivo processado: {arquivo}")

        # Imprime o total de arquivos processados
        print(f"Total de arquivos processados: {total_arquivos_processados}\n")

    # Trata quando o arquivo não é encontrado
    except FileNotFoundError:
        print("O arquivo não foi encontrado.")

    # Trata quando não consegue achar o arquivo config.ini ou não consegue achar os parâmetros no arquivo
    except configparser.Error:
        print("Erro ao ler o arquivo de configuração.")
