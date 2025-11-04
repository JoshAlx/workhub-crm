# controllers/auth_controller.py
from views.login_view import LoginView
from views.main_view import MainView
from models.user_model import obtener_usuario_por_email, actualizar_hash_usuario
from utils.password_hasher import verificar_password, hashear_password


# Se eliminó la importación de ttkbootstrap

class AuthController:
    def __init__(self, app):
        self.app = app  # Referencia a la App principal (main.py)
        self.view = LoginView()
        self.view.login_button.config(command=self.login)

        # --- FIX: Hashear passwords placeholder ---
        self.setup_initial_passwords()

    def setup_initial_passwords(self):
        """Hashea los passwords 'admin123' y 'super123' que pusimos en el SQL."""
        try:
            user_s = obtener_usuario_por_email('super@workhub.com')
            if user_s and user_s['password_hash'] == 'placeholder':
                hash_s = hashear_password('super123')
                actualizar_hash_usuario(user_s['id_usuario'], hash_s)
                print("Hash de SuperAdmin actualizado.")

            user_a = obtener_usuario_por_email('admin@workhub.com')
            if user_a and user_a['password_hash'] == 'placeholder':
                hash_a = hashear_password('admin123')
                actualizar_hash_usuario(user_a['id_usuario'], hash_a)
                print("Hash de Admin actualizado.")
        except Exception as e:
            print(f"Error al inicializar hashes (ignorar si ya se hizo): {e}")

    def run(self):
        self.view.mainloop()

    def login(self):
        email = self.view.email_entry.get()
        password = self.view.password_entry.get()

        if not email or not password:
            self.view.show_error("Email y contraseña son requeridos.")
            return

        usuario = obtener_usuario_por_email(email)

        if not usuario:
            self.view.show_error("Usuario no encontrado.")
            return

        # Verificar contraseña hasheada
        if not verificar_password(password, usuario['password_hash']):
            self.view.show_error("Contraseña incorrecta.")
            return

        # Login exitoso
        self.view.clear_error()
        self.view.hide()  # Oculta la ventana de Login

        # Guardar info del usuario en la app
        self.app.set_current_user({
            "id": usuario['id_usuario'],
            "nombre": usuario['nombre_completo'],
            "email": usuario['email'],
            "rol": usuario['rol'],
            "id_sede": usuario['id_sede_asignada'],
            "sede": usuario.get('nombre_sede', 'N/A')
        })

        # Abrir la vista principal
        self.app.show_main_view()