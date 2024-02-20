import csv
import pyodbc

# Establecer la cadena de conexión
connection_string = 'DRIVER={SQL Server};SERVER=190.210.182.24\\sqlexpress;DATABASE=Pisos;UID=sa;PWD=Open6736'
connection = pyodbc.connect(connection_string)

# Crear un cursor para ejecutar consultas
cursor = connection.cursor()

# Configurar ARITHABORT a ON
cursor.execute("SET ARITHABORT ON")

cursor.execute("EXEC SP_InformacionPresupuestos 1, '31-01-2024', '31-01-2024', -1, -1, -1, -1, -1, -1, -1")

# Obtener los nombres de las columnas
column_names = [column[0] for column in cursor.description]

# Obtener los resultados, si los hay
results = cursor.fetchall()

# Escribir los resultados en un archivo CSV
with open('resultadosinfo.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    # Escribir los nombres de las columnas
    writer.writerow(column_names)
    # Escribir los datos
    writer.writerows(results)

print("Los resultados se han guardado en 'resultados.csv'.")

# Cerrar el cursor y la conexión
cursor.close()
connection.close()