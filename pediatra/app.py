#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import web
from controllers.index import Index  
from controllers.registro import Registro as Registro
from controllers.iniciosesion import Iniciosesion as Iniciosesion
from controllers.lista_personas import ListaPersonas as ListaPersonas
from controllers.agregar_personas import AgregarPaciente as AgregarPaciente
from controllers.detalle import DetalleUsuario as DetalleUsuario
#from controllers.detalle import ActualizarFotoBebe as ActualizarFotoBebe
from controllers.cerrarsesion import Logout as Logout
from controllers.estadistica_personas import EstadisticaUsuario as EstadisticaUsuario
from controllers.configuracion import Configuracion as Configuracion
from controllers.configuracion import ActualizarConfiguracion as ActualizarConfiguracion
from controllers.configuracion import ActualizarFoto as ActualizarFoto

from controllers.ficha import DetallePersonas as DetallePersonas

web.config.debug = False  

# Definir rutas
urls = (
    '/', 'Index',
    '/registro', 'Registro',
    '/iniciosesion', 'Iniciosesion',
    '/listapersonas', 'ListaPersonas',
    '/agregar', 'AgregarPaciente',
    '/usuario/(.+)', 'DetalleUsuario',
    '/logout', 'Logout',
    '/estadisticas', 'EstadisticaUsuario',
    '/configuracion', 'Configuracion',
    '/actualizar_configuracion', 'ActualizarConfiguracion',
    '/consulta', 'Consulta',
    '/cambiar_estado/(.*)', 'CambiarEstado',
    '/credencial/(.*)', 'DetallePersonas',
    '/actualizar_foto', 'ActualizarFoto',
    '/detalle_paciente/(.+)/actualizar_foto', 'ActualizarFotoBebe',
    '/actualizar_foto_paciente', 'ActualizarFotoBebe'

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