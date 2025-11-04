# views/admin_view.py
import tkinter as tk
from tkinter import ttk
from tkinter.constants import *
from .base_view import BaseView


class AdminView(BaseView):
    """
    Vista especial para el SuperAdmin.
    Gestiona Sedes y Usuarios.
    """

    def __init__(self, master, sedes_list):
        super().__init__(master, title="Administración del Sistema (SuperAdmin)")
        self.geometry("900x600")

        self.sedes_options = {s['nombre_sede']: s['id_sede'] for s in sedes_list}

        notebook = ttk.Notebook(self)
        notebook.pack(expand=True, fill=BOTH, padx=10, pady=10)

        # --- Pestaña 1: Gestión de Usuarios ---
        user_frame = ttk.Frame(notebook, padding=10)
        notebook.add(user_frame, text="Gestión de Usuarios")

        form_user = ttk.Labelframe(user_frame, text="Nuevo Usuario (Admin/Coordinador)", padding=15)
        form_user.pack(fill=X, padx=10, pady=10)

        ttk.Label(form_user, text="Nombre:").grid(row=0, column=0, padx=5, pady=5, sticky=W)
        self.user_nombre = ttk.Entry(form_user, width=30)
        self.user_nombre.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(form_user, text="Email:").grid(row=1, column=0, padx=5, pady=5, sticky=W)
        self.user_email = ttk.Entry(form_user, width=30)
        self.user_email.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(form_user, text="Password:").grid(row=0, column=2, padx=5, pady=5, sticky=W)
        self.user_pass = ttk.Entry(form_user, width=30, show="*")
        self.user_pass.grid(row=0, column=3, padx=5, pady=5)

        ttk.Label(form_user, text="Rol:").grid(row=2, column=0, padx=5, pady=5, sticky=W)
        self.user_rol = ttk.Combobox(form_user, state="readonly", values=['Admin', 'Coordinador'])
        self.user_rol.grid(row=2, column=1, padx=5, pady=5, sticky=EW)

        ttk.Label(form_user, text="Sede:").grid(row=2, column=2, padx=5, pady=5, sticky=W)
        self.user_sede = ttk.Combobox(form_user, state="readonly", values=list(self.sedes_options.keys()))
        self.user_sede.grid(row=2, column=3, padx=5, pady=5, sticky=EW)

        # Eliminado bootstyle
        self.btn_guardar_usuario = ttk.Button(form_user, text="Crear Usuario")
        self.btn_guardar_usuario.grid(row=3, column=3, padx=5, pady=10, sticky=E)

        # --- Pestaña 2: Gestión de Sedes ---
        sede_frame = ttk.Frame(notebook, padding=10)
        notebook.add(sede_frame, text="Gestión de Sedes")

        form_sede = ttk.Labelframe(sede_frame, text="Nueva Sede", padding=15)
        form_sede.pack(fill=X, padx=10, pady=10)

        ttk.Label(form_sede, text="Nombre Sede:").grid(row=0, column=0, padx=5, pady=5, sticky=W)
        self.sede_nombre = ttk.Entry(form_sede, width=30)
        self.sede_nombre.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(form_sede, text="Dirección:").grid(row=1, column=0, padx=5, pady=5, sticky=W)
        self.sede_dir = ttk.Entry(form_sede, width=30)
        self.sede_dir.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(form_sede, text="Teléfono:").grid(row=2, column=0, padx=5, pady=5, sticky=W)
        self.sede_tel = ttk.Entry(form_sede, width=30)
        self.sede_tel.grid(row=2, column=1, padx=5, pady=5)

        # Eliminado bootstyle
        self.btn_guardar_sede = ttk.Button(form_sede, text="Crear Sede")
        self.btn_guardar_sede.grid(row=3, column=1, padx=5, pady=10, sticky=E)