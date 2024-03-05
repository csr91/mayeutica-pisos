import requests

# URL a la que se va a hacer la solicitud
url = "https://pisosrender.onrender.com/pisos"

# Hacer la solicitud GET
response = requests.get(url)

# Comprobar si la solicitud fue exitosa (código de estado 200)
if response.status_code == 200:
    # Imprimir los resultados en la terminal
    print(response.text)
else:
    # Si la solicitud no fue exitosa, imprimir el código de estado
    print("La solicitud no fue exitosa. Código de estado:", response.status_code)