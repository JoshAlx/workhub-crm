# views/base_view.py
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox  # Importamos el messagebox estándar


class BaseView(tk.Toplevel):  # Cambiado a tk.Toplevel
    """
    Clase base para todas las ventanas (formularios) de la aplicación.
    Asegura consistencia: Favicon, título y tema.
    """

    def __init__(self, master=None, title="WorkHub"):
        super().__init__(master)
        self.title(title)
        self.geometry("800x600")

        # Requisito: Favicon personalizado [cite: 87]
        try:
            self.iconbitmap("assets/favicon.ico")
        except Exception as e:
            print(f"Advertencia: No se pudo cargar 'assets/favicon.ico'. {e}")

        # Se eliminó la lógica de self.style_manager

        # Esto llama directamente a 'destroy' cuando se presiona la 'X'
        self.protocol("WM_DELETE_WINDOW", self.destroy)

        self.withdraw()  # Ocultar la ventana hasta que esté lista
        self.center_window()
        self.deiconify()  # Mostrar ventana centrada

    def center_window(self):
        """Centra la ventana en la pantalla."""
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'{width}x{height}+{x}+{y}')

    def show_message(self, title, message, alert_type="info"):
        """Muestra un diálogo de mensaje."""
        if alert_type == "error":
            messagebox.showerror(title, message, parent=self)
        elif alert_type == "warning":
            messagebox.showwarning(title, message, parent=self)
        else:
            messagebox.showinfo(title, message, parent=self)

    def ask_confirmation(self, title, message):
        """Requisito: Diálogo de confirmación[cite: 83]."""
        # askyesno devuelve True o False directamente
        return messagebox.askyesno(title, message, parent=self)