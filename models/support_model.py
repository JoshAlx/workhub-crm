# models/support_model.py
from .database import crear_conexion
from mysql.connector import Error


def crear_ticket(id_miembro, id_asignado, asunto, desc, prioridad):
    conn = crear_conexion()
    if not conn: return False
    sql = "INSERT INTO Tickets_Soporte (id_miembro_reporta, id_usuario_asignado, asunto, descripcion, estado, prioridad) VALUES (%s, %s, %s, %s, 'Abierto', %s)"
    try:
        cursor = conn.cursor()
        cursor.execute(sql, (id_miembro, id_asignado, asunto, desc, prioridad))
        conn.commit()
        return True
    except Error as e:
        print(f"Error al crear ticket: {e}")
        return False
    finally:
        if conn and conn.is_connected(): cursor.close(); conn.close()


def obtener_tickets_por_sede(id_sede):
    conn = crear_conexion()
    if not conn: return []
    sql = """
          SELECT t.*, m.nombre_completo AS miembro, u.nombre_completo AS asignado
          FROM Tickets_Soporte t
                   JOIN Miembros m ON t.id_miembro_reporta = m.id_miembro
                   LEFT JOIN Usuarios u ON t.id_usuario_asignado = u.id_usuario
          WHERE m.id_sede = %s
          ORDER BY t.fecha_creacion DESC \
          """
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(sql, (id_sede,))
        return cursor.fetchall()
    except Error as e:
        print(f"Error al obtener tickets: {e}")
        return []
    finally:
        if conn and conn.is_connected(): cursor.close(); conn.close()


def actualizar_estado_ticket(id_ticket, estado, id_usuario=None):
    """Regla 5: Escalado de incidentes ."""
    conn = crear_conexion()
    if not conn: return False

    try:
        cursor = conn.cursor()
        if estado == 'Escalado' and id_usuario:
            sql = "UPDATE Tickets_Soporte SET estado = %s, id_usuario_asignado = %s WHERE id_ticket = %s"
            cursor.execute(sql, (estado, id_usuario, id_ticket))
        else:
            sql = "UPDATE Tickets_Soporte SET estado = %s WHERE id_ticket = %s"
            cursor.execute(sql, (estado, id_ticket))
        conn.commit()
        return cursor.rowcount > 0
    except Error as e:
        print(f"Error al actualizar ticket: {e}")
        return False
    finally:
        if conn and conn.is_connected(): cursor.close(); conn.close()