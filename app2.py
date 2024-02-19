import csv
import pyodbc

# Establecer la cadena de conexión
connection_string = 'DRIVER={SQL Server};SERVER=190.210.182.24\\sqlexpress;DATABASE=Pisos;UID=sa;PWD=Open6736'
connection = pyodbc.connect(connection_string)

# Crear un cursor para ejecutar consultas
cursor = connection.cursor()

# Configurar ARITHABORT a ON
cursor.execute("SET ARITHABORT ON")

# Lista de parámetros
parametros = [47835,
47851,
47857,
47858,
47859,
47861,
47862,
47887,
47888,
47890,
47892,
47893,
47902,
47906,
47915,
47918,
47920,
47921,
47922,
47923,
47930,
47931,
47941,
47949,
47950,
47952,
47953,
47958,
47959,
47962,
47964,
47966,
47967,
47968,
47969,
47973,
47974,
47976,
47982,
47985,
47986,
47987,
47994,
47996,
48005,
48008,
48009,
48011,
48018,
48021,
48022,
48026,
48032,
48036,
48044,
48047,
48048,
48050,
48058,
48059,
48064,
48068,
48075,
48077,
48089,
48090,
48091,
48095,
48096,
48098,
48100,
48103,
48104,
48106,
48108,
48109,
48110,
48112,
48116,
48118,
48122,
48123,
48126,
48128,
48130,
48131,
48136,
48137,
48139,
48147,
48148,
48155,
48156,
48157,
48159,
48161,
48163,
48165,
48167,
48168,
48169,
48172,
48173,
48174,
48176,
48178,
48179,
48188,
48189,
48191,
48192,
48194,
48201,
48205,
48214,
48215,
48220,
48221,
48223,
48234,
48236,
48238,
48239,
48241,
48249,
48250,
48252,
48256,
48259,
48262,
48265,
48268,
48277,
48278,
48282,
48284,
48288,
48289,
48290,
48293,
48295,
48302,
48303,
48307,
48314,
48316,
48319,
48321,
48323,
48327,
48328,
48331,
48335
]

# Obtener los nombres de las columnas una vez ejecutada la consulta con el primer parámetro
cursor.execute("EXEC SP_DetalleInformacionPresupuestos ?", parametros[0])
column_names = [column[0] for column in cursor.description]

# Escribir los resultados en un archivo CSV
with open('resultados.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    # Escribir los nombres de las columnas
    writer.writerow(column_names)
    
    # Escribir los datos para cada parámetro
    for parametro in parametros:
        cursor.execute("EXEC SP_DetalleInformacionPresupuestos ?", parametro)
        results = cursor.fetchall()
        writer.writerows(results)

print(results)

# Cerrar el cursor y la conexión
cursor.close()
connection.close()
