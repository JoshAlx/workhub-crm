# views/support_view.py
import tkinter as tk
from tkinter import ttk
from tkinter.constants import *
from .base_view import BaseView


class SupportView(BaseView):
    def __init__(self, master):
        super().__init__(master, title="Gestión de Soporte e Incidentes")
        self.geometry("900x600")

        main_frame = ttk.Frame(self, padding=10)
        main_frame.pack(expand=True, fill=BOTH)
        main_frame.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)

        list_labelframe = ttk.Labelframe(main_frame, text=" Tickets de Soporte ", padding=15)
        list_labelframe.grid(row=0, column=0, sticky=NSEW, padx=10, pady=10)
        list_labelframe.rowconfigure(0, weight=1)
        list_labelframe.columnconfigure(0, weight=1)

        self.tree = ttk.Treeview(list_labelframe,
                                 columns=("ID", "Miembro", "Asunto", "Asignado", "Estado", "Prioridad"),
                                 show="headings")
        self.tree.grid(row=0, column=0, columnspan=3, sticky=NSEW)
        self.tree.heading("ID", text="ID");
        self.tree.column("ID", width=40, anchor=CENTER)
        self.tree.heading("Miembro", text="Reporta");
        self.tree.column("Miembro", width=150)
        self.tree.heading("Asunto", text="Asunto");
        self.tree.column("Asunto", width=250)
        self.tree.heading("Asignado", text="Asignado");
        self.tree.column("Asignado", width=150)
        self.tree.heading("Estado", text="Estado");
        self.tree.column("Estado", width=80, anchor=CENTER)
        self.tree.heading("Prioridad", text="Prioridad");
        self.tree.column("Prioridad", width=80, anchor=CENTER)

        scrollbar = ttk.Scrollbar(list_labelframe, orient=VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.grid(row=0, column=3, sticky=NS)

        # Eliminados bootstyle
        self.btn_resolver = ttk.Button(list_labelframe, text="Marcar como Resuelto")
        self.btn_resolver.grid(row=1, column=0, sticky=E, pady=10, padx=5)

        self.btn_escalar = ttk.Button(list_labelframe, text="Escalar a Admin")
        self.btn_escalar.grid(row=1, column=1, sticky=E, pady=10, padx=5)

    def popular_tabla_tickets(self, tickets):
        for item in self.tree.get_children():
            self.tree.delete(item)
        for t in tickets:
            self.tree.insert("", END, iid=t['id_ticket'],
                             values=(t['id_ticket'], t['miembro'], t['asunto'],
                                     t.get('asignado', 'N/A'), t['estado'], t['prioridad']))

    def obtener_id_seleccionado(self):
        try:
            return self.tree.selection()[0]
        except IndexError:
            return None