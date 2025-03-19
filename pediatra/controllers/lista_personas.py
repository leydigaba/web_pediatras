import web
from models.pediatras import Personas
render = web.template.render("views/")

class ListaPersonas:
    def GET(self):
        try:
            p = Personas()  # Instancia del modelo
            datos = p.lista_personas()  # Obtiene los datos
            return render.lista_personas(datos)  # Renderiza la vista con los datos
        except Exception as error:
            message = {"Error": str(error)}
            print(f"ERROR: {message}")  
            return "Ocurrió un error, revisa la consola."
