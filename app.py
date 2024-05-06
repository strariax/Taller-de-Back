#Importamos las librerias 
from flask import render_template, request, redirect,url_for, session
from conexion import app, db
from models import Usuarios, Notas

#creamos la ruta principal de nuestra pagina

@app.route('/')
def index():
    nombre = 'Clari'
    return render_template('index.html', nombre = nombre)

@app.route('/registrar', methods = ['POST', 'GET'])

# methods -> Indica a Flask qué métodos HTTP son permitidos para esa ruta específica.Si no especificas el argumento methods, Flask asumirá por defecto que la ruta sólo acepta solicitudes GET, que es cuando un usuario accede a una página web. Se espera que los métodos HTTP sean especificados en mayúsculas. Esto se debe a que los métodos HTTP son definidos en mayúsculas en el protocolo HTTP

def registrar(): # -> Creamos la función registrar

    if request.method == 'POST': # ->  Verifica si la solicitud actual es un POST.

        # Ahora, para acceder a los datos enviados a través del formulario: 

        nombre = request.form['nombre'] # -> request.form es una herramienta que facilita la recopilación y manejo de datos enviados a través de formularios web

        # En request.form['clave'], 'clave' debe ser el nombre del campo de entrada del formulario HTML. Es crucial asegurarse de que los nombres en el HTML coincidan exactamente con los que usas en request.form

        apellido = request.form['apellido']
        cedula = request.form['cedula']
        correo = request.form['correo']

        datos_usuario = Usuarios(nombre, apellido, cedula, correo) # -> Creamos un objeto de la clase usuario con los datos obtenidos

        db.session.add(datos_usuario) # -> Programa el objeto datos_usuario para ser insertado en la base de datos cuando se ejecute la próxima transacción.

        # Se refiere a la sesión de la base de datos, que en SQLAlchemy actúa como un contenedor para todas las operaciones que quieres realizar en la base de datos

        db.session.commit() # -> Este método se utiliza para confirmar todas las operaciones que han sido registradas en la sesión.

        session["usuario_id"] = datos_usuario.id

        # Esta línea guarda un dato específico del usuario en la sesión, en este caso, el id del usuario, que es un identificador único para cada usuario en la base de datos. datos_usuario es un objeto que representa un registro de usuario en la base de datos, y datos_usuario.id es el campo que contiene el ID único asignado a ese usuario.

        return render_template('/cargar_notas.html')

    return render_template('registrar.html')

@app.route('/inicio_sesion', methods=['POST','GET'])

def inicio_sesion():
    if request.method == 'POST':
        cedula = request.form['cedula']
        correo = request.form['correo']
        usuario_existe = Usuarios.query.filter(Usuarios.cedula == cedula).first()

        # Usuario es una clase de modelo en SQLAlchemy que representa una tabla en nuestra base de datos
        # .query permite comenzar una consulta asociada con el modelo Usuarios.
        # .filter permite filtrar los resultados de la consulta basada en una condición.
        # Usuarios.cedula == cedula -> Esta expresión compara cada valor en la columna cedula de la tabla Usuarios con el valor dado en la variable cedula.
        # .first() es un método que se utiliza al final de una consulta SQLAlchemy para devolver el primer resultado de la consulta.

        if usuario_existe:
            if usuario_existe.correo == correo:
                session["usuario_id"] = usuario_existe.id
                return render_template('cargar_notas.html')
        else:
            return render_template("inicio_sesion.html")

    return render_template('inicio_sesion.html')

@app.route('/cargar_notas', methods = ['POST', 'GET'])
def cargar_notas():

    if request.method == 'POST':
        fecha = request.form['fecha']
        titulo = request.form['titulo']
        descripción = request.form['descripción']
        usuario_id = session.get('usuario_id')

        notas_registradas = Notas(fecha, titulo, descripción, usuario_id)

        db.session.add(notas_registradas)
        db.session.commit()

        return render_template('cargar_notas.html')

    return render_template('cargar_notas.html')


@app.route('/ver_notas', methods = ['POST','GET'])

def ver_notas():

    usuario_id = session.get("usuario_id") # -> El método get es un método de diccionario en Python que se utiliza para recuperar un valor de un diccionario usando una clave

    # Consultar la tabla "Notas" para obtener las notas del usuario

    notas = Notas.query.filter_by(usuario_id=usuario_id).all()

    return render_template("ver_notas.html", notas=notas)

@app.route('/actualizar_notas/<int:nota_id>', methods=['GET','POST'])

# <int:nota_id> -> Utiliza una variable de ruta (<int:nota_id>) que indica que esta parte de la URL debe ser un entero y se pasará a la función actualizar_notas como nota_id. Esto permite que la función reciba dinámicamente el ID de una nota específica que se necesita actualizar.

def actualizar_notas(nota_id):
    nota_a_actualizar = Notas.query.get(nota_id)

    if request.method == 'POST':
        fecha = request.form['fecha']
        titulo = request.form['titulo']
        descripción = request.form['descripción']

        nota_a_actualizar.fecha = fecha
        nota_a_actualizar.titulo = titulo
        nota_a_actualizar.descripción = descripción

        db.session.commit()

        return redirect(url_for('ver_notas'))
    
        # render_template() se utiliza para enviar una página al cliente, mientras que redirect(url_for()) se utiliza para enviar al cliente a una página diferente.
    
    return render_template('actualizar_notas.html', nota_a_actualizar=nota_a_actualizar)

@app.route('/eliminar_nota', methods = ['GET','POST'])

def eliminar_nota():
    
    if request.method == 'POST':
        id = request.form['nota_id']
        nota_a_eliminar = Notas.query.filter_by(id=id).first()

        db.session.delete(nota_a_eliminar)

        # El método db.session.delete() es utilizado para eliminar registros de la base de datos.

        db.session.commit()

        return redirect(url_for('ver_notas'))


if __name__ == ("__main__"):
    app.run(debug = True, port=8000)