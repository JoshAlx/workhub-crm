# views/login_view.py
import tkinter as tk
from tkinter import ttk
from tkinter.constants import *  # Importamos constantes estándar


# Se eliminó la importación de CURRENT_THEME

class LoginView(tk.Tk):  # Cambiado a tk.Tk
    """
    Ventana de Login. Es la ventana principal (tk.Tk).
    """

    def __init__(self):
        super().__init__()  # Eliminado themename

        self.title("WorkHub - Inicio de Sesión")
        self.geometry("400x450")

        try:
            self.iconbitmap("assets/favicon.ico")[cite: 87]
        except Exception as e:
            print(f"Advertencia: No se pudo cargar 'assets/favicon.ico'. {e}")

        self.center_window()

        # Frame principal
        self.main_frame = ttk.Frame(self, padding=(40, 20))
        self.main_frame.pack(expand=True, fill=BOTH)

        # Eliminado bootstyle
        ttk.Label(self.main_frame, text="WorkHub", font=("Helvetica", 24, "bold"), foreground="blue").pack(
            pady=(10, 20))

        # Formulario de Login
        form_frame = ttk.Frame(self.main_frame)
        form_frame.pack(pady=20)

        ttk.Label(form_frame, text="Email:", font=("Helvetica", 12)).grid(row=0, column=0, sticky=W, pady=5)
        self.email_entry = ttk.Entry(form_frame, width=30, font=("Helvetica", 12))
        self.email_entry.grid(row=1, column=0, pady=5, padx=5)

        ttk.Label(form_frame, text="Contraseña:", font=("Helvetica", 12)).grid(row=2, column=0, sticky=W, pady=5)
        self.password_entry = ttk.Entry(form_frame, width=30, font=("Helvetica", 12), show="*")
        self.password_entry.grid(row=3, column=0, pady=5, padx=5)

        # Eliminado bootstyle
        self.login_button = ttk.Button(self.main_frame, text="Ingresar", width=20)
        self.login_button.pack(pady=20)

        # Eliminado bootstyle, usamos foreground="red" para errores
        self.message_label = ttk.Label(self.main_frame, text="", font=("Helvetica", 10), foreground="red")
        self.message_label.pack(pady=(10, 0))

        # Bind Enter key
        self.email_entry.bind("<Return>", lambda e: self.password_entry.focus())
        self.password_entry.bind("<Return>", lambda e: self.login_button.invoke())

    def center_window(self):
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'{width}x{height}+{x}+{y}')

    def show_error(self, message):
        self.message_label.config(text=message, foreground="red")  # Aseguramos color

    def clear_error(self):
        self.message_label.config(text="", foreground="red")  # Ocultamos texto

    def hide(self):
        """Oculta la ventana."""
        self.withdraw()

    def show(self):
        """Muestra la ventana."""
        self.deiconify()

    def close(self):
        """Destruye la ventana (se usará al salir)."""
        self.destroy()