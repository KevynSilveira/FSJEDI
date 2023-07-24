import customtkinter as ctk
import sys

def redirect_print(fild_print_receive, fild_print_return):
    def write_log_receive(text):
        fild_print_receive.insert(ctk.END, text)
        fild_print_receive.see(ctk.END)

    def write_log_return(text):
        fild_print_return.insert(ctk.END, text)
        fild_print_return.see(ctk.END)

    log_console = sys.stdout.write

    if "pedido" in log_console.lower():
        write_log_receive(log_console)
    elif "retorno" in log_console.lower():
        write_log_return(log_console)
    else:
        write_log_receive(log_console)