from SEPARA import separate_file
import threading
import time
import FTP

status = False
stop_processing = threading.Event()  # Usar um threading.Event para sinalizar parada

def start():
    global status
    if not status:
        status = True
        stop_processing.clear()  # Limpar o sinal para permitir a execução das threads
        upload_thread = threading.Thread(target=process_upload)
        download_thread = threading.Thread(target=process_download)
        upload_thread.start()
        download_thread.start()

def process_upload():
    try:
        while not stop_processing.is_set():  # Verificar o sinal para parar
            FTP.upload_file()

    except Exception as e:
        print("Upload error:", str(e))

    finally:
        time.sleep(180)

def process_download():
    try:
        while not stop_processing.is_set():  # Verificar o sinal para parar
            FTP.download_file()

        separate_file()  # Executar a separação após o download ser interrompido

    except Exception as e:
        print("Download error:", str(e))

    finally:
        time.sleep(180)

def stop():
    global status
    if status:
        status = False
        stop_processing.set()  # Definir o sinal para parar as threads


