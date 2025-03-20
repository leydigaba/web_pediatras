import web
from models.pediatras import iniciar_sesion
render = web.template.render("views/")

class Iniciosesion:
    def GET(self):
        return render.iniciosesion(datos={})  

    def POST(self):
        try:
            datos = web.input()
            correo = datos.correo
            password = datos.password

            print(f"Intentando iniciar sesión con: {correo}")  

            usuario = iniciar_sesion(correo, password)

            print(f"Resultado de iniciar_sesion: {usuario}")  

            if usuario:
                session = web.ctx.session  # Acceder a la sesión
                session.usuario = usuario  # Guardar el usuario en sesión
                print("✅ Sesión iniciada correctamente.")

                # Redirigir según el rol del usuario
                if usuario.get("rol") == "admin":
                    return web.seeother("/indexadmin")
                else:
                    return web.seeother("/listapersonas")
            else:
                print("❌ Credenciales incorrectas")  
                return render.iniciosesion(datos={"error": "Correo o contraseña incorrectos."})

        except Exception as e:
            print(f"⚠️ Error en inicio de sesión: {str(e)}")  
            return render.iniciosesion(datos={"error": str(e)})
