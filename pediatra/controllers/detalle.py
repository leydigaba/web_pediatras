import web
import json
from models.pediatras import Personas

render = web.template.render("views/")

class DetalleUsuario:
    def GET(self, paciente_id):
        try:
            session = web.ctx.session
            if not session.get('usuario'):
                print("🚫 No hay usuario en sesión. Redirigiendo a /iniciosesion...")
                raise web.seeother('/iniciosesion')

            correo_pediatra = session.get('usuario').get('correo')
            personas = Personas()
            paciente = personas.lista_pacientes_por_id_y_pediatra(paciente_id, correo_pediatra)
            print("Paciente obtenido:", paciente)

            # Verificar si el paciente existe
            if paciente and paciente.get(paciente_id):
                return render.detalle_personas(paciente)  # Mostrar los detalles del paciente
            else:
                return "No tienes acceso a este paciente"
        except web.seeother as redireccion:
            raise redireccion
        except Exception as e:
            print("Error en GET de DetalleUsuario:", str(e))
            return "Error al obtener los datos"

    def POST(self, paciente_id):
        print(f"POST iniciado con paciente_id: '{paciente_id}'")
        try:
            # Verificar si la sesión está iniciada
            session = web.ctx.session
            if not session.get('usuario'):
                print("🚫 No hay usuario en sesión. Redirigiendo a /iniciosesion...")
                return json.dumps({"error": "No hay sesión iniciada"})

            datos = web.input()
            correo_pediatra = session.get('usuario').get('correo')
            personas = Personas()

            paciente = personas.lista_pacientes_por_id_y_pediatra(paciente_id, correo_pediatra)
            if not paciente or not paciente.get(paciente_id):
                return json.dumps({"error": "No tienes acceso a este paciente"})

            datos_actualizar = {
                'nombre': datos.get('nombre'),
                'primer_apellido': datos.get('apellido1'),
                'segundo_apellido': datos.get('apellido2'),
                'fecha_nacimiento': datos.get('fecha_nacimiento'),
                'edad': datos.get('edad'),
                'curp': datos.get('curp'),
                'genero': datos.get('genero'),
                'nombre_madre': datos.get('nombre_madre'),
                'nombre_padre': datos.get('nombre_padre'),
                'telefono': datos.get('telefono'),
                'direccion': datos.get('direccion'),
                'peso': datos.get('peso'),
                'talla': datos.get('talla'),
                'perimetro_cefalico': datos.get('perimetro_cefalico'),
                'grupo_sanguineo': datos.get('grupo_sanguineo'),
                'antecedente_neonatal': datos.get('antecedente_neonatal'),
                'antecedente_neonatal_si': datos.get('antecedente_neonatal_si'),
                'antecedente_neonatal_no': datos.get('antecedente_neonatal_no'),
                'edad_neonatal_semanas': datos.get('edad_neonatal_semanas'),
                'edad_neonatal_dias': datos.get('edad_neonatal_dias'),
                'peso_datos': datos.get('peso_datos'),
                'talla_datos': datos.get('talla_datos'),
                'patologias': datos.get('patologias'),
                'alergias': datos.get('alergias'),  # ← Se agregó la coma faltante
                'patologias_si': datos.get('patologias_si'),
                'patologias_no': datos.get('patologias_no'),
                'gestas': datos.get('gestas'),
                'abortos': datos.get('abortos'),
                'partos': datos.get('partos'),
                'cesareas': datos.get('cesareas'),
                'normal': datos.get('normal'),
                'riesgo': datos.get('riesgo'),
                'espontaneo': datos.get('espontaneo'),
                'intraoperatoria': datos.get('intraoperatoria'),
                'electiva': datos.get('electiva')
            }

            # Filtrar solo los valores que no son None o cadenas vacías
            datos_actualizar = {k: v for k, v in datos_actualizar.items() if v}

            resultado = personas.actualizar_paciente(paciente_id, datos_actualizar)

            if resultado:
                return json.dumps({"success": True, "mensaje": "Datos actualizados correctamente"})
            else:
                return json.dumps({"success": False, "error": "Error al actualizar los datos"})

        except Exception as e:
            print("Error en POST de DetalleUsuario:", str(e))
            return json.dumps({"success": False, "error": str(e)})
