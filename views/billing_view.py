# views/billing_view.py
import tkinter as tk
from tkinter import ttk
from tkinter.constants import *
from .base_view import BaseView
from tkcalendar import DateEntry


class BillingView(BaseView):
    def __init__(self, master):
        super().__init__(master, title="Gestión de Facturación")
        self.geometry("1000x600")

        main_frame = ttk.Frame(self, padding=10)
        main_frame.pack(expand=True, fill=BOTH)
        main_frame.rowconfigure(1, weight=1)
        main_frame.columnconfigure(0, weight=1)

        # --- 1. Frame Filtros y Acciones ---
        action_frame = ttk.Labelframe(main_frame, text=" Acciones y Filtros ", padding=15)
        action_frame.grid(row=0, column=0, sticky=NSEW, padx=10, pady=10)

        # Eliminados bootstyle, style y el parche _determine_downarrow
        ttk.Label(action_frame, text="Fecha Inicio:").grid(row=0, column=0, padx=(0, 5))
        self.filtro_fecha_inicio = DateEntry(action_frame, width=12, date_pattern='yyyy-mm-dd', locale='es_ES')
        self.filtro_fecha_inicio.grid(row=0, column=1, padx=(0, 20))

        ttk.Label(action_frame, text="Fecha Fin:").grid(row=0, column=2, padx=(0, 5))
        self.filtro_fecha_fin = DateEntry(action_frame, width=12, date_pattern='yyyy-mm-dd', locale='es_ES')
        self.filtro_fecha_fin.grid(row=0, column=3, padx=(0, 20))

        # Eliminados bootstyle
        self.btn_filtrar = ttk.Button(action_frame, text="Filtrar")
        self.btn_filtrar.grid(row=0, column=4, padx=10)

        self.btn_exportar_excel = ttk.Button(action_frame, text="Exportar a Excel")
        self.btn_exportar_excel.grid(row=0, column=5, padx=10)

        self.btn_exportar_pdf = ttk.Button(action_frame, text="Exportar a PDF")
        self.btn_exportar_pdf.grid(row=0, column=6, padx=10)

        # --- 2. Frame Lista de Facturas ---
        list_frame = ttk.Frame(main_frame)
        list_frame.grid(row=1, column=0, sticky=NSEW, padx=10, pady=10)
        list_frame.rowconfigure(0, weight=1)
        list_frame.columnconfigure(0, weight=1)

        self.tree = ttk.Treeview(list_frame, columns=("ID", "Miembro", "Monto", "Emisión", "Vencimiento", "Estado"),
                                 show="headings")
        self.tree.grid(row=0, column=0, sticky=NSEW)
        self.tree.heading("ID", text="ID");
        self.tree.column("ID", width=50, anchor=CENTER)
        self.tree.heading("Miembro", text="Miembro");
        self.tree.column("Miembro", width=250)
        self.tree.heading("Monto", text="Monto");
        self.tree.column("Monto", width=100, anchor=E)
        self.tree.heading("Emisión", text="F. Emisión");
        self.tree.column("Emisión", width=100, anchor=CENTER)
        self.tree.heading("Vencimiento", text="F. Vencimiento");
        self.tree.column("Vencimiento", width=100, anchor=CENTER)
        self.tree.heading("Estado", text="Estado");
        self.tree.column("Estado", width=100, anchor=CENTER)

        scrollbar = ttk.Scrollbar(list_frame, orient=VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.grid(row=0, column=1, sticky=NS)

        self.datos_filtrados = []

    def popular_tabla_facturas(self, facturas):
        self.datos_filtrados = facturas
        for item in self.tree.get_children():
            self.tree.delete(item)
        for f in facturas:
            monto = f"${f['monto']:.2f}"
            self.tree.insert("", END, iid=f['id_factura'],
                             values=(f['id_factura'], f['nombre_completo'], monto,
                                     f['fecha_emision'], f['fecha_vencimiento'], f['estado_pago']))