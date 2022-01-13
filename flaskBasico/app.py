from flask import Flask, render_template, jsonify, request, \
                  redirect, url_for, send_from_directory, session, \
                  abort
import os

# decorador: función que modifica el comportamiento de otra
# TODO: incluir argumentos en el decorador
def auth(func):
    def inner_func(*args, **kwargs):
        if 'username' in session:
            return func(*args, **kwargs)
        return redirect(url_for('login'))
    inner_func.__name__ = func.__name__
    return inner_func



# se crea una aplicación Flask
app = Flask(__name__)
# Set the secret key to some random bytes. Keep this really secret!
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

# usaremos una lista de diccionarios para almacenar datos
alumnado = [ {"nombre": "Juan"},
             {"nombre": "Maria"},
             {"nombre": "Ana"},
             ]


# @app.route se aplica a una función que será ejecutada al recibir una petición a la url
@app.route('/')
@auth
def hello_world():
    # cuando el resultado de una url debe ser una plantilla se usa render_template
    # el primer argumento es el nombre de la plantilla (debe estar en la carpeta templates)
    # los siguientes argumentos son las variables que se pueden usar en la plantilla
    return render_template("index.html", gente="Alumnos de 2º DAW mañanero")

# en las rutas podemos admitir argumentos variables
# se puede especificar el tipo de datos (string, int, path, ...)
@app.route('/alumnado/<string:nombre>')
@auth
# el nombre del argumento de la url debe coindidir con el argumento de la función
def get_alumnado(nombre):
    # cuando la url responda con contenido, json se usa jsonify
    # hay que cuidar que el tipo de los datos que pasemos a jsonify sean serializables
    resultado = [ alumno
                    for alumno in alumnado
                    if nombre in alumno.get("nombre") ]
    if len(resultado) == 0:
        abort(404, f"No hay alumnos que contengan: {nombre}")
    return jsonify()

# se puede indicar una lista de métodos aceptados en la ruta
@app.route('/nuevo/', methods=['POST'])
@auth
def nuevo_alumno():
    # cuando los datos provienen de un formulario, se encuentran en formato diccionario
    # en request.form
    alumnado.append({"nombre": request.form.get("nombre")})
    # si el formulario permite la subida de archivos, se encuentran en request.files
    imagen = request.files['imagen']
    # para obtener la carpeta donde se ejecuta flask (python puro)
    #carpeta = os.path.abspath(os.curdir)
    # thx Pablo (from flask)
    carpeta = app.root_path
    # request.files es una lista de objetos de tipo FileStorage
    # este objeto admite el método save() para guardar su contenido en disco
    # también disponemos de acceso al nombre de archivo y otros atributos interesantes
    imagen.save(carpeta+"/static/"+imagen.filename)
    # send_static_file devuelve un paquete http, que podemos modificar su encabezado
    #envio = app.send_static_file(imagen.filename)
    # modificamos la propiedad conten_type por una fake
    #envio.content_type = "image/tururu"
    return app.send_static_file(imagen.filename)

# thx Joserra
@app.route("/subir/", methods=['GET', 'POST'])
@auth
def subir():
    # comprobamos si el método de la petición es GET
    if request.method == 'GET':
        return render_template("subir.html")
    archivo = request.files['archivo']
    carpeta = app.root_path
    # si la carpeta archivos no está creada se produce error
    archivo.save(carpeta + "/archivos/" + archivo.filename)
    # redirección (da problemas en insomnia, porque no cambia el método de la petición)
    # url_for : método acepta el nombre de una función asociada a una ruta
    return redirect(url_for('hello_world', _method='GET'))

# permitimos que el path tenga '/'
@app.route('/descargar/<path:path>')
@auth
def descargar(path):
    # cuando la respuesta es un archivo que no está en carpeta static
    return send_from_directory('archivos/', path)

# implementación de la autenticación (método simple, no recomendable en producción)
# lo más lógico es usar una librería de terceros
# thx Pablo: Flask-Login
@app.route("/login/", methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    username = request.form['username']
    if username == 'Gonzalo':
        return redirect(url_for('login', _method='GET'))
    session['username'] = username
    return redirect(url_for('hello_world', _method='GET'))

@app.route('/logout')
@auth
def logout():
    session.pop('username')
    return redirect(url_for('login', _method='GET'))

if __name__ == '__main__':
    # la aplicación se pone en marcha (solo si se llama directamente, no a través de import)
    app.run()
