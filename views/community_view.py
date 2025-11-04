# views/community_view.py
import tkinter as tk
from tkinter import ttk
from tkinter.constants import *
from .base_view import BaseView
from tkcalendar import DateEntry
from PIL import Image, ImageTk


# Formulario 2 con gestión de imágenes [cite: 85]
class CommunityView(BaseView):
    def __init__(self, master):
        super().__init__(master, title="Gestión de Comunidad y Eventos")
        self.geometry("900x600")

        main_frame = ttk.Frame(self, padding=10)
        main_frame.pack(expand=True, fill=BOTH)
        main_frame.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)  # Formulario
        main_frame.columnconfigure(1, weight=2)  # Lista

        # --- 1. Frame Formulario (Izquierda) ---
        form_labelframe = ttk.Labelframe(main_frame, text=" Nuevo Evento ", padding=15)
        form_labelframe.grid(row=0, column=0, sticky=NSEW, padx=10, pady=10)

        ttk.Label(form_labelframe, text="Título del Evento:").grid(row=0, column=0, sticky=W, pady=5)
        self.entry_titulo = ttk.Entry(form_labelframe, width=40)
        self.entry_titulo.grid(row=1, column=0, columnspan=2, sticky=EW, pady=5)

        ttk.Label(form_labelframe, text="Descripción:").grid(row=2, column=0, sticky=W, pady=5)
        self.text_desc = tk.Text(form_labelframe, width=40, height=5)  # Usamos tk.Text
        self.text_desc.grid(row=3, column=0, columnspan=2, sticky=EW, pady=5)

        # Eliminados bootstyle, style y el parche _determine_downarrow
        ttk.Label(form_labelframe, text="Fecha Evento:").grid(row=4, column=0, sticky=W, pady=5)
        self.entry_fecha = DateEntry(form_labelframe, width=18, date_pattern='yyyy-mm-dd', locale='es_ES')
        self.entry_fecha.grid(row=5, column=0, sticky=W, pady=5)

        ttk.Label(form_labelframe, text="Lugar:").grid(row=6, column=0, sticky=W, pady=5)
        self.entry_lugar = ttk.Entry(form_labelframe, width=40)
        self.entry_lugar.grid(row=7, column=0, columnspan=2, sticky=EW, pady=5)

        # Eliminado bootstyle
        ttk.Label(form_labelframe, text="Imagen del Evento (Flyer):").grid(row=8, column=0, sticky=W, pady=5)
        self.btn_cargar_imagen = ttk.Button(form_labelframe, text="Cargar Imagen")
        self.btn_cargar_imagen.grid(row=9, column=0, sticky=EW, pady=5, padx=(0, 5))

        # Eliminado bootstyle
        self.img_label_preview = ttk.Label(form_labelframe, text="Sin imagen")
        self.img_label_preview.grid(row=8, column=1, rowspan=2, sticky=W, padx=10)
        self.ruta_imagen_seleccionada = None
        self.photo_image = None

        # Eliminado bootstyle
        self.btn_guardar = ttk.Button(form_labelframe, text="Crear Evento")
        self.btn_guardar.grid(row=10, column=0, columnspan=2, pady=20, sticky=EW)

        # --- 2. Frame Lista (Derecha) ---
        list_labelframe = ttk.Labelframe(main_frame, text=" Próximos Eventos ", padding=15)
        list_labelframe.grid(row=0, column=1, sticky=NSEW, padx=10, pady=10)
        list_labelframe.rowconfigure(0, weight=1);
        list_labelframe.columnconfigure(0, weight=1)

        self.tree = ttk.Treeview(list_labelframe, columns=("ID", "Título", "Fecha", "Lugar"), show="headings")
        self.tree.grid(row=0, column=0, sticky=NSEW)
        self.tree.heading("ID", text="ID");
        self.tree.column("ID", width=40, anchor=CENTER)
        self.tree.heading("Título", text="Título");
        self.tree.column("Título", width=200)
        self.tree.heading("Fecha", text="Fecha");
        self.tree.column("Fecha", width=120)
        self.tree.heading("Lugar", text="Lugar");
        self.tree.column("Lugar", width=150)

    def set_preview_image(self, ruta_imagen):
        try:
            img = Image.open(ruta_imagen)
            img.thumbnail((100, 100), Image.LANCZOS)
            self.photo_image = ImageTk.PhotoImage(img)
            self.img_label_preview.config(image=self.photo_image, text="")
        except Exception:
            self.img_label_preview.config(image=None, text="Error img")

    def limpiar_formulario(self):
        self.entry_titulo.delete(0, END)
        self.text_desc.delete("1.0", END)
        self.entry_lugar.delete(0, END)
        self.img_label_preview.config(image=None, text="Sin imagen")
        self.photo_image = None
        self.ruta_imagen_seleccionada = None

    def popular_tabla_eventos(self, eventos):
        for item in self.tree.get_children():
            self.tree.delete(item)
        for e in eventos:
            fecha = e['fecha_evento'].strftime('%Y-%m-%d %H:%M')
            self.tree.insert("", END, iid=e['id_evento'],
                             values=(e['id_evento'], e['titulo'], fecha, e['lugar']))

    def obtener_datos_formulario(self):
        return {
            "titulo": self.entry_titulo.get(),
            "descripcion": self.text_desc.get("1.0", END).strip(),
            "fecha": self.entry_fecha.get_date(),
            "lugar": self.entry_lugar.get(),
            "foto_path": self.ruta_imagen_seleccionada
        }