from flask import Flask, jsonify, request
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

# Base de datos simulada
base_datos = {
    "usuarios": [
        {"id": 1, "nombre": "Juan", "password": generate_password_hash("123456")}
    ]
}

# Función auxiliar para encontrar un usuario por ID
def encontrar_usuario(id):
    for usuario in base_datos["usuarios"]:
        if usuario["id"] == id:
            return usuario
    return None

# Ruta para crear un nuevo usuario
@app.route('/usuarios', methods=['POST'])
def crear_usuario():
    data = request.get_json()
    if not data or not 'nombre' in data or not 'password' in data:
        return jsonify({'mensaje': 'Datos inválidos'}), 400
    nuevo_usuario = {
        'id': len(base_datos["usuarios"]) + 1,
        'nombre': data['nombre'],
        'password': 'Hola123'
    }
    base_datos["usuarios"].append(nuevo_usuario)
    return jsonify(nuevo_usuario), 201

# Ruta para obtener un usuario por ID
@app.route('/usuarios/<int:id>', methods=['GET'])
def obtener_usuario(id):
    usuario = encontrar_usuario(id)
    if usuario:
        return jsonify(usuario)
    return jsonify({'mensaje': 'Usuario no encontrado'}), 404

# Ruta para eliminar un usuario por ID
@app.route('/usuarios/<int:id>', methods=['DELETE'])
def eliminar_usuario(id):
    usuario = encontrar_usuario(id)
    if usuario:
        base_datos["usuarios"].remove(usuario)
        return jsonify({'mensaje': 'Usuario eliminado'}), 200
    return jsonify({'mensaje': 'Usuario no encontrado'}), 404

# Decorador para autenticación básica
def requiere_autenticacion(f):
    def wrapper(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_password_hash(base_datos["usuarios"][0]['password'], auth.password):
            return jsonify({'mensaje': 'Credenciales inválidas'}), 401
        return f(*args, **kwargs)
    return wrapper

# Ruta protegida para obtener todos los usuarios
@app.route('/usuarios-protegidos', methods=['GET'])
@requiere_autenticacion
def obtener_usuarios_protegidos():
    return jsonify(base_datos["usuarios"])


@app.route('/usuarios', methods=['GET'])
def obtener_todos_los_usuarios():
    return jsonify(base_datos["usuarios"])

if __name__ == '__main__':
 app.run(port=5000, debug=True)