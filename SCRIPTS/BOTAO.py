from SEPARA import separate_file
#import FTP

choice = ["Recebe", "Envia"]
status = False
stop_processing = True

def start():
    try:
        global choice, status, stop_processing
        status = True
        stop_processing = False
        while status:
            print("rodando...")
            #FTP.run_ftp(choice[1])
            separate_file()
    except Exception as e:
        print(f"Ocorreu uma exceção: {str(e)}")

def stop():
    global status, stop_processing
    status = False
    stop_processing = True
