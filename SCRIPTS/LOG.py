import sys
import customtkinter as ctk

class StdoutRedirector:
    def __init__(self, text_widget):
        self.text_widget = text_widget

    def write(self, text):
        self.text_widget.insert(ctk.END, text)
        self.text_widget.see(ctk.END)