from SEPARA import separate_file
import threading
import time
import FTP

choice = ["Recebe", "Envia"]
status = False
stop_processing = True

def start():
    try:
        global choice, status, stop_processing

        status = True
        stop_processing = False

        upload_thread = threading.Thread(target=process_upload)
        download_thread = threading.Thread(target=process_download)

        upload_thread.start()
        download_thread.start()

        upload_thread.join()
        download_thread.join()

        separate_file()  # Separate file operations after both upload and download are done

    except Exception as e:
        # Handle exceptions
        print("An error occurred:", str(e))

def process_upload():
    try:
        while status:
            if stop_processing:
                break
            FTP.upload_file()
            time.sleep(180)  # Add delay between upload iterations

    except Exception as e:
        print("Upload error:", str(e))

def process_download():
    try:
        while status:
            if stop_processing:
                break
            FTP.download_file()
            separate_file()  # Call separate_file() after each download operation

    except Exception as e:
        print("Download error:", str(e))

def stop():

    global status, stop_processing
    status = False
    stop_processing = True
