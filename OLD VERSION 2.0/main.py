import tkinter as tk
from tkinter import messagebox
import time
import datetime
from threading import Thread
import sys

# Importe os módulos necessários
from processamento_pedido import processamento_pedidos
from separacao_pedidos import acessar_db, fechar_db
#from busca_arquivo_ftp import conectar_ftp_baixar_arquivos

ultimo_horario_execucao = None
executando_processamento = False
lbl_status = None
conexao_bd = False

def iniciar_processamento():
    global ultimo_horario_execucao, executando_processamento, conexao_bd

    if executando_processamento:
        return

    executando_processamento = True
    atualizar_label_status("Executando")

    #verifica se já executando.
    if conexao_bd is False:

        # Fazer a conexão com o banco de dados
        acessar_db()
        conexao_bd = True

    # Iniciar um while True com tempo de retorno a importação a cada 5 minutos
    while executando_processamento:
        # Conecta no FTP da FSJEDI
        #conectar_ftp_baixar_arquivos()

        # Processamento dos pedidos
        processamento_pedidos()

        # Obter a hora atual
        hora_atual = datetime.datetime.now().time()  # Obter o horário atual como um objeto datetime.time

        #atualiza o horário da ultima execução
        ultimo_horario_execucao = hora_atual

        #Modela o parâmetro de hora
        ultimo_horario_execucao= datetime.datetime.now().strftime("%H:%M:%S")

        # Imprime o horário de conclusão
        print(f"Horário de conclusão: {ultimo_horario_execucao}\n\n")

        # Aguardar 5 minutos antes de iniciar o próximo ciclo
        time.sleep(300)

    executando_processamento = False
    atualizar_label_status("Parado")

def verificar_periodo_processamento():
    #Esse método verifica se o tempo de execução é maior que 6 minutos, caso seja ele ira parar o processamento e iniciar novamente.
    global ultimo_horario_execucao, executando_processamento

    if not executando_processamento:
        return

    hora_atual = datetime.datetime.now().time()

    if ultimo_horario_execucao is not None:
        if isinstance(ultimo_horario_execucao, str):
            ultimo_horario_execucao = datetime.datetime.strptime(ultimo_horario_execucao, "%H:%M:%S").time()

        diferenca_tempo = (datetime.datetime.combine(datetime.datetime.today(), hora_atual) - datetime.datetime.combine(datetime.datetime.today(), ultimo_horario_execucao)).total_seconds()
        if diferenca_tempo >= 360:
            print("Reiniciando processamento")
            parar_processamento()
            iniciar_processamento_thread()

    else:
        ultimo_horario_execucao = hora_atual



def parar_processamento():
    global executando_processamento, ultimo_horario_execucao, conexao_bd
    executando_processamento = False
    ultimo_horario_execucao = None
    conexao_bd = False
    fechar_db()
    atualizar_label_status("Parado")

def fechar_aplicacao(root):
    if messagebox.askokcancel("Fechar", "Deseja fechar a aplicação?"):
        root.quit()
        root.destroy()
        sys.exit()

def iniciar_processamento_thread():
    thread = Thread(target=iniciar_processamento)
    thread.start()

def monitorar_processamento_thread():
    thread = Thread(target=monitorar_processamento)
    thread.start()

def monitorar_processamento():
    while True:
        verificar_periodo_processamento()
        time.sleep(360)  # Aguardar 6 minutos antes de verificar novamente

def create_gui(root):
    global lbl_status

    verificar_periodo_processamento()  # Verificar o período de processamento

    root.title("Processamento FSJEDI")
    root.geometry("600x300")
    root.resizable(0, 0)  # Impede o redimensionamento da janela

    # Estilos dos botões e labels
    button_style = {"width": 12, "height": 2, "font": ("Helvetica", 12), "bg": "#C0C0C0", "fg": "black", "highlightbackground": "#f8f9fa"}
    btn_iniciar_style = {**button_style, "bg": "#C0C0C0", "fg": "black", "highlightbackground": "#f8f9fa"}
    btn_parar_style = {**button_style, "bg": "#C0C0C0", "fg": "black", "highlightbackground": "#f8f9fa"}
    btn_fechar_style = {**button_style, "bg": "#C0C0C0", "fg": "black", "highlightbackground": "#f8f9fa"}
    label_style = {"font": ("Helvetica", 12, "bold"), "pady": 10, "bg": "#f8f9fa", "fg": "black", "highlightbackground": "#f8f9fa"}

    # Frame principal
    frame = tk.Frame(root, bg="#f8f9fa")
    frame.grid(row=0, column=0, padx=20, pady=25, sticky=tk.W)

    # Botões
    btn_iniciar = tk.Button(frame, text="Iniciar", command=iniciar_processamento_thread, **btn_iniciar_style)
    btn_iniciar.grid(row=0, column=0, padx=10, pady=5)

    btn_parar = tk.Button(frame, text="Parar", command=parar_processamento, **btn_parar_style)
    btn_parar.grid(row=1, column=0, padx=10, pady=5)

    btn_fechar = tk.Button(frame, text="Fechar", command=lambda: fechar_aplicacao(root), **btn_fechar_style)
    btn_fechar.grid(row=2, column=0, padx=10, pady=5)

    # Frame do log
    log_frame = tk.Frame(root, bg="#343a40")
    log_frame.grid(row=0, column=1, padx=12, pady=20, sticky=tk.NW)

    # Log
    log_text = tk.Text(log_frame, height=11.5, width=47, bg="#343a40", fg="white")
    log_text.grid(row=1, column=0)

    # Barra de rolagem vertical
    scrollbar = tk.Scrollbar(log_frame, command=log_text.yview)
    scrollbar.grid(row=1, column=1, sticky='nsew')

    # Configurar a barra de rolagem para o widget Text
    log_text.configure(yscrollcommand=scrollbar.set)

    # Label do título
    lbl_titulo = tk.Label(log_frame, text="Processamento FSJEDI", font=("Helvetica", 16, "bold"))
    lbl_titulo.grid(row=0, column=0, sticky="nsew")

    # Label de status
    lbl_status = tk.Label(root, text="Status: Parado", **label_style)
    lbl_status.grid(row=1, column=0, padx=5, pady=5, sticky=tk.SW)

    # Função para redirecionar o print para o log
    def redirecionar_print(text_widget):
        def escrever_no_log(text):
            text_widget.insert(tk.END, text)
            text_widget.see(tk.END)

        sys.stdout.write = escrever_no_log

    redirecionar_print(log_text)

    # Função para atualizar o tempo de execução
    def atualizar_tempo_execucao():
        tempo = datetime.datetime.now() - inicio_execucao
        dias = tempo.days
        horas, resto = divmod(tempo.seconds, 3600)
        minutos, segundos = divmod(resto, 60)

        tempo_formatado = f"Tempo de execução: {dias:02d}:{horas:02d}:{minutos:02d}:{segundos:02d}"
        lbl_tempo_execucao.config(text=tempo_formatado)
        lbl_tempo_execucao.after(1000, atualizar_tempo_execucao)

    inicio_execucao = datetime.datetime.now()

    # Label de tempo de execução
    lbl_tempo_execucao = tk.Label(root, **label_style)
    lbl_tempo_execucao.grid(row=1, column=1, pady=5)
    atualizar_tempo_execucao()

    monitorar_processamento_thread()  # Iniciar a monitoração do processamento

def atualizar_label_status(status):
    if lbl_status:
        lbl_status.config(text="Status: " + status)

root = tk.Tk()
create_gui(root)
root.protocol("WM_DELETE_WINDOW", lambda: fechar_aplicacao(root))
root.mainloop()
