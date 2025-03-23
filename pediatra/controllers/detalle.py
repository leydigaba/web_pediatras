import web
import json
from models.pediatras import Personas

# Renderizar las vistas desde la carpeta "views"
render = web.template.render("views/")

class DetalleUsuario:
    def GET(self, paciente_id):
        try:
            # Verificar si la sesión está iniciada
            session = web.ctx.session
            if not session.get('usuario'):
                print("🚫 No hay usuario en sesión. Redirigiendo a /iniciosesion...")
                raise web.seeother('/iniciosesion')

            correo_pediatra = session.get('usuario').get('correo')
            personas = Personas()

            # Obtener el paciente por su ID utilizando el método de la clase Personas
            paciente = personas.lista_pacientes_por_id_y_pediatra(paciente_id,correo_pediatra)
            print("Paciente obtenido:", paciente)
            
            # Verificar si el paciente existe
            if paciente and paciente.get(paciente_id):
         
                return render.detalle_personas(paciente)  # Mostrar los detalles del paciente
            else:
                return "No tienes acceso a este paciente"
        except web.seeother as redireccion:
            raise redireccion


    def POST(self, paciente_id):
            print(f"POST iniciado con paciente_id: '{paciente_id}'")
            try:
                # Verificar si la sesión está iniciada
                session = web.ctx.session
                if not session.get('usuario'):
                    print("🚫 No hay usuario en sesión. Redirigiendo a /iniciosesion...")
                    return json.dumps({"error": "No hay sesión iniciada"})

                # Obtener los datos del formulario
                datos = web.input()
                correo_pediatra = session.get('usuario').get('correo')
                personas = Personas()
                
                paciente = personas.lista_pacientes_por_id_y_pediatra(paciente_id, correo_pediatra)
                if not paciente or not paciente.get(paciente_id):
                    return json.dumps({"error": "No tienes acceso a este paciente"})
                
                # Preparar los datos a actualizar
                datos_actualizar = {
                    'nombre': datos.get('nombre'),
                    'primer_apellido': datos.get('apellido1'),
                    'segundo_apellido': datos.get('apellido2'),
                    'fecha_nacimiento': datos.get('fecha_nacimiento'),
                    'edad': datos.get('edad'),
                    'curp': datos.get('curp'),
                    'genero': datos.get('genero'),
                    'nombre_madre': datos.get('nombre_madre'),
                    'nombre_padre': datos.get('nombre_padre'),
                    'telefono': datos.get('telefono'),
                    'direccion': datos.get('direccion'),
                    'peso': datos.get('peso'),
                    'talla': datos.get('talla'),
                    'perimetro_cefalico': datos.get('perimetro_cefalico'),
                    'grupo_sanguineo': datos.get('grupo_sanguineo')
                }
                
                # Filtrar campos vacíos
                datos_actualizar = {k: v for k, v in datos_actualizar.items() if v}
                
                # Actualizar los datos del paciente
                resultado = personas.actualizar_paciente(paciente_id, datos_actualizar)
                
                if resultado:
                    return json.dumps({"success": True, "mensaje": "Datos actualizados correctamente"})
                else:
                    return json.dumps({"success": False, "error": "Error al actualizar los datos"})
                    
            except Exception as e:
                print("Error en POST de DetalleUsuario:", str(e))
                return json.dumps({"success": False, "error": str(e)})
