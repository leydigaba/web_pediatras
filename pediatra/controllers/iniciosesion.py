import web
from models.pediatras import iniciar_sesion 
render = web.template.render("views/")


class Iniciosesion:
    def GET(self):
        return render.iniciosesion(datos={})  # Aseguramos que 'datos' se pase vacío

    def POST(self):
        try:
            datos = web.input()
            correo = datos.correo
            password = datos.password

            print(f"Intentando iniciar sesión con: {correo}")  

            usuario = iniciar_sesion(correo, password)

            print(f"Resultado de iniciar_sesion: {usuario}")  

            if usuario:
                web.ctx.session.usuario = usuario  
                print("Redireccionando a /listapersonas")  
                return web.seeother("/listapersonas")
            else:
                print("Credenciales incorrectas")  
                return render.iniciosesion(datos={"error": "Correo o contraseña incorrectos."})

        except Exception as e:
            error_msg = f"Error en inicio de sesión: {str(e)}"
            print(error_msg)  
            return render.iniciosesion(datos={"error": error_msg})