import web
from models.pediatras import Personas
render = web.template.render("views/")

class ListaPersonas:
    def GET(self):
        try:
            p = Personas()  
            datos = p.lista_personas()  
            return render.lista_personas(datos)  
        except Exception as error:
            print(f" ERROR: {str(error)}")
            return "Ocurrió un error, revisa la consola."