import customtkinter as ctk
import sys
import io

def redirect_print(fild_print_receive, fild_print_return): # Recebe como parametros os dois textbox que serão utilizados como log
    def write_log_receive(text): # Escreve no log de pedido
        fild_print_receive.insert(ctk.END, text)
        fild_print_receive.see(ctk.END)

    def write_log_return(text): # Escreve no log de retorno
        fild_print_return.insert(ctk.END, text)
        fild_print_return.see(ctk.END)

    # Redirecionar a saída padrão para um buffer
    stdout_buffer = io.StringIO()
    sys.stdout = stdout_buffer

    log_console = stdout_buffer.getvalue() # Pega o valor escrito no console

    if "pedido" in log_console.lower(): # verifica se há pedido no texto
        write_log_receive(log_console)
    elif "retorno" in log_console.lower(): # verifica se há retorno no texto
        write_log_return(log_console)
    else: # Se não tiver nenhum ele vai levar como padrão o de pedido pois é mais extenso
        write_log_receive(log_console)

    sys.stdout = sys.__stdout__ # Restaura a saida padrão para o console