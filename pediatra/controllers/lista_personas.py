import web
from models.pediatras import Personas
render = web.template.render("views/")

class ListaPersonas: 
    def GET(self):
        try:
            # Primero verificamos si web.ctx tiene una sesión
            if not hasattr(web.ctx, 'session') or not web.ctx.session.get('usuario'):
                # Limpiar la sesión si no hay usuario
                print("🚫 No hay usuario en sesión. Limpiando sesión y redirigiendo a /iniciosesion...")
                if hasattr(web.ctx, 'session'):
                    web.ctx.session.kill()  # Limpia la sesión actual
                return web.seeother('/iniciosesion')

            print(f"🔍 Sesión actual: {web.ctx.session.get('usuario')}")  # Ahora sí podemos imprimir la sesión

            p = Personas()  
            datos = p.lista_personas()  
            return render.lista_personas(datos)  
        except Exception as error:
            print(f"❌ ERROR: {str(error)}")
            return "Ocurrió un error, revisa la consola."