import pyrebase
import bcrypt  # Importar bcrypt para el hashing de contraseñas
import json

config = {
    "apiKey": "AIzaSyBJf1q8pBMRDbK1-QsCBOAlCFWlC7ehh1A",
    "authDomain": "babychatpediatras.firebaseapp.com",
    "databaseURL": "https://babychatpediatras-default-rtdb.firebaseio.com",
    "storageBucket": "babychatpediatras.firebasestorage.app"
}

firebase = pyrebase.initialize_app(config)
db = firebase.database()
auth = firebase.auth()

def registrar_usuario(nombre, apellido1, apellido2, fecha_nacimiento, correo, licencia, password):
    try:
        # Verificar si el usuario ya existe
        try:
            auth.sign_in_with_email_and_password(correo, password)
            print("El usuario ya existe en Firebase.")
            return False  # No se registra si ya existe
        except:
            pass  # Si el usuario no existe, continúa con el registro
        
        # Hash de la contraseña antes de guardarla en la base de datos
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        
        # Registrar usuario en Firebase Authentication
        user = auth.create_user_with_email_and_password(correo, password)
        
        # Guardar información adicional en la base de datos
        datos_usuario = {
            "nombre": nombre,
            "apellido1": apellido1,
            "apellido2": apellido2,
            "fecha_nacimiento": fecha_nacimiento,
            "correo": correo,
            "licencia": licencia,
            "password_hash": hashed_password,  # Guardar solo el hash, no la contraseña en texto plano
            "uid": user["localId"]  # ID único de Firebase
        }
        
        # Usar child() en lugar de collection() para Realtime Database
        # Nota: Firebase Realtime Database no permite puntos en las claves
        db.child("usuarios").child(correo.replace(".", ",")).set(datos_usuario)
        
        print("Usuario registrado correctamente.")
        return True
    
    except Exception as e:
        try:
            error = json.loads(e.args[1])  # Decodificar error de Firebase
            if "EMAIL_EXISTS" in error["error"]["message"]:
                print("El correo ya está registrado.")
            else:
                print(f"Error al registrar usuario: {error['error']['message']}")
        except:
            print(f"Error inesperado: {str(e)}")
        return False