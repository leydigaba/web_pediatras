import web
from models.pediatras import Personas, firebase

db = firebase.database()

render = web.template.render("views/")

class AgregarPaciente:
    def GET(self):
        try:
            # Verificamos si la sesión está iniciada
            session = web.ctx.session
            if not session.get('usuario'):
                print("🚫 No hay usuario en sesión. Redirigiendo a /iniciosesion...")
                raise web.seeother('/iniciosesion')
                
            return render.agregar_personas()
        except web.seeother as redireccion:
            raise redireccion
        except Exception as error:
            print(f"❌ ERROR: {str(error)}")
            return "Ocurrió un error, revisa la consola."
    
    def POST(self):
        try:
            # Verificamos si la sesión está iniciada
            session = web.ctx.session
            if not session.get('usuario'):
                print("🚫 No hay usuario en sesión. Redirigiendo a /iniciosesion...")
                raise web.seeother('/iniciosesion')
                
            datos = web.input()
            
            campos_obligatorios = [
                "nombre", "primer_apellido", "segundo_apellido", 
                "edad", "genero", "telefono",
                "nombre_madre", "direccion"
            ]
            
            for campo in campos_obligatorios:
                if campo not in datos or datos[campo].strip() == "":
                    print(f"Campo faltante o vacío: {campo}")
                    return "Error: Todos los campos son obligatorios."
            
            # Obtenemos el correo del pediatra de la sesión
            correo_pediatra = session.get('usuario').get('correo')
            
            paciente = {
                "nombre": datos.nombre,
                "primer_apellido": datos.primer_apellido,
                "segundo_apellido": datos.segundo_apellido,
                "edad": datos.edad,
                "genero": datos.genero,
                "telefono": datos.telefono,
                "nombre_madre": datos.nombre_madre,
                "nombre_padre": datos.get("nombre_padre", "No especificado"),
                "direccion": datos.direccion,
                "fecha_registro": db.generate_key(),
                "pediatra": correo_pediatra  # Añadimos el correo del pediatra
            }
            
            print("Datos del paciente a guardar:", paciente)
            
            resultado = db.child("pacientes").push(paciente)
            print("Paciente guardado con éxito:", resultado)
            raise web.seeother('/listapersonas')
            
        except web.seeother as redireccion:
            raise redireccion
        except Exception as e:
            print(f"Error al agregar paciente: {str(e)}")
            return f"Error al agregar paciente: {str(e)}"