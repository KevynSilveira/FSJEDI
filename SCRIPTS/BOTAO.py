from SEPARA import separate_file
#import FTP

choice = ["Recebe", "Envia"]
status = False

def start():
    try:
        global choice, status
        status = True
        while status:
            print("rodando...")
            #FTP.run_ftp(choice[1])
            separate_file()
    except Exception as e:
        print(f"Ocorreu uma exceção: {str(e)}")

def stop():
    global status
    status = False
