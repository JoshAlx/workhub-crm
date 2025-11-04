# models/billing_model.py
from .database import crear_conexion
from mysql.connector import Error


def crear_factura(id_miembro, monto, emision, vencimiento, descripcion, estado):
    conn = crear_conexion()
    if not conn: return False
    sql = "INSERT INTO Facturas (id_miembro, monto, fecha_emision, fecha_vencimiento, estado_pago, descripcion) VALUES (%s, %s, %s, %s, %s, %s)"
    try:
        cursor = conn.cursor()
        cursor.execute(sql, (id_miembro, monto, emision, vencimiento, estado, descripcion))
        conn.commit()
        return True
    except Error as e:
        print(f"Error al crear factura: {e}")
        return False
    finally:
        if conn and conn.is_connected(): cursor.close(); conn.close()


def obtener_facturas_por_rango(id_sede, fecha_inicio, fecha_fin):
    """
    Obtiene facturas por rango de fechas para el requisito de exportación.
    Maneja id_sede=None para SuperAdmin.
    """
    conn = crear_conexion()
    if not conn: return []

    try:
        cursor = conn.cursor(dictionary=True)

        # Construcción de la consulta dinámica
        sql_base = """
        SELECT f.*, m.nombre_completo, s.nombre_sede
        FROM Facturas f
        JOIN Miembros m ON f.id_miembro = m.id_miembro
        JOIN Sedes s ON m.id_sede = s.id_sede
        """

        condiciones = ["f.fecha_emision BETWEEN %s AND %s"]
        datos = [fecha_inicio, fecha_fin]

        if id_sede: # Si id_sede NO es None (es un Admin)
            condiciones.append("m.id_sede = %s")
            datos.append(id_sede)

        # Unir las condiciones
        sql_final = sql_base + " WHERE " + " AND ".join(condiciones) + " ORDER BY f.fecha_emision"

        cursor.execute(sql_final, datos)
        return cursor.fetchall()
    except Error as e:
        print(f"Error al obtener facturas por rango: {e}")
        return []
    finally:
        if conn and conn.is_connected(): cursor.close(); conn.close()


def obtener_facturas_pendientes_vencidas(id_sede):
    """Regla 3: Suspensión por falta de pago ."""
    conn = crear_conexion()
    if not conn: return []
    sql = """
          SELECT f.id_factura, f.id_miembro
          FROM Facturas f
                   JOIN Miembros m ON f.id_miembro = m.id_miembro
          WHERE m.id_sede = %s
            AND f.estado_pago = 'Pendiente'
            AND f.fecha_vencimiento < CURDATE() \
          """
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(sql, (id_sede,))
        return cursor.fetchall()
    except Error as e:
        print(f"Error al obtener facturas vencidas: {e}")
        return []
    finally:
        if conn and conn.is_connected(): cursor.close(); conn.close()


def generar_facturas_recurrentes(id_sede):
    """Regla 2: Facturación automática ."""
    conn = crear_conexion()
    if not conn: return False

    # Obtiene miembros activos de la sede y el precio de su plan
    sql_miembros = """
                   SELECT m.id_miembro, p.precio, p.nombre_plan
                   FROM Miembros m
                            JOIN Planes p ON m.id_plan = p.id_plan
                   WHERE m.id_sede = %s \
                     AND m.estado = 'Activo' \
                   """

    sql_insert = """
                 INSERT INTO Facturas (id_miembro, monto, fecha_emision, fecha_vencimiento, estado_pago, descripcion)
                 VALUES (%s, %s, CURDATE(), DATE_ADD(CURDATE(), INTERVAL 5 DAY), 'Pendiente', %s) \
                 """

    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(sql_miembros, (id_sede,))
        miembros_a_facturar = cursor.fetchall()

        count = 0
        for miembro in miembros_a_facturar:
            desc = f"Factura recurrente plan {miembro['nombre_plan']}"
            cursor.execute(sql_insert, (miembro['id_miembro'], miembro['precio'], desc))
            count += 1

        conn.commit()
        return count  # Retorna cuántas facturas se generaron

    except Error as e:
        print(f"Error al generar facturas recurrentes: {e}")
        return 0
    finally:
        if conn and conn.is_connected(): cursor.close(); conn.close()