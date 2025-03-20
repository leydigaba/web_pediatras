import web

render = web.template.render('views/admins', base="../master1")

class VistaAdmins:
    def GET(self):
        try: 
            return render.vistaadmins()  # Asegúrate de que index.html existe
        except Exception as error:
            message = {
                "error": error.args[0] }
            print(f"ERROR: {message}")
            return message