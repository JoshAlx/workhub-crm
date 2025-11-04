# controllers/admin_controller.py
from views.admin_view import AdminView
from models import user_model
from utils.password_hasher import hashear_password
from utils.validator import validar_email, validar_longitud_texto


class AdminController:
    def __init__(self, master):
        self.sedes = user_model.obtener_sedes()
        self.view = AdminView(master, self.sedes)

        # Bindings
        self.view.btn_guardar_sede.config(command=self.guardar_sede)
        self.view.btn_guardar_usuario.config(command=self.guardar_usuario)

    def guardar_sede(self):
        nombre = self.view.sede_nombre.get()
        direccion = self.view.sede_dir.get()
        tel = self.view.sede_tel.get()

        if not nombre or not direccion:
            self.view.show_message("Error", "Nombre y Dirección son obligatorios.", "error")
            return

        exito = user_model.crear_sede(nombre, direccion, tel)
        if exito:
            self.view.show_message("Éxito", "Sede creada. Reinicie la app para verla en los combos.")
            self.view.sede_nombre.delete(0, 'end')
            self.view.sede_dir.delete(0, 'end')
            self.view.sede_tel.delete(0, 'end')
        else:
            self.view.show_message("Error BD", "No se pudo crear la sede.", "error")

    def guardar_usuario(self):
        nombre = self.view.user_nombre.get()
        email = self.view.user_email.get()
        password = self.view.user_pass.get()
        rol = self.view.user_rol.get()
        id_sede = self.view.sedes_options.get(self.view.user_sede.get())

        if not validar_email(email):
            self.view.show_message("Error", "Email inválido.", "error")
            return
        if not validar_longitud_texto(password, min_len=6):
            self.view.show_message("Error", "Password debe tener al menos 6 caracteres.", "error")
            return
        if not rol or not id_sede:
            self.view.show_message("Error", "Rol y Sede son obligatorios.", "error")
            return

        hash_pass = hashear_password(password)

        exito = user_model.crear_usuario(nombre, email, hash_pass, rol, id_sede)
        if exito:
            self.view.show_message("Éxito", "Usuario creado correctamente.")
            self.view.user_nombre.delete(0, 'end')
            self.view.user_email.delete(0, 'end')
            self.view.user_pass.delete(0, 'end')
        else:
            self.view.show_message("Error BD", "No se pudo crear el usuario (Email ya existe?).", "error")