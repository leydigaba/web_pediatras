import web
from controllers.index import Index  
from controllers.registro import Registro as Registro



urls = (
    "/", "Index",
    "/registro", "Registro",
    '/exito', 'Exito'
)

# Clase para la página de éxito
class Exito:
    def GET(self):
        return """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Registro Exitoso</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    background-color: #f4f4f4;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    height: 100vh;
                    margin: 0;
                }
                .container {
                    background: white;
                    padding: 20px;
                    border-radius: 10px;
                    box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1);
                    width: 350px;
                    text-align: center;
                }
                h2 {
                    color: #4CAF50;
                }
                .btn {
                    background-color: #007BFF;
                    color: white;
                    border: none;
                    padding: 10px;
                    border-radius: 5px;
                    text-decoration: none;
                    display: inline-block;
                    margin-top: 15px;
                }
            </style>
        </head>
        <body>
            <div class="container">
                <h2>¡Registro Exitoso!</h2>
                <p>Tu cuenta ha sido creada correctamente.</p>
                <a href="/login" class="btn">Iniciar Sesión</a>
            </div>
        </body>
        </html>
        """
app = web.application(urls, globals())


# Manejo de errores
def error_handler():
    return web.internalerror("Ocurrió un error en el servidor. Intenta nuevamente.")

if __name__ == "__main__":
    app.run()
