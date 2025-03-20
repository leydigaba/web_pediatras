import plotly.graph_objects as go
from models.pediatras import CrecimientoInfantilModelo

render = web.template.render("views/")  

class CrecimientoInfantilControlador:
    def __init__(self):
        self.modelo = CrecimientoInfantilModelo()
    
    def generar_grafica(self, tipo_grafica, edad, valor):
        """Generar gráfica de percentiles y calcular resultados"""
        df = self.modelo.obtener_datos_percentiles(tipo_grafica)
        unidad = 'kg' if tipo_grafica == 'peso' else 'cm'
        titulo = f'Percentiles de {"Peso" if tipo_grafica == "peso" else "Talla"} para Edad (0-5 años)'
        
        # Crear figura
        fig = go.Figure()
        
        # Añadir las líneas de percentiles
        for percentil, nombre in zip(['p3', 'p15', 'p50', 'p85', 'p97'], ['3%', '15%', '50%', '85%', '97%']):
            fig.add_trace(go.Scatter(
                x=df['edad_meses'],
                y=df[percentil],
                mode='lines',
                name=f'Percentil {nombre}',
                line=dict(width=2)
            ))
        
        # Añadir el punto del niño si la edad está dentro del rango
        if 0 <= edad <= 60:
            fig.add_trace(go.Scatter(
                x=[edad],
                y=[valor],
                mode='markers',
                name='Niño',
                marker=dict(size=12, color='red')
            ))
        
        # Configuración de la gráfica
        fig.update_layout(
            title=titulo,
            xaxis_title='Edad (meses)',
            yaxis_title=f'{"Peso" if tipo_grafica == "peso" else "Talla"} ({unidad})',
            legend_title='Percentiles',
            hovermode='closest'
        )
        
        # Calcular el percentil aproximado
        percentil_estimado = self.modelo.calcular_percentil(tipo_grafica, edad, valor)
        
        return fig, percentil_estimado