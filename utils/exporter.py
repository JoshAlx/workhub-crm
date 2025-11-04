# utils/exporter.py
from openpyxl import Workbook
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors
import datetime


# Cumple con exportar a Excel
def exportar_a_excel(datos, cabeceras, titulo_archivo):
    """
    Exporta una lista de diccionarios a un archivo Excel.
    'datos' es una lista de diccionarios (ej: [{}, {}])
    'cabeceras' es una lista de strings (ej: ['ID', 'Nombre'])
    """
    # Usamos openpyxl
    wb = Workbook()
    ws = wb.active
    ws.title = "Datos"

    # Añadir cabeceras
    ws.append(cabeceras)

    # Añadir datos
    for fila_dict in datos:
        fila_lista = []
        # Aseguramos que los datos se añadan en el orden de las cabeceras
        # Asumimos que las llaves del dict coinciden con las cabeceras (o una versión en minúscula)
        # Para ser robustos, usamos las cabeceras para extraer los datos
        keys_dict = {k.lower().replace(" ", "_"): k for k in fila_dict.keys()}

        for cabecera in cabeceras:
            # Buscamos la llave correspondiente en el diccionario
            key_a_buscar = cabecera.lower().replace(" ", "_")

            # Buscamos la llave real en el diccionario
            key_real = None
            if key_a_buscar in keys_dict:
                key_real = keys_dict[key_a_buscar]

            # Si no la encontramos por nombre, intentamos por la llave original (ej: 'nombre_completo')
            elif cabecera in fila_dict:
                key_real = cabecera

            valor = fila_dict.get(key_real, "")  # Obtenemos el valor

            # Evitar error de "Aware/Naive datetime"
            if isinstance(valor, datetime.datetime):
                valor = valor.replace(tzinfo=None)

            fila_lista.append(valor)

        ws.append(fila_lista)

    try:
        wb.save(titulo_archivo)
        return True
    except Exception as e:
        print(f"Error al guardar Excel: {e}")
        return False


# Cumple con exportar a PDF
def exportar_a_pdf(datos, cabeceras, titulo_archivo, titulo_documento):
    """
    Exporta datos a un PDF con formato profesional.
    """
    # Usamos reportlab
    doc = SimpleDocTemplate(titulo_archivo, pagesize=letter)
    elements = []

    # Convertimos los datos (lista de dicts) a lista de listas
    data_list = [cabeceras]  # Inicia con las cabeceras

    keys_dict_base = {k.lower().replace(" ", "_"): k for k in datos[0].keys()} if datos else {}

    for fila_dict in datos:
        fila_lista = []
        for cabecera in cabeceras:
            key_a_buscar = cabecera.lower().replace(" ", "_")
            key_real = keys_dict_base.get(key_a_buscar, cabecera)  # Intenta encontrar la llave

            valor = fila_dict.get(key_real, "")

            # Convertir todo a string para ReportLab
            if isinstance(valor, datetime.datetime):
                valor = valor.strftime("%Y-%m-%d %H:%M")
            elif isinstance(valor, datetime.date):
                valor = valor.strftime("%Y-%m-%d")
            else:
                valor = str(valor)

            fila_lista.append(valor)
        data_list.append(fila_lista)

    # Crear la tabla
    table = Table(data_list)

    # Estilo profesional
    style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#4F81BD")),  # Cabecera azul
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor("#DCE6F1")),  # Filas pares
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ])

    # Aplicar estilo de filas alternas (impares)
    for i in range(1, len(data_list)):
        if i % 2 == 0:
            style.add('BACKGROUND', (0, i), (-1, i), colors.HexColor("#B8CCE4"))

    table.setStyle(style)
    elements.append(table)

    try:
        doc.build(elements)
        return True
    except Exception as e:
        print(f"Error al guardar PDF: {e}")
        return False