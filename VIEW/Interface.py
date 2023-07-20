# Criação da interface

# Adicionando imports
import customtkinter as ctk # precisa do comando (pip install customtkinter)

def create_frame_main(): # Criando frame principal

    frame_main = ctk.CTk()
    frame_main.geometry("700x400") # Defini a largura e altura do frame respectivamente
    frame_main.title("FSJEDI")
    frame_main.resizable(False, False)

    frame_main.mainloop()





if __name__ == "__main__":
    create_frame_main()