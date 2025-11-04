# views/main_view.py
import tkinter as tk
from tkinter import ttk
from tkinter.constants import *
from .base_view import BaseView


class MainView(BaseView):
    """
    Vista principal (Dashboard) que se abre después del login.
    Contiene los botones para acceder a los 4 módulos mínimos[cite: 97].
    """

    def __init__(self, master, user_info):
        # Lógica para manejar el título
        sede_nombre = user_info.get('sede') or 'SuperAdmin'  # Si es None, usa 'SuperAdmin'

        super().__init__(master, title=f"WorkHub Dashboard - {sede_nombre}")
        self.geometry("1000x700")

        self.user_info = user_info

        # --- Barra de Menú ---
        self.menu_bar = tk.Menu(self)  # Cambiado a tk.Menu
        self.config(menu=self.menu_bar)

        # Menú Archivo
        self.file_menu = tk.Menu(self.menu_bar, tearoff=False)  # Cambiado a tk.Menu
        self.menu_bar.add_cascade(label="Archivo", menu=self.file_menu)
        self.file_menu.add_command(label="Cerrar Sesión")  # Se conectará en el controller
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Salir", command=self.on_close)

        # Se eliminó el menú de Opciones (Temas)

        # --- Frame Principal ---
        self.main_frame = ttk.Frame(self, padding=20)
        self.main_frame.pack(expand=True, fill=BOTH)

        header_label = f"Bienvenido, {self.user_info.get('nombre')} ({self.user_info.get('rol')})"
        # Eliminado bootstyle
        ttk.Label(self.main_frame, text=header_label, font=("Helvetica", 18, "bold")).pack(pady=10)

        # --- Contenedor de Botones de Módulos ---
        self.button_grid = ttk.Frame(self.main_frame)
        self.button_grid.pack(expand=True, fill=BOTH, pady=20)

        self.configure_grid(self.button_grid, 3)  # 3 columnas

        # --- Módulos "WorkHub" [cite: 6] (Mínimo 4) ---
        # Eliminados bootstyle y compound de todos los botones

        # 1. Módulo Miembros y Planes [cite: 7]
        self.btn_miembros = ttk.Button(self.button_grid, text="Gestión de Miembros")
        self.btn_miembros.grid(row=0, column=0, sticky=NSEW, padx=10, pady=10)

        # 2. Módulo Reserva de Espacios [cite: 11]
        self.btn_reservas = ttk.Button(self.button_grid, text="Reservas de Espacios")
        self.btn_reservas.grid(row=0, column=1, sticky=NSEW, padx=10, pady=10)

        # 3. Módulo Facturación y Pagos [cite: 16]
        self.btn_facturacion = ttk.Button(self.button_grid, text="Facturación y Pagos")
        self.btn_facturacion.grid(row=0, column=2, sticky=NSEW, padx=10, pady=10)

        # 4. Módulo Comunidad y Eventos [cite: 23]
        self.btn_comunidad = ttk.Button(self.button_grid, text="Comunidad y Eventos")
        self.btn_comunidad.grid(row=1, column=0, sticky=NSEW, padx=10, pady=10)

        # 5. Módulo Soporte e Incidentes [cite: 28]
        self.btn_soporte = ttk.Button(self.button_grid, text="Soporte e Incidentes")
        self.btn_soporte.grid(row=1, column=1, sticky=NSEW, padx=10, pady=10)

        # Módulo de Administración (Solo para SuperAdmin)
        self.btn_admin = ttk.Button(self.button_grid, text="Administración (Usuarios/Sedes)")
        if self.user_info.get('rol') == 'SuperAdmin':
            self.btn_admin.grid(row=1, column=2, sticky=NSEW, padx=10, pady=10)

    def configure_grid(self, container, cols):
        """Configura el grid para que los botones se expandan."""
        for i in range(cols):
            container.columnconfigure(i, weight=1)
        for i in range(2):  # Asumimos 2 filas de botones
            container.rowconfigure(i, weight=1)

    def on_close(self):
        # Al cerrar la ventana principal, se cierra la aplicación
        self.master.destroy()