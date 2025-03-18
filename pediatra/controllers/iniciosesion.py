import web
from models.pediatras import iniciar_sesion 
render = web.template.render("views/")

class Iniciosesion:
    def GET(self):
        return render.iniciosesion()  
    
    def POST(self):
        try:
            datos = web.input()
            correo = datos.correo
            password = datos.password

            usuario = iniciar_sesion(correo, password)

            if usuario:
                return f"Bienvenido, {usuario['nombre']}!"
            else:
                return render.iniciosesion(error="⚠️ Correo o contraseña incorrectos.") 
        
        except Exception as e:
            error_msg = f"❌ Error en inicio de sesión: {str(e)}"
            print(error_msg)  
            return render.iniciosesion(error=error_msg) 