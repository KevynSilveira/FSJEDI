import customtkinter as ctk # precisa do comando (pip install customtkinter)
from FORMATA_HR import format_time
from BOTAO import start
from BOTAO import stop

tempo = 0

def create_frame_main(): # Criando frame principal

    global tempo

    frame_main = ctk.CTk()
    frame_main.geometry("200x140") # Defini a largura e altura do frame respectivamente
    frame_main.title("FSJEDI")
    frame_main.resizable(False, False) # Tira a opção de maximizar

    # Criando botões de execução (start, pause, log)
    b_start = ctk.CTkButton(master=frame_main, width=100, height=30, text="Iniciar", corner_radius=4, command=start)
    b_start.place(x=50, y=10)

    b_stop = ctk.CTkButton(master=frame_main, width=100, height=30, text="Pausar", corner_radius=4, command=stop)
    b_stop.place(x=50, y=50)

    l_runtime = ctk.CTkLabel(master=frame_main, text=f"Tempo em execução: {tempo}", width=100)
    l_runtime.place(x=5, y=100)

    def update_time(): # Atualiza o tempo a cada 1 segundo
        global tempo
        nonlocal l_runtime
        tempo += 1
        formatted_time = format_time(tempo)
        l_runtime.configure(text=f"Tempo em execução: {formatted_time}")
        frame_main.after(1000, update_time)

    update_time()
    frame_main.mainloop()

if __name__ == "__main__":
    create_frame_main()
