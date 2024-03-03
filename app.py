from flask import Flask, jsonify
from flask_cors import CORS
import subprocess

app = Flask(__name__)
CORS(app)  # Esto permite solicitudes de otros dominios (CORS)

@app.route('/')
def hola_mundo():
    return '¡Hola Mundo!'

@app.route('/ejecutar_query')
def ejecutar_query():
    try:
        # Ejecuta el archivo nd.js utilizando Node.js
        resultado = subprocess.check_output(['node', 'nd.js'])
        return jsonify({'resultado': resultado.decode('utf-8')})
    except subprocess.CalledProcessError as e:
        # Captura errores si el proceso de Node.js falla
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)
