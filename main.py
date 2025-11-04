# main.py
import tkinter as tk
from controllers.auth_controller import AuthController
from controllers.member_controller import MemberController
from controllers.reservation_controller import ReservationController
from controllers.billing_controller import BillingController
from controllers.community_controller import CommunityController
from controllers.support_controller import SupportController
from controllers.admin_controller import AdminController
from views.main_view import MainView


# Se eliminó la importación de CURRENT_THEME

class WorkHubApp:
    def __init__(self):
        self.current_user = None
        self.main_view = None

        # Iniciar el controlador de autenticación
        self.auth_controller = AuthController(self)

    def run(self):
        """Inicia el bucle principal de la aplicación (Login)."""
        self.auth_controller.run()

    def set_current_user(self, user_info):
        self.current_user = user_info

    def show_main_view(self):
        """Muestra el dashboard principal después del login."""
        if not self.current_user:
            print("Error: Intento de abrir MainView sin usuario logueado.")
            return

        # La 'root' es la propia ventana de login (que ya fue ocultada por el controller)
        root = self.auth_controller.view

        self.main_view = MainView(root, self.current_user)

        # Conectar botones del dashboard a los controladores
        self.main_view.btn_miembros.config(command=self.open_member_module)
        self.main_view.btn_reservas.config(command=self.open_reservation_module)
        self.main_view.btn_facturacion.config(command=self.open_billing_module)
        self.main_view.btn_comunidad.config(command=self.open_community_module)
        self.main_view.btn_soporte.config(command=self.open_support_module)

        if self.current_user.get('rol') == 'SuperAdmin':
            self.main_view.btn_admin.config(command=self.open_admin_module)

        # Conectar menú
        self.main_view.file_menu.entryconfig("Cerrar Sesión", command=self.logout)

        # Se eliminó la lógica de los menús de temas

    def change_theme(self, theme_name):
        """Función obsoleta, ya no usamos temas."""
        pass

    def logout(self):
        self.current_user = None
        self.main_view.destroy()  # Cierra la ventana del Dashboard

        # Limpiamos los campos y volvemos a mostrar la ventana de login
        self.auth_controller.view.email_entry.delete(0, 'end')
        self.auth_controller.view.password_entry.delete(0, 'end')
        self.auth_controller.view.clear_error()
        self.auth_controller.view.show()  # Muestra el LoginView original

    # --- Métodos para abrir módulos ---

    def open_member_module(self):
        MemberController(self.main_view, self.current_user)

    def open_reservation_module(self):
        ReservationController(self.main_view, self.current_user)

    def open_billing_module(self):
        BillingController(self.main_view, self.current_user)

    def open_community_module(self):
        CommunityController(self.main_view, self.current_user)

    def open_support_module(self):
        SupportController(self.main_view, self.current_user)

    def open_admin_module(self):
        AdminController(self.main_view)


if __name__ == "__main__":
    app = WorkHubApp()
    app.run()