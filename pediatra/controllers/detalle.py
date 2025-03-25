import web
import json
from models.pediatras import Personas

# Renderizar las vistas desde la carpeta "views"
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
            paciente = personas.lista_pacientes_por_id_y_pediatra(paciente_id,correo_pediatra)
            print("Paciente obtenido:", paciente)
            
            # Verificar si el paciente existe
            if paciente and paciente.get(paciente_id):
         
                return render.detalle_personas(paciente)  # Mostrar los detalles del paciente
            else:
                return "No tienes acceso a este paciente"
        except web.seeother as redireccion:
            raise redireccion

    def POST(self, paciente_id):
            print(f"POST iniciado con paciente_id: '{paciente_id}'")
            try:class ActualizarFotoPaciente:
    def POST(self):
        try:
            session = web.ctx.session
            if not session.get('usuario'):
                return json.dumps({"error": "No hay sesión iniciada"})

            datos = web.input(foto={})
            correo_pediatra = session.get('usuario').get('correo')
            
            # Verificar si se subió un archivo
            if datos.foto.filename:
                # Generar nombre de archivo único
                filename = f"{str(uuid.uuid4())}_{datos.foto.filename}"
                upload_path = os.path.join('static/uploads', filename)
                
                # Crear directorio si no existe
                os.makedirs('static/uploads', exist_ok=True)
                
                # Guardar archivo
                with open(upload_path, 'wb') as f:
                    f.write(datos.foto.file.read())
                
                # Actualizar en base de datos
                personas = Personas()
                
                # Aquí necesitas obtener el ID del paciente 
                # Por ejemplo, podría venir de un campo oculto en el formulario
                paciente_id = datos.get('paciente_id')  
                
                resultado = personas.actualizar_foto_paciente(paciente_id, f"/static/uploads/{filename}")
                
                if resultado:
                    return json.dumps({"success": True, "foto": f"/static/uploads/{filename}"})
                else:
                    return json.dumps({"error": "No se pudo actualizar la foto"})
            
            return json.dumps({"error": "No se recibió ningún archivo"})
        
        except Exception as e:
            print(f"Error en actualizar foto: {str(e)}")
            return json.dumps({"error": str(e)})

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
                    'antecedente_neonatal_si': datos.get('antecedente_neonatal_si'),
                    'antecedente_neonatal_no': datos.get('antecedente_neonatal_no'),
                    'edad_neonatal_semanas': datos.get('edad_neonatal_semanas'),
                    'edad_neonatal_dias': datos.get('edad_neonatal_dias'),
                    'peso_datos': datos.get('peso_datos'),
                    'talla_datos': datos.get('talla_datos'),
                    'patologias_si': datos.get('patologias_si'),
                    'patologias_no': datos.get('patologias_no'),
                    'gestas': datos.get('gestas'),
                    'abortos': datos.get('abortos'),
                    'partos': datos.get('partos'),
                    'cesareas': datos.get('cesareas'),
                    'normal': datos.get('normal'),
                    'riesgo': datos.get('riesgo'), 
                    'alto_riesgo': datos.get('alto_riesgo'),
                    'terminacion': datos.get('terminacion')
                    
                }
                
                datos_actualizar = {k: v for k, v in datos_actualizar.items() if v}
                resultado = personas.actualizar_paciente(paciente_id, datos_actualizar)
                
                if resultado:
                    return json.dumps({"success": True, "mensaje": "Datos actualizados correctamente"})
                else:
                    return json.dumps({"success": False, "error": "Error al actualizar los datos"})
                    
            except Exception as e:
                print("Error en POST de DetalleUsuario:", str(e))
                return json.dumps({"success": False, "error": str(e)})

