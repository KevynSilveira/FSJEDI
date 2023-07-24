# Criação da interface

# Adicionando imports
import customtkinter as ctk # precisa do comando (pip install customtkinter)
from FUNCTIONS.REDIRECIONA import redirect_print
import datetime
from FUNCTIONS.FORMATA_HR import format_time

tempo = 0

def teste():
    print("retorno")

def create_frame_main(): # Criando frame principal

    global tempo

    frame_main = ctk.CTk()
    frame_main.geometry("500x300") # Defini a largura e altura do frame respectivamente
    frame_main.title("FSJEDI")
    frame_main.resizable(False, False) # Tira a opção de maximizar

    # Criando botões de execução (start, pause, log)
    b_start = ctk.CTkButton(master=frame_main, width=100, height=30, text="Iniciar", corner_radius=4)
    b_start.place(x=85, y=10)

    b_pause = ctk.CTkButton(master=frame_main, width=100, height=30, text="Pausar", corner_radius=4)
    b_pause.place(x=195, y=10)

    log = ["Log pedido", "Log retorno"] # Lista de texto para o botão
    b_log = ctk.CTkButton(master=frame_main, width=100, height=30, text=log[1], corner_radius=4)
    b_log.place(x=305, y=10)

    log = ["Log pedido", "Log retorno"] # Lista de texto para o botão
    b_log = ctk.CTkButton(master=frame_main, width=100, height=30 ,text=log[1], corner_radius=4, command=teste)
    b_log.place(x=305, y=10)

    # Frame log
    f_log_request = ctk.CTkTextbox(master=frame_main, width=235 , height=200)
    f_log_request.place(x=10, y=75)
    #f_log_request.insert(ctk.END, "Pedido")
    f_log_request.bind("<Key>", lambda e: "break")

    f_log_return = ctk.CTkTextbox(master=frame_main, width=235 , height=200)
    f_log_return.place(x=255, y=75)
    #f_log_return.insert(ctk.END, "Retorno")
    f_log_return.bind("<Key>", lambda e: "break")

    redirect_print(f_log_request, f_log_return)

    l_runtime = ctk.CTkLabel(master=frame_main, text=f"Tempo em execução: {tempo}", width=100)
    l_runtime.place(x=180, y=275)

    def update_time(): # Atualiza o tempo a cada 1 segundo
        global tempo
        nonlocal l_runtime
        tempo += 1
        formatted_time = format_time(tempo)
        l_runtime.configure(text=f"Tempo em execução: {formatted_time}")
        frame_main.after(1000, update_time)

    l_pedido = ctk.CTkLabel(master=frame_main, text="LOG PEDIDO", width=100)
    l_pedido.place(x=77, y=45)

    l_retono = ctk.CTkLabel(master=frame_main, text="LOG RETORNO", width=100)
    l_retono.place(x=330, y=45)

    update_time()
    frame_main.mainloop()


if __name__ == "__main__":
    create_frame_main()
