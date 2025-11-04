# controllers/reservation_controller.py
from views.reservation_view import ReservationView
from models import reservation_model, member_model
from datetime import datetime


class ReservationController:
    def __init__(self, master, user_info):
        self.user_info = user_info
        self.id_sede_usuario = self.user_info.get('id_sede')

        # Cargar datos para combos
        self.miembros = member_model.obtener_miembros_por_sede(self.id_sede_usuario)
        self.espacios = reservation_model.obtener_espacios_por_sede(self.id_sede_usuario)

        self.view = ReservationView(master, self.espacios, self.miembros)

        # Bindings
        self.view.btn_guardar.config(command=self.guardar_reserva)
        self.view.combo_miembro.bind("<<ComboboxSelected>>", self.actualizar_creditos_label)
        self.view.filtro_fecha_lista.bind("<<DateEntrySelected>>", self.actualizar_tabla_reservas)

        self.actualizar_tabla_reservas()

    def actualizar_tabla_reservas(self, event=None):
        fecha_filtro = self.view.filtro_fecha_lista.get_date()
        reservas = reservation_model.obtener_reservas_por_fecha(self.id_sede_usuario, fecha_filtro)
        self.view.popular_tabla_reservas(reservas)

    def actualizar_creditos_label(self, event=None):
        id_miembro = self.view.combo_miembro_options.get(self.view.combo_miembro.get())
        if not id_miembro:
            self.view.label_creditos.config(text="Seleccione un miembro...", foreground="black")
            return

        totales, usados = reservation_model.verificar_creditos_miembro(id_miembro)
        disponibles = totales - usados

        texto = f"Créditos de reserva: {disponibles} / {totales} disponibles este mes."
        # Cambiamos la lógica de 'bootstyle' por 'foreground'
        color = "green" if disponibles > 0 else "red"
        self.view.label_creditos.config(text=texto, foreground=color)

    def guardar_reserva(self):
        datos = self.view.obtener_datos_reserva()
        if not datos or not datos['id_miembro'] or not datos['id_espacio']:
            self.view.show_message("Error", "Todos los campos son obligatorios.", "error")
            return

        # --- Regla de Negocio 1: Reserva basada en Plan [cite: 56-58] ---
        totales, usados = reservation_model.verificar_creditos_miembro(datos['id_miembro'])
        if usados >= totales:
            # Requisito: Dirigir a flujo de pago por uso [cite: 58]
            if not self.view.ask_confirmation("Sin Créditos",
                                              "El miembro no tiene créditos de reserva. ¿Desea continuar como un 'Pago por Uso'?"):
                return

        try:
            inicio_dt = datetime.strptime(datos['inicio'], '%Y-%m-%d %H:%M')
            fin_dt = datetime.strptime(datos['fin'], '%Y-%m-%d %H:%M')
            if fin_dt <= inicio_dt:
                self.view.show_message("Error", "La hora de fin debe ser posterior a la hora de inicio.", "error")
                return
        except ValueError:
            self.view.show_message("Error", "Formato de fecha u hora incorrecto.", "error")
            return

        exito = reservation_model.crear_reserva(datos['id_miembro'], datos['id_espacio'], datos['inicio'], datos['fin'])

        if exito:
            self.view.show_message("Éxito", "Reserva creada correctamente.")
            self.actualizar_tabla_reservas()
            self.actualizar_creditos_label()
        else:
            self.view.show_message("Error BD", "No se pudo guardar la reserva (¿conflicto de horario?).", "error")