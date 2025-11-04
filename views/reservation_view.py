# views/reservation_view.py
import tkinter as tk
from tkinter import ttk
from tkinter.constants import *
from .base_view import BaseView
from tkcalendar import DateEntry  # Requisito: tkcalendar


class ReservationView(BaseView):
    def __init__(self, master, espacios_list, miembros_list):
        super().__init__(master, title="Gestión de Reservas")
        self.geometry("900x600")

        main_frame = ttk.Frame(self, padding=10)
        main_frame.pack(expand=True, fill=BOTH)
        main_frame.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)  # Formulario
        main_frame.columnconfigure(1, weight=2)  # Lista

        # --- 1. Frame Formulario (Izquierda) ---
        form_labelframe = ttk.Labelframe(main_frame, text=" Nueva Reserva ", padding=15)
        form_labelframe.grid(row=0, column=0, sticky=NSEW, padx=10, pady=10)

        # Miembro
        ttk.Label(form_labelframe, text="Miembro:").grid(row=0, column=0, sticky=W, pady=5)
        self.combo_miembro_options = {m['nombre_completo']: m['id_miembro'] for m in miembros_list}
        self.combo_miembro = ttk.Combobox(form_labelframe, state="readonly",
                                          values=list(self.combo_miembro_options.keys()))
        self.combo_miembro.grid(row=1, column=0, columnspan=2, sticky=EW, pady=5)

        # Espacio
        ttk.Label(form_labelframe, text="Espacio:").grid(row=2, column=0, sticky=W, pady=5)
        self.combo_espacio_options = {e['nombre_espacio']: e['id_espacio'] for e in espacios_list}
        self.combo_espacio = ttk.Combobox(form_labelframe, state="readonly",
                                          values=list(self.combo_espacio_options.keys()))
        self.combo_espacio.grid(row=3, column=0, columnspan=2, sticky=EW, pady=5)

        # Fecha (tkcalendar )
        # Eliminados bootstyle, style y el parche _determine_downarrow
        ttk.Label(form_labelframe, text="Fecha:").grid(row=4, column=0, sticky=W, pady=5)
        self.entry_fecha = DateEntry(form_labelframe, width=18, date_pattern='yyyy-mm-dd',
                                     locale='es_ES', showweeknumbers=False)
        self.entry_fecha.grid(row=5, column=0, sticky=W, pady=5)

        # Hora Inicio
        ttk.Label(form_labelframe, text="Hora Inicio:").grid(row=6, column=0, sticky=W, pady=5)
        self.combo_hora_inicio = ttk.Combobox(form_labelframe, state="readonly",
                                              values=[f"{h:02d}:00" for h in range(7, 22)])
        self.combo_hora_inicio.grid(row=7, column=0, sticky=EW, pady=5, padx=(0, 5))

        # Hora Fin
        ttk.Label(form_labelframe, text="Hora Fin:").grid(row=6, column=1, sticky=W, pady=5)
        self.combo_hora_fin = ttk.Combobox(form_labelframe, state="readonly",
                                           values=[f"{h:02d}:00" for h in range(8, 23)])
        self.combo_hora_fin.grid(row=7, column=1, sticky=EW, pady=5, padx=(5, 0))

        # Eliminado bootstyle
        self.btn_guardar = ttk.Button(form_labelframe, text="Confirmar Reserva")
        self.btn_guardar.grid(row=8, column=0, columnspan=2, pady=20, sticky=EW)

        # Eliminado bootstyle
        self.label_creditos = ttk.Label(form_labelframe, text="Seleccione un miembro...")
        self.label_creditos.grid(row=9, column=0, columnspan=2, pady=10)

        # --- 2. Frame Lista (Derecha) ---
        list_labelframe = ttk.Labelframe(main_frame, text=" Reservas del Día ", padding=15)
        list_labelframe.grid(row=0, column=1, sticky=NSEW, padx=10, pady=10)
        list_labelframe.rowconfigure(1, weight=1)  # Treeview
        list_labelframe.columnconfigure(0, weight=1)

        # Eliminados bootstyle, style y el parche _determine_downarrow
        ttk.Label(list_labelframe, text="Ver reservas para:").grid(row=0, column=0, sticky=W, pady=5)
        self.filtro_fecha_lista = DateEntry(list_labelframe, width=18, date_pattern='yyyy-mm-dd', locale='es_ES')
        self.filtro_fecha_lista.grid(row=0, column=1, sticky=W, pady=5)

        self.tree = ttk.Treeview(list_labelframe, columns=("ID", "Miembro", "Espacio", "Inicio", "Fin"),
                                 show="headings", height=15)
        self.tree.grid(row=1, column=0, columnspan=2, sticky=NSEW)
        self.tree.heading("ID", text="ID");
        self.tree.column("ID", width=40, anchor=CENTER)
        self.tree.heading("Miembro", text="Miembro");
        self.tree.column("Miembro", width=150)
        self.tree.heading("Espacio", text="Espacio");
        self.tree.column("Espacio", width=100)
        self.tree.heading("Inicio", text="Inicio");
        self.tree.column("Inicio", width=120)
        self.tree.heading("Fin", text="Fin");
        self.tree.column("Fin", width=120)

    def popular_tabla_reservas(self, reservas):
        for item in self.tree.get_children():
            self.tree.delete(item)
        for r in reservas:
            inicio = r['fecha_hora_inicio'].strftime('%Y-%m-%d %H:%M')
            fin = r['fecha_hora_fin'].strftime('%Y-%m-%d %H:%M')
            self.tree.insert("", END, iid=r['id_reserva'],
                             values=(r['id_reserva'], r['nombre_completo'], r['nombre_espacio'], inicio, fin))

    def obtener_datos_reserva(self):
        try:
            fecha = self.entry_fecha.get_date()
            hora_inicio = self.combo_hora_inicio.get()
            hora_fin = self.combo_hora_fin.get()

            inicio_dt = f"{fecha} {hora_inicio}"
            fin_dt = f"{fecha} {hora_fin}"

            return {
                "id_miembro": self.combo_miembro_options.get(self.combo_miembro.get()),
                "id_espacio": self.combo_espacio_options.get(self.combo_espacio.get()),
                "inicio": inicio_dt,
                "fin": fin_dt
            }
        except Exception:
            return None