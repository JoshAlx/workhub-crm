# models/community_model.py
from .database import crear_conexion
from mysql.connector import Error

# --- CRUD Anuncios ---

def crear_anuncio(titulo, contenido, id_usuario, id_sede):
    conn = crear_conexion()
    if not conn: return False
    sql = "INSERT INTO Anuncios (titulo, contenido, id_usuario_publica, id_sede) VALUES (%s, %s, %s, %s)"
    try:
        cursor = conn.cursor()
        cursor.execute(sql, (titulo, contenido, id_usuario, id_sede))
        conn.commit()
        return True
    except Error as e:
        print(f"Error al crear anuncio: {e}")
        return False
    finally:
        if conn and conn.is_connected(): cursor.close(); conn.close()

def obtener_anuncios_por_sede(id_sede):
    conn = crear_conexion()
    if not conn: return []
    sql = """
    SELECT a.*, u.nombre_completo AS autor
    FROM Anuncios a
    JOIN Usuarios u ON a.id_usuario_publica = u.id_usuario
    WHERE a.id_sede = %s
    ORDER BY a.fecha_publicacion DESC
    """
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(sql, (id_sede,))
        return cursor.fetchall()
    except Error as e:
        print(f"Error al obtener anuncios: {e}")
        return []
    finally:
        if conn and conn.is_connected(): cursor.close(); conn.close()

# --- CRUD Eventos (Formulario 2 con imagen)  ---

def crear_evento(titulo, desc, fecha, lugar, img_path, id_sede):
    conn = crear_conexion()
    if not conn: return False
    sql = "INSERT INTO Eventos (titulo, descripcion, fecha_evento, lugar, imagen_evento_path, id_sede) VALUES (%s, %s, %s, %s, %s, %s)"
    try:
        cursor = conn.cursor()
        cursor.execute(sql, (titulo, desc, fecha, lugar, img_path, id_sede))
        conn.commit()
        return True
    except Error as e:
        print(f"Error al crear evento: {e}")
        return False
    finally:
        if conn and conn.is_connected(): cursor.close(); conn.close()

def obtener_eventos_por_sede(id_sede):
    conn = crear_conexion()
    if not conn: return []
    sql = "SELECT * FROM Eventos WHERE id_sede = %s ORDER BY fecha_evento DESC"
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(sql, (id_sede,))
        return cursor.fetchall()
    except Error as e:
        print(f"Error al obtener eventos: {e}")
        return []
    finally:
        if conn and conn.is_connected(): cursor.close(); conn.close()