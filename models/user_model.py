# models/user_model.py
from .database import crear_conexion
from mysql.connector import Error


# --- CRUD Sedes (Gestionado por SuperAdmin) ---

def crear_sede(nombre, direccion, telefono):
    conn = crear_conexion()
    if not conn: return False
    sql = "INSERT INTO Sedes (nombre_sede, direccion, telefono) VALUES (%s, %s, %s)"
    try:
        cursor = conn.cursor()
        cursor.execute(sql, (nombre, direccion, telefono))
        conn.commit()
        return True
    except Error as e:
        print(f"Error al crear sede: {e}")
        return False
    finally:
        if conn and conn.is_connected(): cursor.close(); conn.close()


def obtener_sedes():
    conn = crear_conexion()
    if not conn: return []
    sql = "SELECT * FROM Sedes"
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(sql)
        return cursor.fetchall()
    except Error as e:
        print(f"Error al obtener sedes: {e}")
        return []
    finally:
        if conn and conn.is_connected(): cursor.close(); conn.close()


# --- CRUD Usuarios (Roles) ---

def crear_usuario(nombre, email, password_hash, rol, id_sede):
    conn = crear_conexion()
    if not conn: return False
    if rol == 'SuperAdmin': id_sede = None

    sql = "INSERT INTO Usuarios (nombre_completo, email, password_hash, rol, id_sede_asignada) VALUES (%s, %s, %s, %s, %s)"
    try:
        cursor = conn.cursor()
        cursor.execute(sql, (nombre, email, password_hash, rol, id_sede))
        conn.commit()
        return True
    except Error as e:
        print(f"Error al crear usuario: {e}")
        return False
    finally:
        if conn and conn.is_connected(): cursor.close(); conn.close()


def obtener_usuario_por_email(email):
    conn = crear_conexion()
    if not conn: return None
    sql = "SELECT u.*, s.nombre_sede FROM Usuarios u LEFT JOIN Sedes s ON u.id_sede_asignada = s.id_sede WHERE u.email = %s"
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(sql, (email,))
        return cursor.fetchone()
    except Error as e:
        print(f"Error al obtener usuario por email: {e}")
        return None
    finally:
        if conn and conn.is_connected(): cursor.close(); conn.close()


def actualizar_hash_usuario(id_usuario, nuevo_hash):
    """Función para actualizar los hashes placeholder de la BD."""
    conn = crear_conexion()
    if not conn: return False
    sql = "UPDATE Usuarios SET password_hash = %s WHERE id_usuario = %s"
    try:
        cursor = conn.cursor()
        cursor.execute(sql, (nuevo_hash, id_usuario))
        conn.commit()
        return cursor.rowcount > 0
    except Error as e:
        print(f"Error al actualizar hash: {e}")
        return False
    finally:
        if conn and conn.is_connected(): cursor.close(); conn.close()