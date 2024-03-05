import time
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

# Almacenar todos los resultados y nombres de columnas en listas separadas
all_results = [results_informacion_presupuestos, results_presupuestos_pendientes]
all_column_names = [column_names, column_names]

# Obtener las hojas de cálculo correspondientes
worksheet_informacion_presupuestos = spreadsheet.worksheet('SP_InformacionPresupuestos')
worksheet_presupuestos_pendientes = spreadsheet.worksheet('SP_PresupuestosPendientes')
worksheets = [worksheet_informacion_presupuestos, worksheet_presupuestos_pendientes]

# Iterar sobre las consultas y pegar los resultados en las hojas de cálculo
for i, (results, column_names) in enumerate(zip(all_results, all_column_names)):
    worksheet = worksheets[i]

    # Borrar el contenido actual de la hoja de cálculo
    worksheet.clear()

    # Pegar los nombres de las columnas en la primera fila
    worksheet.update(range_name='A1', values=[column_names])

    # Construir una lista de listas para todos los resultados
    values = [[str(item) for item in row] for row in results]

    # Pegar todos los resultados en el sheet de una sola vez
    worksheet.update(range_name=f'A2', values=values)

    time.sleep(1)  # Espera un segundo entre cada hoja de cálculo

print("Resultados actualizados en Google Sheets.")
