import web
from models.pediatras import Personas, firebase


db = firebase.database()


render = web.template.render("views/")

class AgregarPaciente:
    def GET(self):
        return render.agregar_personas()
    
    def POST(self):
        try:
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
                "fecha_registro": db.generate_key()
            }
            
            print("Datos del paciente a guardar:", paciente)
        
            resultado = db.child("pacientes").push(paciente)
            print("Paciente guardado con éxito:", resultado)
            raise web.seeother('/listapersonas')
            
        except Exception as e:
            print(f"Error al agregar paciente: {str(e)}")
            return f"Error al agregar paciente: {str(e)}"