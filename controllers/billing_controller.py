# controllers/billing_controller.py
from views.billing_view import BillingView
from models import billing_model
from utils.exporter import exportar_a_excel, exportar_a_pdf
from tkinter.filedialog import asksaveasfilename


class BillingController:
    def __init__(self, master, user_info):
        self.user_info = user_info
        self.id_sede_usuario = self.user_info.get('id_sede')

        self.view = BillingView(master)

        # Bindings
        self.view.btn_filtrar.config(command=self.actualizar_tabla_facturas)
        self.view.btn_exportar_excel.config(command=self.exportar_excel)
        self.view.btn_exportar_pdf.config(command=self.exportar_pdf)

        self.actualizar_tabla_facturas()  # Carga inicial

    def actualizar_tabla_facturas(self):
        fecha_inicio = self.view.filtro_fecha_inicio.get_date()
        fecha_fin = self.view.filtro_fecha_fin.get_date()

        facturas = billing_model.obtener_facturas_por_rango(self.id_sede_usuario, fecha_inicio, fecha_fin)
        self.view.popular_tabla_facturas(facturas)

    def exportar_excel(self):
        # Requisito: Exportar a Excel
        datos = self.view.datos_filtrados
        if not datos:
            self.view.show_message("Error", "No hay datos para exportar.", "warning")
            return

        cabeceras = ["ID", "Miembro", "Monto", "Emisión", "Vencimiento", "Estado"]
        # Mapeo de llaves de BD a cabeceras
        datos_mapeados = [
            {"ID": d['id_factura'], "Miembro": d['nombre_completo'], "Monto": d['monto'],
             "Emisión": d['fecha_emision'], "Vencimiento": d['fecha_vencimiento'], "Estado": d['estado_pago']}
            for d in datos
        ]

        ruta = asksaveasfilename(defaultextension=".xlsx", filetypes=[("Archivos Excel", "*.xlsx")])
        if not ruta:
            return

        exito = exportar_a_excel(datos_mapeados, cabeceras, ruta)
        if exito:
            self.view.show_message("Éxito", f"Archivo Excel guardado en:\n{ruta}")
        else:
            self.view.show_message("Error", "No se pudo guardar el archivo Excel.", "error")

    def exportar_pdf(self):
        # Requisito: Exportar a PDF
        datos = self.view.datos_filtrados
        if not datos:
            self.view.show_message("Error", "No hay datos para exportar.", "warning")
            return

        cabeceras = ["ID", "Miembro", "Monto", "Emisión", "Venc.", "Estado"]
        # Mapeo de llaves (similar a Excel)
        datos_mapeados = [
            {"ID": d['id_factura'], "Miembro": d['nombre_completo'], "Monto": f"${d['monto']:.2f}",
             "Emisión": d['fecha_emision'], "Venc.": d['fecha_vencimiento'], "Estado": d['estado_pago']}
            for d in datos
        ]

        ruta = asksaveasfilename(defaultextension=".pdf", filetypes=[("Archivos PDF", "*.pdf")])
        if not ruta:
            return

        exito = exportar_a_pdf(datos_mapeados, cabeceras, ruta, "Reporte de Facturación WorkHub")
        if exito:
            self.view.show_message("Éxito", f"Archivo PDF guardado en:\n{ruta}")
        else:
            self.view.show_message("Error", "No se pudo guardar el archivo PDF.", "error")