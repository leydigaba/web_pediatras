import web
from models.pediatras import Personas 

render = web.template.render("views/")  

class AgregarPersona:
    def GET(self):
        return render.agregar_persona()  # Se debe tener 'views/agregar_persona.html'

    def POST(self):
        datos = web.input()
        nombre = datos.get('nombre', '').strip()
        edad = datos.get('edad', '').strip()

        if not nombre or not edad:
            return "Error: Todos los campos son obligatorios."

        try:
            persona = Personas()  # Instancia de la clase Personas
            persona.agregar_persona(nombre, edad)  # Llama al método para agregar
            return "Persona agregada con éxito"
        except Exception as e:
            return f"Error al agregar la persona: {str(e)}"
