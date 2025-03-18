import web
from controllers.index import Index  
from controllers.registro import Registro as Registro
from controllers.iniciosesion import Iniciosesion as Iniciosesion
from controllers.pacientes import ListaPersonas as ListaPersonas



urls = (
    "/", "Index",
    "/registro", "Registro",
    "/iniciosesion", "Iniciosesion",
    "/listapersonas", "Listapersonas",
    
)

app = web.application(urls, globals())


def error_handler():
    return web.internalerror("Ocurrió un error en el servidor. Intenta nuevamente.")

if __name__ == "__main__":
    app.run()
