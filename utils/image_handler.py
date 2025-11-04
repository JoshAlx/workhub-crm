# utils/image_handler.py
from PIL import Image, ImageTk
import os

# Cumple con el requisito de PILLOW
# Cumple con formatos soportados

MAX_SIZE = (300, 300)
ALLOWED_FORMATS = ('JPEG', 'PNG', 'GIF')  # PIL usa 'JPEG' para .jpg


def procesar_imagen(ruta_origen, ruta_destino_base):
    """
    Redimensiona, convierte a PNG (para consistencia) y guarda la imagen.
    Valida formato y tamaño.
    Retorna la ruta final o None si falla.
    """
    try:
        img = Image.open(ruta_origen)

        # 1. Validación de formato
        if img.format not in ALLOWED_FORMATS:
            print(f"Error: Formato no soportado {img.format}")
            return None

        # 2. Redimensionamiento (Manejo profesional )
        img.thumbnail(MAX_SIZE, Image.LANCZOS)

        # 3. Conversión y guardado
        # Usamos os.path.splitext para obtener el nombre base
        nombre_base = os.path.basename(ruta_origen)
        nombre_sin_ext = os.path.splitext(nombre_base)[0]

        # Guardamos como PNG para estandarizar
        ruta_final = os.path.join(ruta_destino_base, f"{nombre_sin_ext}.png")

        img.save(ruta_final, "PNG")

        return ruta_final

    except Exception as e:
        print(f"Error al procesar imagen con PILLOW: {e}")
        return None


def cargar_imagen_tk(ruta_imagen, size=(100, 100)):
    """Carga una imagen para ser usada en un Label de TKinter."""
    try:
        img = Image.open(ruta_imagen)
        img.thumbnail(size, Image.LANCZOS)
        return ImageTk.PhotoImage(img)
    except Exception as e:
        print(f"Error al cargar imagen TK: {e}")
        return None