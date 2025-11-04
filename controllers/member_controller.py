# controllers/member_controller.py
from views.member_view import MemberView
from models import member_model
from utils import validator, image_handler
from tkinter.filedialog import askopenfilename
import os
import shutil


class MemberController:
    def __init__(self, master, user_info):
        self.user_info = user_info
        self.id_sede_usuario = self.user_info.get('id_sede')  # None si es SuperAdmin

        # Cargar datos necesarios para los combos
        self.planes = member_model.obtener_planes()

        self.view = MemberView(master, self.planes)

        # Bindings
        self.view.btn_guardar.config(command=self.guardar_miembro)
        self.view.btn_limpiar.config(command=self.view.limpiar_formulario)
        self.view.btn_eliminar.config(command=self.eliminar_miembro)
        self.view.btn_cargar_imagen.config(command=self.seleccionar_imagen)

        # Cargar datos iniciales
        self.actualizar_tabla()

    def actualizar_tabla(self):
        # SuperAdmin ve todo (id_sede=None), Admin ve solo su sede
        miembros = member_model.obtener_miembros_por_sede(self.id_sede_usuario)
        self.view.popular_tabla(miembros)

    def seleccionar_imagen(self):
        # Cumple requisito Formato y Tamaño
        ruta_origen = askopenfilename(
            title="Seleccionar foto de perfil",
            filetypes=[("Imágenes", "*.jpg *.jpeg *.png *.gif"), ("Todos", "*.*")]
        )
        if not ruta_origen:
            return

        # Guardar ruta temporal para el guardado
        self.view.ruta_imagen_seleccionada = ruta_origen
        # Mostrar preview
        self.view.set_preview_image(ruta_origen)

    def guardar_miembro(self):
        datos = self.view.obtener_datos_formulario()

        # --- Validaciones Requeridas ---
        # 1. Validación Email (RegEx )
        if not validator.validar_email(datos['email']):
            self.view.show_message("Error de Validación", "El formato del email no es válido.", "error")
            return

        # 2. Validación Numérica (Teléfono )
        if not validator.validar_campo_numerico(datos['telefono']):
            self.view.show_message("Error de Validación", "El teléfono solo debe contener números.", "error")
            return

        # 3. Validación Longitud (Nombre )
        if not validator.validar_longitud_texto(datos['nombre'], min_len=3):
            self.view.show_message("Error de Validación", "El nombre debe tener al menos 3 caracteres.", "error")
            return

        if not datos['id_plan']:
            self.view.show_message("Error de Validación", "Debe seleccionar un plan.", "error")
            return

        # --- Procesamiento de Imagen (PILLOW ) ---
        ruta_destino_final = None
        if datos['foto_path']:
            ruta_origen = datos['foto_path']
            # Directorio donde guardaremos las imágenes procesadas
            destino_dir = "assets/images/profiles"
            os.makedirs(destino_dir, exist_ok=True)

            ruta_destino_final = image_handler.procesar_imagen(ruta_origen, destino_dir)

            if not ruta_destino_final:
                self.view.show_message("Error de Imagen",
                                       "No se pudo procesar la imagen. Verifique el formato (JPG, PNG, GIF).", "error")
                return

        # Guardar en BD
        exito = member_model.crear_miembro(
            nombre=datos['nombre'],
            email=datos['email'],
            telefono=datos['telefono'],
            datos_fact="N/A",  # Simplificado
            estado="Activo",
            foto_path=ruta_destino_final,  # Ruta guardada en la BD
            id_plan=datos['id_plan'],
            id_sede=self.id_sede_usuario  # Asigna la sede del Admin
        )

        if exito:
            self.view.show_message("Éxito", "Miembro creado correctamente.")
            self.view.limpiar_formulario()
            self.actualizar_tabla()
        else:
            self.view.show_message("Error BD", "No se pudo guardar el miembro. Verifique si el email ya existe.",
                                   "error")

    def eliminar_miembro(self):
        id_miembro = self.view.obtener_id_seleccionado()
        if not id_miembro:
            self.view.show_message("Error", "Debe seleccionar un miembro de la lista.", "warning")
            return

        # Requisito: Confirmación de datos
        if self.view.ask_confirmation("Confirmar Eliminación",
                                      f"¿Está seguro de que desea eliminar al miembro ID {id_miembro}?"):
            exito = member_model.eliminar_miembro(id_miembro)
            if exito:
                self.view.show_message("Éxito", "Miembro eliminado.")
                self.actualizar_tabla()
            else:
                self.view.show_message("Error BD", "No se pudo eliminar el miembro.", "error")