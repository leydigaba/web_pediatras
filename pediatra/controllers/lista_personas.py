import web
from models.pediatras import Personas

render = web.template.render("views/")

class ListaPersonas: 
    def GET(self):
        try:
            # Accedemos a la sesión
            session = web.ctx.session  
            usuario = session.get('usuario')

            # Si no hay usuario en sesión, redirige al login
            if not usuario:
                print("🚫 No hay usuario en sesión. Redirigiendo a /iniciosesion...")
                raise web.seeother('/iniciosesion')

            # Si el usuario es admin, redirigirlo a indexadmin
            if usuario.get('rol') == 'admin':
                print("🔄 Usuario administrador detectado. Redirigiendo a /indexadmin...")
                raise web.seeother('/indexadmin')

            print(f"🔍 Usuario autorizado: {usuario['correo']} - Accediendo a ListaPersonas")

            # Recuperamos la lista de pacientes
            p = Personas()  
            pacientes = p.lista_pacientes()

            # Aseguramos que cada paciente tenga datos necesarios
            for id, paciente in pacientes.items():
                paciente.setdefault('estado', 'pendiente')
                if 'edad' in paciente and isinstance(paciente['edad'], (int, float)):
                    paciente['edad'] = f"{paciente['edad']} años"
                paciente.setdefault('ultima_visita', 'Sin registro')

            return render.lista_personas(pacientes)

        except web.seeother as redireccion:
            raise redireccion  # Redirige correctamente sin capturar como error
        except Exception as error:
            print(f"❌ ERROR: {str(error)}")
            return "Ocurrió un error, revisa la consola."
