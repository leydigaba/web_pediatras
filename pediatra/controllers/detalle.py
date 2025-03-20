import web
from models.pediatras import Personas  

render = web.template.render("views/")

class DetalleUsuario:
    def GET(self, usuario_id):
        personas = Personas()  
        persona = p.lista_pacientes().get(persona_id)
        if persona:
            return render.detalle_personas(persona_id, persona)
        else:
            return "Persona no encontrada"

