# models/reservation_model.py
from .database import crear_conexion
from mysql.connector import Error


# --- CRUD Espacios ---

def crear_espacio(nombre, tipo, capacidad, id_sede):
    conn = crear_conexion()
    if not conn: return False
    sql = "INSERT INTO Espacios (nombre_espacio, tipo, capacidad, id_sede) VALUES (%s, %s, %s, %s)"
    try:
        cursor = conn.cursor()
        cursor.execute(sql, (nombre, tipo, capacidad, id_sede))
        conn.commit()
        return True
    except Error as e:
        print(f"Error al crear espacio: {e}")
        return False
    finally:
        if conn and conn.is_connected(): cursor.close(); conn.close()


def obtener_espacios_por_sede(id_sede):
    conn = crear_conexion()
    if not conn: return []
    sql = "SELECT * FROM Espacios WHERE id_sede = %s"
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(sql, (id_sede,))
        return cursor.fetchall()
    except Error as e:
        print(f"Error al obtener espacios: {e}")
        return []
    finally:
        if conn and conn.is_connected(): cursor.close(); conn.close()


# --- CRUD Reservas ---

def crear_reserva(id_miembro, id_espacio, inicio, fin):
    conn = crear_conexion()
    if not conn: return False
    sql = "INSERT INTO Reservas (id_miembro, id_espacio, fecha_hora_inicio, fecha_hora_fin, estado) VALUES (%s, %s, %s, %s, 'Confirmada')"
    try:
        cursor = conn.cursor()
        cursor.execute(sql, (id_miembro, id_espacio, inicio, fin))
        conn.commit()
        return True
    except Error as e:
        print(f"Error al crear reserva: {e}")
        return False
    finally:
        if conn and conn.is_connected(): cursor.close(); conn.close()


def obtener_reservas_por_fecha(id_sede, fecha):
    """
    Obtiene las reservas de una sede en una fecha específica para el calendario.
    Maneja id_sede=None para SuperAdmin.
    """
    conn = crear_conexion()
    if not conn: return []

    try:
        cursor = conn.cursor(dictionary=True)

        sql_base = """
        SELECT r.*, m.nombre_completo, e.nombre_espacio, s.nombre_sede
        FROM Reservas r
        JOIN Miembros m ON r.id_miembro = m.id_miembro
        JOIN Espacios e ON r.id_espacio = e.id_espacio
        JOIN Sedes s ON e.id_sede = s.id_sede
        """

        condiciones = ["DATE(r.fecha_hora_inicio) = %s"]
        datos = [fecha]

        if id_sede: # Si id_sede NO es None (es un Admin)
            condiciones.append("e.id_sede = %s")
            datos.append(id_sede)

        sql_final = sql_base + " WHERE " + " AND ".join(condiciones)

        cursor.execute(sql_final, datos)
        return cursor.fetchall()
    except Error as e:
        print(f"Error al obtener reservas: {e}")
        return []
    finally:
        if conn and conn.is_connected(): cursor.close(); conn.close()


def verificar_creditos_miembro(id_miembro):
    """Regla 1: Verifica créditos antes de reservar ."""
    conn = crear_conexion()
    if not conn: return (0, 0)

    sql_creditos = """
                   SELECT p.creditos_reserva_mes
                   FROM Miembros m
                            JOIN Planes p ON m.id_plan = p.id_plan
                   WHERE m.id_miembro = %s \
                   """

    sql_usados = """
                 SELECT COUNT(id_reserva) as usados
                 FROM Reservas
                 WHERE id_miembro = %s AND MONTH (fecha_hora_inicio) = MONTH (CURDATE()) \
                   AND YEAR (fecha_hora_inicio) = YEAR (CURDATE()) \
                 """

    try:
        cursor = conn.cursor(dictionary=True)

        cursor.execute(sql_creditos, (id_miembro,))
        plan_data = cursor.fetchone()
        creditos_totales = plan_data['creditos_reserva_mes'] if plan_data else 0

        cursor.execute(sql_usados, (id_miembro,))
        reservas_data = cursor.fetchone()
        creditos_usados = reservas_data['usados'] if reservas_data else 0

        return (creditos_totales, creditos_usados)

    except Error as e:
        print(f"Error al verificar créditos: {e}")
        return (0, 0)
    finally:
        if conn and conn.is_connected(): cursor.close(); conn.close()