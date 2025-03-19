import web
from controllers.index import Index  
from controllers.registro import Registro as Registro
from controllers.iniciosesion import Iniciosesion as Iniciosesion
from controllers.lista_personas import ListaPersonas as ListaPersonas
from controllers.agregar_personas import AgregarPersona as AgregarPersona



web.config.debug = False  

# Definir rutas
urls = (
    '/', 'Index',
    '/registro', 'Registro',
    '/iniciosesion', 'Iniciosesion',
    '/listapersonas', 'ListaPersonas',
    '/agregar', 'AgregarPersona'  
)

app = web.application(urls, globals())

# 🔹 Configuración de sesión
session_store = web.session.DiskStore("sessions")
session = web.session.Session(app, session_store, initializer={"usuario": None})

def session_hook():
    """Asigna la sesión al contexto de la aplicación."""
    web.ctx.session = session  

app.add_processor(web.loadhook(session_hook))

# 🔹 Protección de rutas con sesión
def auth_hook():
    rutas_protegidas = ["/listapersonas", "/agregar"]  
    usuario_en_sesion = web.ctx.session.get("usuario") 

    print(f"🟡 Usuario en sesión: {usuario_en_sesion}")  # Para depuración

    if web.ctx.path in rutas_protegidas and not usuario_en_sesion:
        print(f"🔴 Acceso denegado a {web.ctx.path}: Usuario no autenticado.")
        return web.seeother("/iniciosesion")  # Redirige al login

app.add_processor(web.loadhook(auth_hook))

if __name__ == "__main__":
    app.run()