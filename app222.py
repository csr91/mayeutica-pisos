import csv
import pyodbc
import gspread
from google.oauth2.service_account import Credentials

# Autenticación con Google Sheets
scope = ["https://www.googleapis.com/auth/spreadsheets"]
creds = Credentials.from_service_account_file('auth.json', scopes=scope)
client = gspread.authorize(creds)

# Abrir la hoja de cálculo
spreadsheet = client.open_by_url("https://docs.google.com/spreadsheets/d/1HEJjq5NzeahwSyc47cmC0cJWd8wsQV9xXIKGP2j12t0/edit#gid=0")
worksheet = spreadsheet.worksheet("SP_InformacionPresupuestos")

# Establecer la cadena de conexión
connection_string = 'DRIVER={SQL Server};SERVER=190.210.182.24\\sqlexpress;DATABASE=Pisos;UID=sa;PWD=Open6736'
connection = pyodbc.connect(connection_string)

# Crear un cursor para ejecutar consultas
cursor = connection.cursor()

# Configurar ARITHABORT a ON
cursor.execute("SET ARITHABORT ON")

# Ejecutar el procedimiento almacenado SP_Clientes con el filtro por idCliente
# cursor.execute("EXEC SP_InformacionPresupuestos 1, '15-11-2023', '31-12-2023', -1, -1, -1, -1, -1, -1, -1")
cursor.execute("EXEC SP_PresupuestosPendientes 1, '15-11-2023', '31-12-2023'")

# Obtener los nombres de las columnas
column_names = [column[0] for column in cursor.description]

# Obtener los resultados, si los hay
results = cursor.fetchall()

# Escribir los resultados en la hoja de cálculo
for row in results:
    worksheet.append_row(row)

print("Los resultados se han guardado en la hoja de cálculo 'SP_InformacionPresupuestos'.")

# Cerrar el cursor y la conexión
cursor.close()
connection.close()
