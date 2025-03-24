import web

render = web.template.render('views/admins', base="../master1")

class VistaRespuestas:
    def GET(self):
        try: 
            return render.vistarespuestas() 
        except Exception as error:
            message = {
                "error": error.args[0] }
            print(f"ERROR: {message}")
            return message