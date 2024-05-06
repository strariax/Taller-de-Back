from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Usuarios(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    nombre = db.Column(db.String(50), nullable =  False)
    apellido = db.Column(db.String(50), nullable =  False)
    cedula = db.Column(db.String(10), nullable =  False)
    correo = db.Column(db.String(), nullable = False)

    def __init__(self, nombre, apellido, cedula, correo):
        self.nombre = nombre
        self.apellido = apellido
        self.cedula = cedula
        self.correo = correo

class Notas(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    fecha = db.Column(db.String(50), nullable =  False)
    titulo = db.Column(db.String(50), nullable =  False)
    descripción = db.Column(db.String(10), nullable =  False)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)

    def __init__(self, fecha, titulo, descripción, usuario_id):
        self.fecha = fecha
        self.titulo = titulo
        self.descripción = descripción
        self.usuario_id = usuario_id