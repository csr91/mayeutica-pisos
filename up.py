from flask import Flask, jsonify

import pyodbc
import gspread
from google.oauth2.service_account import Credentials

app = Flask(__name__)

# Autenticación con Google Sheets
scope = ["https://www.googleapis.com/auth/spreadsheets"]
creds = Credentials.from_service_account_file('auth.json', scopes=scope)
client = gspread.authorize(creds)

# Abrir la hoja de cálculo
spreadsheet = client.open_by_url("https://docs.google.com/spreadsheets/d/1HEJjq5NzeahwSyc47cmC0cJWd8wsQV9xXIKGP2j12t0/edit#gid=0")
worksheet = spreadsheet.worksheet("SP_InformacionPresupuestos")

@app.route('/actualizar-datos')
def actualizar_datos():
    try:
        # Establecer la cadena de conexión
        connection_string = 'DRIVER={SQL Server};SERVER=190.210.182.24\\sqlexpress;DATABASE=Pisos;UID=sa;PWD=Open6736'
        connection = pyodbc.connect(connection_string)

        # Crear un cursor para ejecutar consultas
        cursor = connection.cursor()

        # Configurar ARITHABORT a ON
        cursor.execute("SET ARITHABORT ON")

        cursor.execute("EXEC SP_InformacionPresupuestos 1, '30-12-2023', '31-12-2023', -1, -1, -1, -1, -1, -1, -1")
        # cursor.execute("EXEC SP_PresupuestosPendientes 1, '15-11-2023', '31-12-2023'")

        # Obtener los nombres de las columnas
        column_names = [column[0] for column in cursor.description]

        # Obtener los resultados, si los hay
        results = cursor.fetchall()

        # Escribir los resultados en la hoja de cálculo
        for row in results:
            row_as_text = [str(value) if value is not None else '' for value in row]  # Convertir todos los valores de la fila a texto, dejando en blanco si es None
            worksheet.append_row(row_as_text)

        print("Los resultados se han guardado en la hoja de cálculo 'SP_InformacionPresupuestos'.")

        # Cerrar el cursor y la conexión
        cursor.close()
        connection.close()

        return jsonify({"message": "Datos actualizados correctamente"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run()
