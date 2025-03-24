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
        user = auth.create_user_with_email_and_password(correo, password)  

        datos_usuario = {
            "nombre": nombre,
            "apellido1": apellido1,
            "apellido2": apellido2,
            "fecha_nacimiento": fecha_nacimiento,
            "correo": correo,
            "licencia": licencia,
            "uid": user["localId"],
            "rol": "user"  # Siempre será "user"
        }

        # Guardar en Firebase
        db.child("usuarios").child(user["localId"]).set(datos_usuario)

        print("Usuario registrado correctamente.")
        return True

    except Exception as e:
        print(f"Error al registrar usuario: {str(e)}")
        return False


def iniciar_sesion(correo, password):
    try:
        user = auth.sign_in_with_email_and_password(correo, password)
        uid = user["localId"]
        
        datos_usuario = db.child("usuarios").child(correo.replace(".", ",")).get().val()
        
        if datos_usuario:
            print("Inicio de sesión exitoso.")
            return datos_usuario  
        else:
            print("No se encontraron datos del usuario.")
            return None

    except Exception as e:
        print(f"Error en el inicio de sesión: {str(e)}")
        return None

def registrar_administrador(nombre, apellido1, apellido2, telefono, correo, rango, password):
    try:
        user = auth.create_user_with_email_and_password(correo, password)

        datos_admin = {
            "nombre": nombre,
            "apellido1": apellido1,
            "apellido2": apellido2,
            "telefono": telefono,
            "correo": correo,
            "rango": rango,
            "uid": user["localId"],
            "rol": "admin"
        }

        db.child("administradores").child(user["localId"]).set(datos_admin)

        print("Administrador registrado correctamente.")
        return True

    except Exception as e:
        print(f"Error al registrar administrador: {str(e)}")
        return False

class Personas:
    def __init__(self):
        self.db = db

    def lista_personas(self):
        try:
            datos = self.db.child("personas").get()
            print("Datos crudos desde Firebase:", datos.val())  
            return datos.val() if datos.val() else {}
        except Exception as e:
            print(f"Error: {str(e)}")
            return {}
    
    def agregar_persona(self, nombre, edad):
        """Método existente para agregar personas simples"""
        try:
            persona = {
                "nombre": nombre,
                "edad": edad
            }
            self.db.child("personas").push(persona)
            return True
        except Exception as e:
            print(f"Error al agregar persona: {str(e)}")
            return False

    def lista_pacientes(self, pediatra_email=None):
        """Método para listar pacientes, opcionalmente filtrando por pediatra"""
        try:
            datos = self.db.child("pacientes").get()
            todos_pacientes = datos.val() if datos.val() else {}
            
            # Si no se especifica pediatra, devolver todos los pacientes
            if not pediatra_email:
                return todos_pacientes
            
            # Filtrar pacientes que tienen el pediatra especificado
            pacientes_filtrados = {}
            for id, paciente in todos_pacientes.items():
                if paciente.get('pediatra') == pediatra_email:
                    pacientes_filtrados[id] = paciente
                    
            print(f"Pacientes filtrados para pediatra {pediatra_email}: {len(pacientes_filtrados)}")
            return pacientes_filtrados
                
        except Exception as e:
            print(f"Error al listar pacientes: {str(e)}")
            return {}

    def lista_pacientes_por_id_y_pediatra(self, paciente_id=None, pediatra_email=None):
        """Método para listar pacientes, filtrando por ID y opcionalmente por pediatra"""
        try:
            datos = self.db.child("pacientes").get()
            todos_pacientes = datos.val() if datos.val() else {}
            
            # Si no se especifican filtros, devolver todos los pacientes
            if not paciente_id and not pediatra_email:
                return todos_pacientes
            
            pacientes_filtrados = {}
            
            for id, paciente in todos_pacientes.items():
                # Filtrar por ID si se proporciona
                if paciente_id and id != paciente_id:
                    continue
                
                # Filtrar por pediatra si se proporciona
                if pediatra_email and paciente.get('pediatra') != pediatra_email:
                    continue
                
                pacientes_filtrados[id] = paciente
            
            print(f"Pacientes filtrados con ID {paciente_id} y pediatra {pediatra_email}: {len(pacientes_filtrados)}")
            return pacientes_filtrados
                
        except Exception as e:
            print(f"Error al listar pacientes: {str(e)}")
            return {}

    def actualizar_paciente(self, paciente_id, datos_actualizar):
        try:
            self.db.child("pacientes").child(paciente_id).update(datos_actualizar)
            print(f"Datos actualizados para el paciente {paciente_id}: {datos_actualizar}")
            return True
        except Exception as e:
            print(f"Error al actualizar paciente: {str(e)}")
            return False



    def agregar_paciente(self, datos_paciente):
        """Método para agregar un paciente completo con todos sus datos"""
        try:
            resultado = self.db.child("pacientes").push(datos_paciente)
            return True
        except Exception as e:
            print(f"Error al agregar paciente: {str(e)}")
            return False