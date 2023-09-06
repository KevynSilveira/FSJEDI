import customtkinter as ctk # precisa do comando (pip install customtkinter)
from FORMATA_HR import format_time
from BOTAO import start
from BOTAO import stop
from LOG import StdoutRedirector
import sys

tempo = 0

def create_frame_main(): # Criando frame principal

    global tempo

    frame_main = ctk.CTk()
    frame_main.geometry("480x225") # Defini a largura e altura do frame respectivamente
    frame_main.title("FSJEDI")
    frame_main.resizable(False, False) # Tira a opção de maximizar

    ctk.set_appearance_mode("Dark")

    l_title = ctk.CTkLabel(master=frame_main, text="Processamento FSJEDI", width=200)
    l_title.configure(font=("arial", 20))
    l_title.place(x=115, y=10)

    # Criando botões de execução (start, pause, log)
    b_start = ctk.CTkButton(master=frame_main, width=100, height=70, text="Iniciar", corner_radius=4, command=start,
                            fg_color="dark grey", text_color="black", hover_color="gray")
    b_start.configure(font=("arial", 14))
    b_start.place(x=5, y=55)

    b_stop = ctk.CTkButton(master=frame_main, width=100, height=70, text="Pausar", corner_radius=4, command=stop,
                           fg_color="dark grey", text_color="black", hover_color="gray")
    b_stop.configure(font=("arial", 14))
    b_stop.place(x=5, y=130)

    log = ctk.CTkTextbox(master=frame_main, width=350, height=145)
    log.configure(font=("arial", 12))
    log.place(x=120, y=55)

    l_runtime = ctk.CTkLabel(master=frame_main, text=f": {tempo}", width=100)
    l_runtime.place(x=165, y=200)

    sys.stdout = StdoutRedirector(log) # Log com todos os print do código.

    def update_time(): # Atualiza o tempo a cada 1 segundo
        global tempo
        nonlocal l_runtime
        tempo += 1
        formatted_time = format_time(tempo)
        l_runtime.configure(text=f"Iniciou há: {formatted_time}")
        frame_main.after(1000, update_time)

    update_time()
    frame_main.mainloop()

if __name__ == "__main__":
    create_frame_main()
