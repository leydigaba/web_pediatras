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

    def lista_pacientes(self):
        """Método para listar pacientes"""
        try:
            datos = self.db.child("pacientes").get()
            print("Datos de pacientes:", datos.val())  
            return datos.val() if datos.val() else {}
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

class CrecimientoInfantilModelo:
    def __init__(self):
        # Inicializar datos de percentiles
        self.edades_meses = list(range(0, 61))  # 0 a 60 meses (5 años)
        
        # Generar datos de percentiles (simulados)
        self._generar_datos_peso()
        self._generar_datos_talla()
    
    def _generar_datos_peso(self):
        # Datos aproximados para niños (peso en kg)
        percentil_3_peso = [2.5 + 0.5 * (i ** 0.8) for i in range(61)]
        percentil_15_peso = [3.0 + 0.55 * (i ** 0.8) for i in range(61)]
        percentil_50_peso = [3.5 + 0.6 * (i ** 0.8) for i in range(61)]
        percentil_85_peso = [4.0 + 0.65 * (i ** 0.8) for i in range(61)]
        percentil_97_peso = [4.5 + 0.7 * (i ** 0.8) for i in range(61)]
        
        # Crear DataFrame para peso
        self.df_peso = pd.DataFrame({
            'edad_meses': self.edades_meses,
            'p3': percentil_3_peso,
            'p15': percentil_15_peso,
            'p50': percentil_50_peso,
            'p85': percentil_85_peso,
            'p97': percentil_97_peso
        })
    
    def _generar_datos_talla(self):
        # Datos aproximados para niños (talla en cm)
        percentil_3_talla = [48 + 15 * np.log(i + 1) for i in range(61)]
        percentil_15_talla = [49 + 15.3 * np.log(i + 1) for i in range(61)]
        percentil_50_talla = [50 + 15.5 * np.log(i + 1) for i in range(61)]
        percentil_85_talla = [51 + 15.8 * np.log(i + 1) for i in range(61)]
        percentil_97_talla = [52 + 16 * np.log(i + 1) for i in range(61)]
        
        # Crear DataFrame para talla
        self.df_talla = pd.DataFrame({
            'edad_meses': self.edades_meses,
            'p3': percentil_3_talla,
            'p15': percentil_15_talla,
            'p50': percentil_50_talla,
            'p85': percentil_85_talla,
            'p97': percentil_97_talla
        })
    
    def obtener_datos_percentiles(self, tipo):
        """Obtener datos de percentiles según el tipo (peso o talla)"""
        if tipo == 'peso':
            return self.df_peso
        elif tipo == 'talla':
            return self.df_talla
        else:
            raise ValueError("Tipo debe ser 'peso' o 'talla'")
    
    def calcular_percentil(self, tipo, edad, valor):
        """Calcular el percentil aproximado en el que se encuentra el niño"""
        if not (0 <= edad <= 60):
            return "La edad debe estar entre 0 y 60 meses."
        
        df = self.df_peso if tipo == 'peso' else self.df_talla
        valores_percentiles = [df.loc[df['edad_meses'] == edad, p].values[0] 
                              for p in ['p3', 'p15', 'p50', 'p85', 'p97']]
        
        if valor < valores_percentiles[0]:
            return "< 3%"
        elif valor < valores_percentiles[1]:
            return "3-15%"
        elif valor < valores_percentiles[2]:
            return "15-50%"
        elif valor < valores_percentiles[3]:
            return "50-85%"
        elif valor < valores_percentiles[4]:
            return "85-97%"
        else:
            return "> 97%"