import web
from models.pediatras import Personas

render = web.template.render("views/personas", base="master")



class DetallePersonas:
    def GET(self, persona_id):
        p = Personas()
        print(f"Buscando persona con ID: {persona_id}")  # Depuración
        persona = p.lista_personas().get(persona_id)
        if persona:
            return render.detalle_personas(persona_id, persona)
        else:
            return f"Persona con ID {persona_id} no encontrada"