# models/member_model.py
from .database import crear_conexion
from mysql.connector import Error

# --- CRUD Planes ---

def crear_plan(nombre, precio, beneficios, creditos):
    conn = crear_conexion()
    if not conn: return False
    sql = "INSERT INTO Planes (nombre_plan, precio, beneficios, creditos_reserva_mes) VALUES (%s, %s, %s, %s)"
    try:
        cursor = conn.cursor()
        cursor.execute(sql, (nombre, precio, beneficios, creditos))
        conn.commit()
        return True
    except Error as e:
        print(f"Error al crear plan: {e}")
        return False
    finally:
        if conn and conn.is_connected(): cursor.close(); conn.close()

def obtener_planes():
    conn = crear_conexion()
    if not conn: return []
    sql = "SELECT * FROM Planes"
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(sql)
        return cursor.fetchall()
    except Error as e:
        print(f"Error al obtener planes: {e}")
        return []
    finally:
        if conn and conn.is_connected(): cursor.close(); conn.close()

# --- CRUD Miembros ---

def crear_miembro(nombre, email, telefono, datos_fact, estado, foto_path, id_plan, id_sede):
    conn = crear_conexion()
    if not conn: return False
    sql = """
    INSERT INTO Miembros 
    (nombre_completo, email, telefono, datos_facturacion, fecha_registro, estado, foto_perfil_path, id_plan, id_sede)
    VALUES (%s, %s, %s, %s, CURDATE(), %s, %s, %s, %s)
    """
    try:
        cursor = conn.cursor()
        cursor.execute(sql, (nombre, email, telefono, datos_fact, estado, foto_path, id_plan, id_sede))
        conn.commit()
        return True
    except Error as e:
        print(f"Error al crear miembro: {e}")
        return False
    finally:
        if conn and conn.is_connected(): cursor.close(); conn.close()

def obtener_miembros_por_sede(id_sede):
    conn = crear_conexion()
    if not conn: return []
    try:
        cursor = conn.cursor(dictionary=True)
        if id_sede: # Admin
            sql = "SELECT m.*, p.nombre_plan FROM Miembros m JOIN Planes p ON m.id_plan = p.id_plan WHERE m.id_sede = %s"
            cursor.execute(sql, (id_sede,))
        else: # SuperAdmin
            sql = "SELECT m.*, p.nombre_plan, s.nombre_sede FROM Miembros m JOIN Planes p ON m.id_plan = p.id_plan JOIN Sedes s ON m.id_sede = s.id_sede"
            cursor.execute(sql)
        return cursor.fetchall()
    except Error as e:
        print(f"Error al obtener miembros: {e}")
        return []
    finally:
        if conn and conn.is_connected(): cursor.close(); conn.close()

def actualizar_estado_miembro(id_miembro, estado):
    """Regla 3: Suspensión por falta de pago ."""
    conn = crear_conexion()
    if not conn: return False
    sql = "UPDATE Miembros SET estado = %s WHERE id_miembro = %s"
    try:
        cursor = conn.cursor()
        cursor.execute(sql, (estado, id_miembro))
        conn.commit()
        return cursor.rowcount > 0
    except Error as e:
        print(f"Error al actualizar estado de miembro: {e}")
        return False
    finally:
        if conn and conn.is_connected(): cursor.close(); conn.close()

def eliminar_miembro(id_miembro):
    conn = crear_conexion()
    if not conn: return False
    sql = "DELETE FROM Miembros WHERE id_miembro = %s"
    try:
        cursor = conn.cursor()
        cursor.execute(sql, (id_miembro,))
        conn.commit()
        return cursor.rowcount > 0
    except Error as e:
        print(f"Error al eliminar miembro: {e}")
        return False
    finally:
        if conn and conn.is_connected(): cursor.close(); conn.close()