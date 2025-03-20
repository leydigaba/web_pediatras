import web

render = web.template.render('views/admins', base="../master1")

class VistaPacientes:
    def GET(self):
        try: 
            return render.vistapacientes()  # Asegúrate de que index.html existe
        except Exception as error:
            message = {
                "error": error.args[0] }
            print(f"ERROR: {message}")
            return message