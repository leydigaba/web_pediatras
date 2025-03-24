import web
import json
from models.pediatras import registrar_administrador  # Importa la función del modelo

class RegistroAdmin:
    def POST(self):
        try:
            datos = web.input()

            # Validar que todos los campos estén completos
            campos_requeridos = ["nombre", "primer-apellido", "segundo-apellido", "telefono", "correo", "rango", "contrasena", "confirmar-contrasena"]
            for campo in campos_requeridos:
                if not datos.get(campo, "").strip():
                    return json.dumps({"status": "error", "message": f"El campo {campo} es obligatorio."})

            # Validar que las contraseñas coincidan
            if datos.contrasena != datos["confirmar-contrasena"]:
                return json.dumps({"status": "error", "message": "Las contraseñas no coinciden."})

            # Intentar registrar al administrador
            resultado = registrar_administrador(
                datos.nombre.strip(),
                datos["primer-apellido"].strip(),
                datos["segundo-apellido"].strip(),
                datos.telefono.strip(),
                datos.correo.strip(),
                datos.rango.strip(),
                datos.contrasena.strip()
            )

            # Responder según el resultado
            if resultado:
                return json.dumps({"status": "success", "message": "Administrador registrado correctamente."})
            else:
                return json.dumps({"status": "error", "message": "No se pudo registrar el administrador. Intenta de nuevo."})

        except Exception as e:
            return json.dumps({"status": "error", "message": f"Error inesperado: {str(e)}"})