from SEPARA import separate_file as separa
import FTP as ftp

choice = ["Recebe", "Envia"]
status = False
def start():
    try:
        global choice, status
        status = True
        while status:
            ftp.run_ftp(choice[1])
            separa()
    except Exception as e:
        print(f"Ocorreu uma exceção: {str(e)}")

def stop():
    global status
    status = False