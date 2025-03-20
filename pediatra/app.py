import web
from controllers.index import Index  
from controllers.registro import Registro as Registro
from controllers.iniciosesion import Iniciosesion as Iniciosesion
from controllers.lista_personas import ListaPersonas as ListaPersonas
from controllers.agregar_personas import AgregarPaciente as AgregarPaciente
from controllers.cerrarsesion import Logout as Logout
from controllers.indexadmin import IndexAdmin
from controllers.admins.vistaadmins import VistaAdmins
from controllers.admins.vistapediatras import VistaPediatras
from controllers.admins.vistapacientes import VistaPacientes
from controllers.admins.vistarespuestas import VistaRespuestas
from controllers.admins.vistareportes import VistaReportes


web.config.debug = False  

# Definir rutas
urls = (
    '/', 'Index',
    '/registro', 'Registro',
    '/iniciosesion', 'Iniciosesion',
    '/listapersonas', 'ListaPersonas',
    '/agregar', 'AgregarPaciente',
    '/logout', 'Logout',
    '/indexadmin', 'IndexAdmin',
    '/vistaadmins', 'VistaAdmins',
    '/vistapediatras', 'VistaPediatras',
    '/vistapacientes', 'VistaPacientes',
    '/vistarespuestas', 'VistaRespuestas',
    '/vistareportes', 'VistaReportes'
)

app = web.application(urls, globals())

# 📌 Asegurar que la sesión esté configurada correctamente
if web.config.get('_session') is None:  # Evitar que la sesión se reinicialice en cada request
    session = web.session.Session(app, web.session.DiskStore("sessions"), initializer={"usuario": None})
    web.config._session = session  # Guardar la sesión en web.config

# 📌 Hacer que session sea accesible globalmente
def session_hook():
    web.ctx.session = web.config._session

app.add_processor(web.loadhook(session_hook))
if __name__ == "__main__":
    app.run()