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