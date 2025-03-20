import web
from models.pediatras import Personas
render = web.template.render("views/")

class ListaPersonas: 
    def GET(self):
        try:
            # Verificamos si web.ctx tiene una sesión
            if not hasattr(web.ctx, 'session') or not web.ctx.session.get('usuario'):
                print("🚫 No hay usuario en sesión. Redirigiendo a /iniciosesion...")
                return web.seeother('/iniciosesion')

            print(f"🔍 Sesión actual: {web.ctx.session.get('usuario')}")

            p = Personas()  
            # Obtenemos la lista de pacientes
            pacientes = p.lista_pacientes()  
            
            # Procesamos los datos para asegurarnos de que tengan las propiedades necesarias
            for id, paciente in pacientes.items():
                # Establecemos valores por defecto si no existen
                if 'estado' not in paciente:
                    paciente['estado'] = 'pendiente'
                    
                # Aseguramos que la edad tenga el formato correcto
                if 'edad' in paciente and isinstance(paciente['edad'], (int, float)):
                    paciente['edad'] = f"{paciente['edad']} años"
                    
                # Agregamos una fecha de última visita si no existe
                if 'ultima_visita' not in paciente:
                    paciente['ultima_visita'] = 'Sin registro'
            
            return render.lista_personas(pacientes)
        except Exception as error:
            print(f"❌ ERROR: {str(error)}")
            return "Ocurrió un error, revisa la consola."