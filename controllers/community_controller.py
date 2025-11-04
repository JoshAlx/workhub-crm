# controllers/community_controller.py
from views.community_view import CommunityView
from models import community_model
from utils import image_handler
from tkinter.filedialog import askopenfilename
import os


# Cumple con Formulario 2 con imagen
class CommunityController:
    def __init__(self, master, user_info):
        self.user_info = user_info
        self.id_sede_usuario = self.user_info.get('id_sede')

        self.view = CommunityView(master)

        # Bindings
        self.view.btn_guardar.config(command=self.guardar_evento)
        self.view.btn_cargar_imagen.config(command=self.seleccionar_imagen)

        self.actualizar_tabla()

    def actualizar_tabla(self):
        eventos = community_model.obtener_eventos_por_sede(self.id_sede_usuario)
        self.view.popular_tabla_eventos(eventos)

    def seleccionar_imagen(self):
        ruta_origen = askopenfilename(
            title="Seleccionar flyer del evento",
            filetypes=[("Imágenes", "*.jpg *.jpeg *.png *.gif")]
        )
        if not ruta_origen:
            return
        self.view.ruta_imagen_seleccionada = ruta_origen
        self.view.set_preview_image(ruta_origen)

    def guardar_evento(self):
        datos = self.view.obtener_datos_formulario()

        if not datos['titulo'] or not datos['fecha'] or not datos['lugar']:
            self.view.show_message("Error", "Título, Fecha y Lugar son obligatorios.", "error")
            return

        # Procesamiento de Imagen (PILLOW )
        ruta_destino_final = None
        if datos['foto_path']:
            destino_dir = "assets/images/events"
            os.makedirs(destino_dir, exist_ok=True)
            ruta_destino_final = image_handler.procesar_imagen(datos['foto_path'], destino_dir)

            if not ruta_destino_final:
                self.view.show_message("Error de Imagen", "No se pudo procesar la imagen (Formatos: JPG, PNG, GIF).",
                                       "error")
                return

        # Guardar en BD
        exito = community_model.crear_evento(
            titulo=datos['titulo'],
            desc=datos['descripcion'],
            fecha=datos['fecha'],
            lugar=datos['lugar'],
            img_path=ruta_destino_final,
            id_sede=self.id_sede_usuario
        )

        if exito:
            self.view.show_message("Éxito", "Evento creado correctamente.")
            self.view.limpiar_formulario()
            self.actualizar_tabla()
        else:
            self.view.show_message("Error BD", "No se pudo guardar el evento.", "error")