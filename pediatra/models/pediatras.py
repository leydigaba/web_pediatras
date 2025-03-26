import pyrebase
import bcrypt  # Importar bcrypt para el hashing de contraseñas
import os
import json
import uuid
import web 
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
        user = auth.create_user_with_email_and_password(correo, password)  # ¡Firebase maneja la seguridad!
        
        datos_usuario = {
            "nombre": nombre,
            "apellido1": apellido1,
            "apellido2": apellido2,
            "fecha_nacimiento": fecha_nacimiento,
            "correo": correo,
            "licencia": licencia,
            "uid": user["localId"]  
        }
        
        db.child("usuarios").child(correo.replace(".", ",")).set(datos_usuario)
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
                
                paciente["documentos"] = paciente.get("documentos", {})
                pacientes_filtrados[id] = paciente
            
            print(f"Pacientes filtrados con ID {paciente_id} y pediatra {pediatra_email}: {len(pacientes_filtrados)}")
            return pacientes_filtrados
                
        except Exception as e:
            print(f"Error al listar pacientes: {str(e)}")
            return {}

    def agregar_paciente(self, datos_paciente):
        """Método para agregar un paciente completo con todos sus datos"""
        try:
            resultado = self.db.child("pacientes").push(datos_paciente)
            return True
        except Exception as e:
            print(f"Error al agregar paciente: {str(e)}")
            return False
        

    def obtener_pediatra(self, correo):
        """
        Obtiene los datos de un pediatra por su correo electrónico desde Firebase
        """
        try:
            # En Firebase, el punto (.) no está permitido en las claves, así que lo reemplazamos por coma (,)
            correo_key = correo.replace(".", ",")
            datos = self.db.child("usuarios").child(correo_key).get()
            
            if datos.val():
                return datos.val()
            return None
        except Exception as e:
            print(f"Error al obtener pediatra: {str(e)}")
            return None

    def actualizar_pediatra(self, correo, datos):
        try:
            # En Firebase, el punto (.) no está permitido en las claves, así que lo reemplazamos por coma (,)
            correo_key = correo.replace(".", ",")
            
            # En Firebase, podemos actualizar solo los campos específicos
            self.db.child("usuarios").child(correo_key).update(datos)
            
            return True
        except Exception as e:
            print(f"Error al actualizar pediatra: {str(e)}")
            return False

    def actualizar_paciente(self, paciente_id, datos_actualizar):
        try:
            self.db.child("pacientes").child(paciente_id).update(datos_actualizar)
            print(f"Datos actualizados para el paciente {paciente_id}: {datos_actualizar}")
            return True
        except Exception as e:
            print(f"Error al actualizar paciente: {str(e)}")
            return False


    def actualizar_foto_paciente(self, paciente_id, ruta_foto):
        try:
            self.db.child("pacientes").child(paciente_id).update({"foto_perfil": ruta_foto})
            print(f"Foto actualizada para el paciente {paciente_id}")
            return True
        except Exception as e:
            print(f"Error al actualizar foto de paciente: {str(e)}")
            return False
    
    def subir_foto_perfil(self, correo, archivo):
        try:
            # Generar un nombre de archivo único
            extension = os.path.splitext(archivo.filename)[1]
            nombre_archivo = f"{correo.replace('.', '')}{uuid.uuid4()}{extension}"
            
            # Ruta donde se guardará la foto
            ruta_local = os.path.join('static', 'uploads', 'perfiles', nombre_archivo)
            ruta_storage = f"perfiles/{nombre_archivo}"
            
            # Asegurar que el directorio exista
            os.makedirs(os.path.dirname(ruta_local), exist_ok=True)
            
            # Guardar archivo localmente
            with open(ruta_local, 'wb') as f:
                f.write(archivo.file.read())
            
            # Verificar si el archivo existe antes de subirlo
            if not os.path.exists(ruta_local):
                print(f"Error: El archivo {ruta_local} no existe")
                return None
            
            # Subir a Firebase Storage
            try:
                self.storage.child(ruta_storage).put(ruta_local)
            except Exception as e:
                print(f"Error al subir a Firebase Storage: {str(e)}")
                # Continuar con la ruta local si la subida falla
            
            # Construir URL de la foto (usar ruta local si la subida falla)
            url_foto = f"/static/uploads/perfiles/{nombre_archivo}"
            
            # Actualizar datos del usuario con la URL de la foto
            correo_key = correo.replace(".", ",")
            self.db.child("usuarios").child(correo_key).update({
                "foto_perfil": url_foto
            })
            
            return url_foto
        except Exception as e:
            print(f"Error al subir foto: {str(e)}")
            return None
        
    def actualizar_foto_bebe(self, paciente_id, archivo):
        try:
            # Generar un nombre de archivo único
            extension = os.path.splitext(archivo.filename)[1]
            nombre_archivo = f"{paciente_id}{uuid.uuid4()}{extension}"
            
            # Ruta donde se guardará la foto
            ruta_local = os.path.join('static', 'uploads', 'bebes', nombre_archivo)
            ruta_storage = f"bebes/{nombre_archivo}"
            
            # Asegurar que el directorio exista
            os.makedirs(os.path.dirname(ruta_local), exist_ok=True)
            
            # Guardar archivo localmente
            with open(ruta_local, 'wb') as f:
                f.write(archivo.file.read())
            
            # Verificar si el archivo existe antes de subirlo
            if not os.path.exists(ruta_local):
                print(f"Error: El archivo {ruta_local} no existe")
                return None
            
            # Subir a Firebase Storage
            try:
                self.storage.child(ruta_storage).put(ruta_local)
            except Exception as e:
                print(f"Error al subir a Firebase Storage: {str(e)}")
                # Continuar con la ruta local si la subida falla
            
            # Construir URL de la foto (usar ruta local si la subida falla)
            url_foto = f"/static/uploads/bebes/{nombre_archivo}"
            
            # Actualizar datos del paciente con la URL de la foto
            self.db.child("pacientes").child(paciente_id).update({
                "foto_perfil": url_foto
            })
            
            print(f"Foto actualizada para el bebé {paciente_id}")
            return url_foto
        except Exception as e:
            print(f"Error al actualizar foto del bebé: {str(e)}")
            return None
    def subir_documentos_paciente(self, paciente_id, datos):
        try:
            documentos_guardados = {}
            
            # Tipos de documentos a guardar
            tipos_documentos = [
                'carnet_vacunacion', 
                'resultados_laboratorio', 
                'recetas_medicas', 
                'otros_documentos'
            ]
            
            for tipo_documento in tipos_documentos:
                archivo = datos.get(tipo_documento, {})
                
                # Check if the file is actually present and has a filename
                if hasattr(archivo, 'filename') and archivo.filename:
                    # Generar un nombre de archivo único
                    extension = os.path.splitext(archivo.filename)[1]
                    nombre_archivo = f"{paciente_id}_{tipo_documento}_{uuid.uuid4()}{extension}"
                    
                    # Ruta donde se guardará el documento
                    ruta_local = os.path.join('static', 'uploads', 'documentos', nombre_archivo)
                    ruta_storage = f"documentos/{nombre_archivo}"
                    
                    # Asegurar que el directorio exista
                    os.makedirs(os.path.dirname(ruta_local), exist_ok=True)
                    
                    # Guardar archivo localmente
                    with open(ruta_local, 'wb') as f:
                        f.write(archivo.file.read())
                    
                    # Verificar si el archivo existe
                    if not os.path.exists(ruta_local):
                        print(f"Error: El archivo {ruta_local} no existe")
                        continue
                    
                    # Construir URL del documento
                    url_documento = f"/static/uploads/documentos/{nombre_archivo}"
                    
                    # Almacenar la URL del documento
                    documentos_guardados[tipo_documento] = url_documento
            
            # Actualizar los documentos en la base de datos
            if documentos_guardados:
                self.db.child("pacientes").child(paciente_id).child("documentos").update(documentos_guardados)
                print(f"Documentos actualizados para el paciente {paciente_id}")
                return documentos_guardados
            
            return None
        
        except Exception as e:
            print(f"Error al subir documentos: {str(e)}")
            return None




