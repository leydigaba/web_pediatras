import web

render = web.template.render('views/')

class IndexAdmin:
    def GET(self):
        try: 
            session = web.ctx.session  # Acceder a la sesión

            # Verificar si hay usuario en sesión y si es administrador
            usuario = session.get('usuario')
            if not usuario:
                print("🚫 No hay usuario en sesión. Redirigiendo a /iniciosesion...")
                raise web.seeother('/iniciosesion')
            
            if usuario.get('rol') != 'admin':  
                print("🚫 Acceso denegado. Redirigiendo a /listapersonas...")
                raise web.seeother('/listapersonas')

            print(f"✅ Acceso permitido a {usuario.get('correo')} con rol {usuario.get('rol')}")
            return render.indexadmin()
            
        except web.seeother as redireccion:
            raise redireccion  # Permite la redirección sin ser capturada como error
        except Exception as error:
            print(f"❌ ERROR: {str(error)}")
            return "Ocurrió un error, revisa la consola."
