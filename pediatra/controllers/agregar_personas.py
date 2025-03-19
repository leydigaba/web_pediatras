import web
from models.pediatras import Personas  

render = web.template.render("views/")  

class AgregarPersona:
    def GET(self):
        return render.agregar_personas()  

    def POST(self):
        datos = web.input()
        nombre = datos.get('nombre', '').strip()
        edad = datos.get('edad', '').strip()

        if not nombre or not edad:
            return "Error: Todos los campos son obligatorios."

        try:
            edad = int(edad)  
            persona = Personas()  
            persona.agregar_persona(nombre, edad)  
            return web.seeother('/listar_personas')  
        except ValueError:
            return "Error: La edad debe ser un número válido."
        except Exception as e:
            return f"Error al agregar la persona: {str(e)}" 