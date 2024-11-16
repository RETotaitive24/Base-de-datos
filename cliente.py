import requests
    
def crear_usuario(nombre, password):
    url = 'http://localhost:5000/usuarios'
    data = {'nombre': nombre, 'password': password}
    response = requests.post(url, json=data)
    if response.status_code == 201:
        print("Usuario creado exitosamente")
        return response.json()
    else:
        print("Error al crear usuario:", response.text)

def obtener_usuario(id):
    url = f'http://localhost:5000/usuarios/{id}'
    response = requests.get(url)
    if response.status_code == 200:
        print("Usuario encontrado:")
        return response.json()
    else:
        print("Usuario no encontrado")

def eliminar_usuario(id):
    url = f'http://localhost:5000/usuarios/{id}'
    response = requests.delete(url)
    if response.status_code == 200:
        print("Usuario eliminado exitosamente")
    else:
        print("Error al eliminar usuario")

def obtener_usuarios_protegidos():
    url = 'http://localhost:5000/usuarios-protegidos'
    response = requests.get(url, auth=('user', '123456'))  # Reemplaza con tus credenciales
    if response.status_code == 200:
        print("Usuarios protegidos:")
        return response.json()
    else:
        print("No tienes autorización para ver esta información")

if __name__ == '__main__':
    # Crear un nuevo usuario
    nuevo_usuario = crear_usuario("Nuevo Usuario", "contraseña123")

    # Obtener un usuario por ID
    usuario = obtener_usuario(nuevo_usuario['id'])
    print(usuario)

    # Eliminar un usuario
    eliminar_usuario(nuevo_usuario['id'])

    # Obtener usuarios protegidos (requiere autenticación)
    usuarios_protegidos = obtener_usuarios_protegidos()
    print(usuarios_protegidos)