from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:@localhost/articulos'
db = SQLAlchemy(app)
class Articulo(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    nombre = db.Column(db.String(20), nullable = False)
    codigo = db.Column(db.String(30), unique = True, nullable = False)
    precio = db.Column(db.String(20), nullable = False)
    
    def __init__(self, nombre, codigo, precio):
        self.nombre = nombre
        self.codigo = codigo
        self.precio = precio
        
#CRUD agregar un articulo
@app.route('/articulo', methods=['POST'])
def agregar_articulo():
    data = request.get_json()
    nuevo_articulo = Articulo (
        nombre=data['nombre'],
        codigo=data['codigo'],
        precio=data['precio']
    )
    db.session.add(nuevo_articulo)
    db.session.commit()
    return jsonify({'message': 'Se agrego un articulo'}), 200


#Listar articulos
@app.route('/articulo', methods=['GET'])
def obtener_articulos():
    articulo = Articulo.query.all()
    articulo_json = [{'nombre': articulo.nombre, 'codigo': articulo.codigo, 'precio': articulo.precio}for articulo in articulo]
    return jsonify(articulo_json),200

#Buscar articulos
@app.route('/articulo/buscar', methods = ['POST'])
def buscar_articulos():
    data = request.get_json()
    codigo = data.get('codigo')
    if codigo:
        articulo = Articulo.query.filter_by(codigo=codigo).first()
        if articulo:
            articulo_json = [{'nombre': articulo.nombre, 'codigo': articulo.codigo, 'precio': articulo.precio}]
            return jsonify(articulo_json),200
    return jsonify({'message': 'Articulo no encontrado'}),400
# Modificar articulos
@app.route('/articulo', methods=['PUT'])
def modificar_articulos():
    data = request.get_json()
    codigo = data.get('codigo')
    if codigo:
        articulo = Articulo.query.filter_by(codigo=codigo).first()
        if articulo:
            # Utiliza data.get para obtener el valor de 'precio'
            articulo.nombre = data.get('nombre', articulo.nombre)
            articulo.precio = data.get('precio')
            db.session.commit()
            return jsonify({'message': 'Se modificó un articulo'}), 200
    return jsonify({'message': 'Articulo no encontrado'}), 400


    
if __name__=='__main__':
    with app.app_context():
        db.create_all()
        app.run(debug=True)
    
