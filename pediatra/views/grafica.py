import dash
from dash import dcc, html, callback, Input, Output
from controllers import CrecimientoInfantilControlador

class CrecimientoInfantilVista:
    def __init__(self):
        self.app = dash.Dash(__name__)
        self.controlador = CrecimientoInfantilControlador()
        self._configurar_layout()
        self._configurar_callbacks()
    
    def _configurar_layout(self):
        """Configurar el layout de la aplicación Dash"""
        self.app.layout = html.Div([
            html.H1("Gráfica de Percentiles de Crecimiento Infantil (0-5 años)", 
                   style={'textAlign': 'center'}),
            
            html.Div([
                html.Div([
                    html.Label("Seleccione el tipo de gráfica:"),
                    dcc.RadioItems(
                        id='tipo-grafica',
                        options=[
                            {'label': 'Peso para Edad', 'value': 'peso'},
                            {'label': 'Talla para Edad', 'value': 'talla'}
                        ],
                        value='peso',
                        labelStyle={'display': 'block'}
                    ),
                ], style={'width': '30%', 'display': 'inline-block'}),
                
                html.Div([
                    html.Label("Datos del Niño"),
                    html.Div([
                        html.Label("Edad (meses):"),
                        dcc.Input(id='edad-input', type='number', min=0, max=60, value=12),
                        html.Label("Peso (kg):"),
                        dcc.Input(id='peso-input', type='number', min=0, max=30, value=9.5),
                        html.Label("Talla (cm):"),
                        dcc.Input(id='talla-input', type='number', min=30, max=120, value=75),
                    ]),
                ], style={'width': '30%', 'display': 'inline-block'}),
                
                html.Div([
                    html.Label("Resultado:"),
                    html.Div(id='resultado-calculo'),
                ], style={'width': '30%', 'display': 'inline-block'}),
            ]),
            
            dcc.Graph(id='grafica-percentiles'),
            
            html.Div([
                html.P("Nota: Esta es una aproximación basada en los estándares de la OMS. "
                      "Para evaluaciones clínicas, consulte con un profesional de la salud."),
            ], style={'marginTop': '20px', 'textAlign': 'center'}),
        ])
    
    def _configurar_callbacks(self):
        """Configurar los callbacks de la aplicación Dash"""
        @self.app.callback(
            [Output('grafica-percentiles', 'figure'),
             Output('resultado-calculo', 'children')],
            [Input('tipo-grafica', 'value'),
             Input('edad-input', 'value'),
             Input('peso-input', 'value'),
             Input('talla-input', 'value')]
        )
        def update_graph(tipo_grafica, edad, peso, talla):
            valor_actual = peso if tipo_grafica == 'peso' else talla
            
            # Obtener la gráfica y el percentil del controlador
            fig, percentil_estimado = self.controlador.generar_grafica(tipo_grafica, edad, valor_actual)
            
            # Formatear el resultado
            unidad = 'kg' if tipo_grafica == 'peso' else 'cm'
            resultado = html.Div([
                html.P(f"Edad: {edad} meses"),
                html.P(f"{tipo_grafica.capitalize()}: {valor_actual} {unidad}"),
                html.P(f"Percentil aproximado: {percentil_estimado}"),
            ])
            
            return fig, resultado
    
    def ejecutar(self):
        """Ejecutar la aplicación"""
        self.app.run_server(debug=True)
