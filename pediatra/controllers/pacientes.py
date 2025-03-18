import web

from models.pediatras import iniciar_sesion 
render = web.template.render("views/", base="master")

class ListaPersonas:
    def GET(self):
        try:
            p = Personas() 
            datos = p.lista_personas() 
            return render.lista_personas(datos) 
        except Exception as error:
            message = {
                "Error": str(error)  
            }
            print(f"ERROR: {message}")  
            return message