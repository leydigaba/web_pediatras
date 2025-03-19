import web
from models.pediatras import Personas  

render = web.template.render("views/")  

class AgregarPersona:
    def GET(self):
        return render.agregar_persona()  

    def POST(self):
        datos = web.input()
        nombre = datos.get('nombre', '').strip()
        edad = datos.get('edad', '').strip()

        # Validación de datos
        if not nombre or not edad:
            return "Error: Todos los campos son obligatorios."

        try:
            edad = int(edad)  # Convertir a número
            persona = Personas()  
            persona.agregar_persona(nombre, edad)  

            # Redirigir a la lista de personas o página principal
            return web.seeother('/')  
        except ValueError:
            return "Error: La edad debe ser un número válido."
        except Exception as e:
            return f"Error al agregar la persona: {str(e)}"