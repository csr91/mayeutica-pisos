import csv
import pyodbc
from datetime import datetime, timedelta
import gspread
from google.oauth2.service_account import Credentials

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
cursor.execute(f"EXEC SP_InformacionPresupuestos 1, '01-11-2023', '29-02-2024', -1, -1, -1, -1, -1, -1, -1")

# Obtener los nombres de las columnas y los resultados
column_names = [column[0] for column in cursor.description]
results_informacion_presupuestos = cursor.fetchall()

# Ejecutar la consulta SQL SP_PresupuestosPendientes con las fechas formateadas
cursor.execute(f"EXEC SP_PresupuestosPendientes 1, '01-11-2023', '29-02-2024'")

# Obtener los resultados de la segunda consulta
results_presupuestos_pendientes = cursor.fetchall()

# Escribir los resultados de la primera consulta en un archivo CSV
with open('resultados_informacion_presupuestos.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(column_names)  # Escribir nombres de columnas
    writer.writerows(results_informacion_presupuestos)  # Escribir resultados

# Escribir los resultados de la segunda consulta en un archivo CSV
with open('resultados_presupuestos_pendientes.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(column_names)  # Escribir nombres de columnas
    writer.writerows(results_presupuestos_pendientes)  # Escribir resultados

print("Resultados guardados en archivos CSV.")