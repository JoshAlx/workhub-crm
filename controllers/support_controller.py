# controllers/support_controller.py
from views.support_view import SupportView
from models import support_model


class SupportController:
    def __init__(self, master, user_info):
        self.user_info = user_info
        self.id_sede_usuario = self.user_info.get('id_sede')

        self.view = SupportView(master)

        # Bindings
        self.view.btn_resolver.config(command=self.resolver_ticket)
        self.view.btn_escalar.config(command=self.escalar_ticket)

        # Ocultar botón de escalar si no es Coordinador (Rol Admin lo recibe)
        if self.user_info.get('rol') != 'Coordinador':
            self.view.btn_escalar.pack_forget()  # Ocultar

        self.actualizar_tabla()

    def actualizar_tabla(self):
        tickets = support_model.obtener_tickets_por_sede(self.id_sede_usuario)
        self.view.popular_tabla_tickets(tickets)

    def resolver_ticket(self):
        id_ticket = self.view.obtener_id_seleccionado()
        if not id_ticket:
            self.view.show_message("Error", "Debe seleccionar un ticket.", "warning")
            return

        exito = support_model.actualizar_estado_ticket(id_ticket, "Resuelto")
        if exito:
            self.view.show_message("Éxito", "Ticket marcado como resuelto.")
            self.actualizar_tabla()
        else:
            self.view.show_message("Error BD", "No se pudo actualizar el ticket.", "error")

    def escalar_ticket(self):
        # Regla 5: Escalado de Incidentes
        # (Simplificado: el Coordinador lo escala manualmente al Admin de su sede)

        id_ticket = self.view.obtener_id_seleccionado()
        if not id_ticket:
            self.view.show_message("Error", "Debe seleccionar un ticket.", "warning")
            return

        # (En un sistema real, buscaríamos al Admin de esta sede (self.id_sede_usuario))
        # (Aquí lo escalamos sin re-asignar, solo cambiando el estado)
        id_admin_sede = None  # Implementar lógica para buscar admin de la sede

        exito = support_model.actualizar_estado_ticket(id_ticket, "Escalado", id_admin_sede)
        if exito:
            self.view.show_message("Éxito", "Ticket escalado al Administrador.")
            self.actualizar_tabla()
        else:
            self.view.show_message("Error BD", "No se pudo escalar el ticket.", "error")