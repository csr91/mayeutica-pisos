import pyodbc
from datetime import datetime, timedelta
import gspread
from google.oauth2.service_account import Credentials
from flask import Flask

app = Flask(__name__)

@app.route('/pisos')
def update_google_sheets():

    # Autenticación con Google Sheets
    scope = ["https://www.googleapis.com/auth/spreadsheets"]
    creds = Credentials.from_service_account_file('auth.json', scopes=scope)
    client = gspread.authorize(creds)

    # Establecer la cadena de conexión
    connection_string = 'DRIVER={SQL Server};SERVER=190.210.182.24\\sqlexpress;DATABASE=Pisos;UID=sa;PWD=Open6736'
    connection = pyodbc.connect(connection_string)

    # Crear un cursor para ejecutar consultas
    cursor = connection.cursor()

    # Configurar ARITHABORT a ON
    cursor.execute("SET ARITHABORT ON")

    # Obtener la fecha actual y formatearla para la consulta SQL
    fecha_inicio = datetime.now().replace(day=1).strftime('%d-%m-%Y')
    ultimo_dia_mes = datetime(datetime.now().year, datetime.now().month, 1).replace(day=1, month=datetime.now().month % 12 + 1) - timedelta(days=1)
    fecha_fin = ultimo_dia_mes.strftime('%d-%m-%Y')

    # Ejecutar la consulta SQL SP_InformacionPresupuestos con las fechas formateadas
    cursor.execute(f"EXEC SP_InformacionPresupuestos 1, '{fecha_inicio}', '{fecha_fin}', -1, -1, -1, -1, -1, -1, -1")

    # Obtener los nombres de las columnas y los resultados
    column_names = [column[0] for column in cursor.description]
    results_informacion_presupuestos = cursor.fetchall()

    # Ejecutar la consulta SQL SP_PresupuestosPendientes con las fechas formateadas
    cursor.execute(f"EXEC SP_PresupuestosPendientes 1, '{fecha_inicio}', '{fecha_fin}'")

    # Obtener los resultados de la segunda consulta
    results_presupuestos_pendientes = cursor.fetchall()

    # Abrir la hoja de cálculo
    spreadsheet = client.open_by_key('1HEJjq5NzeahwSyc47cmC0cJWd8wsQV9xXIKGP2j12t0')
    worksheet_informacion_presupuestos = spreadsheet.worksheet('SP_InformacionPresupuestos')

    # Borrar el contenido actual de la hoja de cálculo de SP_InformacionPresupuestos
    worksheet_informacion_presupuestos.clear()

    # Escribir los nombres de las columnas de la primera consulta en la primera fila de SP_InformacionPresupuestos
    worksheet_informacion_presupuestos.update(range_name='A1', values=[column_names])

    # Escribir los resultados de la primera consulta en la hoja de cálculo de SP_InformacionPresupuestos
    for i, row in enumerate(results_informacion_presupuestos):
        row_list = [str(item) for item in row]
        worksheet_informacion_presupuestos.update(range_name=f'A{i+2}', values=[row_list])

    # Abrir la hoja de cálculo de SP_PresupuestosPendientes
    worksheet_presupuestos_pendientes = spreadsheet.worksheet('SP_PresupuestosPendientes')

    # Borrar el contenido actual de la hoja de cálculo de SP_PresupuestosPendientes
    worksheet_presupuestos_pendientes.clear()

    # Escribir los nombres de las columnas de la segunda consulta en la primera fila de SP_PresupuestosPendientes
    worksheet_presupuestos_pendientes.update(range_name='A1', values=[column_names])

    # Escribir los resultados de la segunda consulta en la hoja de cálculo de SP_PresupuestosPendientes
    for i, row in enumerate(results_presupuestos_pendientes):
        row_list = [str(item) for item in row]
        worksheet_presupuestos_pendientes.update(range_name=f'A{i+2}', values=[row_list])

    return "Resultados actualizados en Google Sheets."

if __name__ == '__main__':
    app.run(debug=True)
