# views/member_view.py
import tkinter as tk
from tkinter import ttk
from tkinter.constants import *
from .base_view import BaseView
from PIL import Image, ImageTk


# Formulario 1 con gestión de imágenes [cite: 85]
class MemberView(BaseView):
    def __init__(self, master, planes_list):
        super().__init__(master, title="Gestión de Miembros")
        self.geometry("900x700")

        main_frame = ttk.Frame(self, padding=10)
        main_frame.pack(expand=True, fill=BOTH)
        main_frame.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)  # Formulario
        main_frame.columnconfigure(1, weight=2)  # Lista

        # --- 1. Frame Formulario (Izquierda) ---
        form_labelframe = ttk.Labelframe(main_frame, text=" Formulario de Miembro ", padding=15)
        form_labelframe.grid(row=0, column=0, sticky=NSEW, padx=10, pady=10)

        ttk.Label(form_labelframe, text="Nombre Completo:").grid(row=0, column=0, sticky=W, pady=5)
        self.entry_nombre = ttk.Entry(form_labelframe, width=40)
        self.entry_nombre.grid(row=1, column=0, columnspan=2, sticky=EW, pady=5)

        ttk.Label(form_labelframe, text="Email:").grid(row=2, column=0, sticky=W, pady=5)
        self.entry_email = ttk.Entry(form_labelframe, width=40)
        self.entry_email.grid(row=3, column=0, columnspan=2, sticky=EW, pady=5)

        ttk.Label(form_labelframe, text="Teléfono:").grid(row=4, column=0, sticky=W, pady=5)
        self.entry_telefono = ttk.Entry(form_labelframe, width=40)
        self.entry_telefono.grid(row=5, column=0, columnspan=2, sticky=EW, pady=5)

        ttk.Label(form_labelframe, text="Plan:").grid(row=6, column=0, sticky=W, pady=5)
        self.combo_plan_options = {plan['nombre_plan']: plan['id_plan'] for plan in planes_list}
        self.combo_plan = ttk.Combobox(form_labelframe, state="readonly", values=list(self.combo_plan_options.keys()))
        self.combo_plan.grid(row=7, column=0, columnspan=2, sticky=EW, pady=5)

        ttk.Label(form_labelframe, text="Foto de Perfil:").grid(row=8, column=0, sticky=W, pady=5)
        # Eliminado bootstyle
        self.btn_cargar_imagen = ttk.Button(form_labelframe, text="Cargar Imagen")
        self.btn_cargar_imagen.grid(row=9, column=0, sticky=EW, pady=5, padx=(0, 5))

        # Eliminado bootstyle
        self.img_label_preview = ttk.Label(form_labelframe, text="Sin imagen")
        self.img_label_preview.grid(row=8, column=1, rowspan=2, sticky=W, padx=10)
        self.ruta_imagen_seleccionada = None
        self.photo_image = None

        btn_frame = ttk.Frame(form_labelframe)
        btn_frame.grid(row=10, column=0, columnspan=2, pady=20, sticky=EW)
        # Eliminados bootstyle
        self.btn_guardar = ttk.Button(btn_frame, text="Guardar")
        self.btn_guardar.pack(side=LEFT, expand=True, padx=5)
        self.btn_limpiar = ttk.Button(btn_frame, text="Limpiar")
        self.btn_limpiar.pack(side=LEFT, expand=True, padx=5)

        # --- 2. Frame Lista (Derecha) ---
        list_labelframe = ttk.Labelframe(main_frame, text=" Miembros Activos ", padding=15)
        list_labelframe.grid(row=0, column=1, sticky=NSEW, padx=10, pady=10)
        list_labelframe.rowconfigure(0, weight=1)
        list_labelframe.columnconfigure(0, weight=1)

        self.tree = ttk.Treeview(list_labelframe, columns=("ID", "Nombre", "Email", "Plan", "Estado"), show="headings",
                                 height=15)
        self.tree.grid(row=0, column=0, columnspan=2, sticky=NSEW)

        self.tree.heading("ID", text="ID")
        self.tree.heading("Nombre", text="Nombre")
        self.tree.heading("Email", text="Email")
        self.tree.heading("Plan", text="Plan")
        self.tree.heading("Estado", text="Estado")

        self.tree.column("ID", width=50, anchor=CENTER)
        self.tree.column("Nombre", width=200)
        self.tree.column("Email", width=200)
        self.tree.column("Plan", width=100)
        self.tree.column("Estado", width=80, anchor=CENTER)

        scrollbar = ttk.Scrollbar(list_labelframe, orient=VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.grid(row=0, column=2, sticky=NS)

        # Eliminado bootstyle
        self.btn_eliminar = ttk.Button(list_labelframe, text="Eliminar Seleccionado")
        self.btn_eliminar.grid(row=1, column=0, sticky=E, pady=10, padx=5)

    def set_preview_image(self, ruta_imagen):
        try:
            img = Image.open(ruta_imagen)
            img.thumbnail((100, 100), Image.LANCZOS)
            self.photo_image = ImageTk.PhotoImage(img)
            self.img_label_preview.config(image=self.photo_image, text="")
        except Exception as e:
            self.img_label_preview.config(image=None, text="Error img")
            print(f"Error al cargar preview: {e}")

    def limpiar_formulario(self):
        self.entry_nombre.delete(0, END)
        self.entry_email.delete(0, END)
        self.entry_telefono.delete(0, END)
        self.combo_plan.set("")
        self.img_label_preview.config(image=None, text="Sin imagen")
        self.photo_image = None
        self.ruta_imagen_seleccionada = None
        self.tree.selection_remove(self.tree.selection())

    def popular_tabla(self, miembros):
        for item in self.tree.get_children():
            self.tree.delete(item)

        for miembro in miembros:
            self.tree.insert("", END, iid=miembro['id_miembro'],
                             values=(miembro['id_miembro'],
                                     miembro['nombre_completo'],
                                     miembro['email'],
                                     miembro['nombre_plan'],
                                     miembro['estado']))

    def obtener_datos_formulario(self):
        return {
            "nombre": self.entry_nombre.get(),
            "email": self.entry_email.get(),
            "telefono": self.entry_telefono.get(),
            "id_plan": self.combo_plan_options.get(self.combo_plan.get()),
            "foto_path": self.ruta_imagen_seleccionada
        }

    def obtener_id_seleccionado(self):
        try:
            return self.tree.selection()[0]
        except IndexError:
            return None