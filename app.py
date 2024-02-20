import os
from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hola Mundo!'

if __name__ == '__main__':
    # Utiliza el puerto proporcionado por Heroku si está disponible
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
