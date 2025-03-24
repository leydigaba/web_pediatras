import web
from models.pediatras import Personas
import json

# Configuración de plantillas
render = web.template.render("views/")

# Variable global para el mensaje
mensaje = None

class Configuracion:
    def GET(self):
        global mensaje
        try:
            # Verificar sesión de manera segura
            if not hasattr(web.ctx, 'session') or not web.ctx.session.get('usuario'):
                print("🚫 No hay usuario en sesión. Redirigiendo a /iniciosesion...")
                raise web.seeother('/iniciosesion')
            
            # Obtener correo del pediatra desde la sesión
            correo_pediatra = web.ctx.session.usuario.get('correo')
            print(f"📧 Correo del pediatra en sesión: {correo_pediatra}")
            
            # Crear instancia de Personas y obtener datos completos desde Firebase
            p = Personas()
            datos_pediatra = p.obtener_pediatra(correo_pediatra)
            
            if not datos_pediatra:
                print(f"⚠️ No se encontraron datos para el pediatra con correo: {correo_pediatra}")
                # Si no hay datos, usar al menos el correo que tenemos en la sesión
                datos_pediatra = {"correo": correo_pediatra}
            
            # Convertir OrderedDict a diccionario estándar para evitar problemas
            if hasattr(datos_pediatra, 'items'):  # Comprobar si tiene método items() (diccionario u OrderedDict)
                datos_pediatra = dict(datos_pediatra)
            
            print(f"🔍 Datos completos del pediatra (para la vista): {datos_pediatra}")
            print(f"🔍 Tipo de datos: {type(datos_pediatra)}")
            
            # Comprobar si podemos acceder a cada campo específico para debug
            print(f"Nombre: {datos_pediatra.get('nombre', 'NO DISPONIBLE')}")
            print(f"Apellido1: {datos_pediatra.get('apellido1', 'NO DISPONIBLE')}")
            print(f"Correo: {datos_pediatra.get('correo', 'NO DISPONIBLE')}")
            
            # Pasar el mensaje a la plantilla y luego limpiarlo
            mensaje_actual = mensaje
            mensaje = None  # Limpiar el mensaje después de usarlo
            
            # Renderizar la plantilla con los datos completos (diccionario estándar)
            return render.configuracion(datos_pediatra, mensaje=mensaje_actual)
            
        except web.seeother as redireccion:
            raise redireccion
        except Exception as error:
            print(f"❌ ERROR en GET /configuracion: {str(error)}")
            return "Ocurrió un error: " + str(error)

class ActualizarConfiguracion:
    def POST(self):
        global mensaje
        try:
            # Verificar sesión de manera segura
            if not hasattr(web.ctx, 'session') or not web.ctx.session.get('usuario'):
                print("🚫 No hay usuario en sesión. Redirigiendo a /iniciosesion...")
                raise web.seeother('/iniciosesion')
            
            # Obtener datos del formulario
            formulario = web.input()
            
            # Validar campos obligatorios
            if not formulario.get('nombre') or not formulario.get('apellido1') or not formulario.get('correo'):
                mensaje = "Error: Faltan campos obligatorios."
                raise web.seeother('/configuracion')
            
            # Preparar datos para actualizar
            datos_actualizar = {
                'nombre': formulario.get('nombre'),
                'apellido1': formulario.get('apellido1'),
                'apellido2': formulario.get('apellido2', ''),
                'fecha_nacimiento': formulario.get('fecha_nacimiento', ''),
                'licencia': formulario.get('licencia', '')
                # Mantenemos 'rol' y 'uid' sin cambios
            }
            
            # Obtener correo del pediatra (identificador único)
            correo_pediatra = web.ctx.session.usuario.get('correo')
            
            # Actualizar datos en Firebase
            p = Personas()
            resultado = p.actualizar_pediatra(correo_pediatra, datos_actualizar)
            
            if resultado:
                # Obtener datos actualizados desde Firebase
                datos_actualizados = p.obtener_pediatra(correo_pediatra)
                
                # Convertir a diccionario estándar si es necesario
                if datos_actualizados and hasattr(datos_actualizados, 'items'):
                    datos_actualizados = dict(datos_actualizados)
                
                # Actualizar la sesión con TODOS los datos del usuario
                if datos_actualizados:
                    web.ctx.session.usuario = datos_actualizados
                else:
                    # Si fallamos al recuperar los datos actualizados, al menos actualizamos los campos locales
                    for key, value in datos_actualizar.items():
                        web.ctx.session.usuario[key] = value
                
                mensaje = "¡Información actualizada correctamente!"
            else:
                mensaje = "No se pudo actualizar la información. Intente nuevamente."
            
            # Redireccionar de vuelta a configuración
            raise web.seeother('/configuracion')
            
        except web.seeother as redireccion:
            raise redireccion
        except Exception as error:
            print(f"❌ ERROR al actualizar configuración: {str(error)}")
            mensaje = f"Ocurrió un error: {str(error)}"
            raise web.seeother('/configuracion')