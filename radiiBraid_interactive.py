import numpy as np
import plotly.graph_objects as go
import dash
from dash import dcc, html, Input, Output, State, callback
import dash_bootstrap_components as dbc

# Initialize the Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

# App layout
app.layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.H1("Interactive Fibre Angle Calculator", className="mt-4 mb-4")
        ])
    ]),
    
    dbc.Row([
        dbc.Col([
            html.H5("Number of Horn Gears"),
            dcc.Slider(
                id='n-slider',
                min=1,
                max=192,
                step=1,
                value=192,
                marks={i: f'{i}' for i in range(0, 193, 48)},
                tooltip={"placement": "bottom", "always_visible": True}
            ),
            dbc.Input(
                id='n-input',
                type='number',
                placeholder='Enter value',
                value=192,
                min=1,
                max=192,
                step=1,
                n_submit=0,
                className="mt-2"
            ),
        ], md=12),
    ], className="mb-3 p-4 border rounded bg-light"),
    
    dbc.Row([
        dbc.Col([
            html.H5("Mandrel Diameter (mm)"),
            dcc.Slider(
                id='dm-slider',
                min=1,
                max=1000,
                step=1,
                value=100,
                marks={i: f'{i}' for i in range(0, 1001, 250)},
                tooltip={"placement": "bottom", "always_visible": True}
            ),
            dbc.Input(
                id='dm-input',
                type='number',
                placeholder='Enter value',
                value=100,
                min=1,
                max=1000,
                step=1,
                n_submit=0,
                className="mt-2"
            ),
        ], md=4),
        
        dbc.Col([
            html.H5("Horn Gear Speed (RPM)"),
            dcc.Slider(
                id='hgs-slider',
                min=25,
                max=150,
                step=1,
                value=100,
                marks={i: f'{i}' for i in range(25, 151, 25)},
                tooltip={"placement": "bottom", "always_visible": True}
            ),
            dbc.Input(
                id='hgs-input',
                type='number',
                placeholder='Enter value',
                value=100,
                min=25,
                max=150,
                step=1,
                n_submit=0,
                className="mt-2"
            ),
        ], md=4),
        
        dbc.Col([
            html.H5("Target Fibre Angle (degrees)"),
            dcc.Slider(
                id='angle-slider',
                min=10,
                max=80,
                step=1,
                value=45,
                marks={i: f'{i}°' for i in range(0, 91, 10)},
                tooltip={"placement": "bottom", "always_visible": True}
            ),
            dbc.Input(
                id='angle-input',
                type='number',
                placeholder='Enter value',
                value=45,
                min=10,
                max=80,
                step=1,
                n_submit=0,
                className="mt-2"
            ),
        ], md=4),
    ], className="mb-5 p-4 border rounded bg-light"),
    
    dbc.Row([
        dbc.Col([
            dcc.Graph(id='fibre-angle-graph')
        ])
    ]),
    
    dbc.Row([
        dbc.Col([
            html.Div(id='intersection-info', className="mt-4 p-3 bg-info text-white rounded")
        ])
    ]),
    
    dbc.Row([
        dbc.Col([
            html.Hr(className="mt-5 mb-4"),
            html.Div([
                html.P("Developed by Antony Nixon, University of Sheffield AMRC", className="text-center mb-1"),
                html.P("A.Nixon@amrc.co.uk", className="text-center mb-1"),
                html.P(f"© {2025} All rights reserved", className="text-center text-muted small")
            ], className="mb-4")
        ])
    ])
], fluid=True)


# Callback to sync slider with input
@app.callback(
    Output('dm-slider', 'value'),
    [Input('dm-input', 'value'),
     Input('dm-input', 'n_submit')],
    prevent_initial_call=False
)
def update_dm_slider(input_value, n_submit):
    if input_value is not None:
        return max(1, min(1000, input_value))
    return 100


# Callback to sync input with slider
@app.callback(
    Output('dm-input', 'value'),
    Input('dm-slider', 'value'),
    prevent_initial_call=False
)
def update_dm_input(slider_value):
    return slider_value


# Callback to sync slider with input for HGS
@app.callback(
    Output('hgs-slider', 'value'),
    [Input('hgs-input', 'value'),
     Input('hgs-input', 'n_submit')],
    prevent_initial_call=False
)
def update_hgs_slider(input_value, n_submit):
    if input_value is not None:
        return max(25, min(150, input_value))
    return 100


# Callback to sync input with slider for HGS
@app.callback(
    Output('hgs-input', 'value'),
    Input('hgs-slider', 'value'),
    prevent_initial_call=False
)
def update_hgs_input(slider_value):
    return slider_value


# Callback to sync slider with input for angle
@app.callback(
    Output('angle-slider', 'value'),
    [Input('angle-input', 'value'),
     Input('angle-input', 'n_submit')],
    prevent_initial_call=False
)
def update_angle_slider(input_value, n_submit):
    if input_value is not None:
        return max(10, min(80, input_value))
    return 45


# Callback to sync input with slider for angle
@app.callback(
    Output('angle-input', 'value'),
    Input('angle-slider', 'value'),
    prevent_initial_call=False
)
def update_angle_input(slider_value):
    return slider_value


# Callback to sync slider with input for n
@app.callback(
    Output('n-slider', 'value'),
    [Input('n-input', 'value'),
     Input('n-input', 'n_submit')],
    prevent_initial_call=False
)
def update_n_slider(input_value, n_submit):
    if input_value is not None:
        return max(1, min(192, input_value))
    return 192


# Callback to sync input with slider for n
@app.callback(
    Output('n-input', 'value'),
    Input('n-slider', 'value'),
    prevent_initial_call=False
)
def update_n_input(slider_value):
    return slider_value


@app.callback(
    [Output('fibre-angle-graph', 'figure'),
     Output('intersection-info', 'children')],
    [Input('dm-slider', 'value'),
     Input('hgs-slider', 'value'),
     Input('angle-slider', 'value'),
     Input('n-slider', 'value')]
)
def update_graph(dm, hgs, target_angle, n):
    # Create velocity range
    v_range = np.linspace(0, 100, 200)
    
    # Calculate fibre angle for all velocities
    numerator = (np.pi * dm) * hgs
    denominator = (n / 4) * v_range * 60
    alpha_deg = np.degrees(np.arctan(numerator / denominator))
    
    # Find intersection with target angle
    idx = np.argmin(np.abs(alpha_deg - target_angle))
    v_intersect = v_range[idx]
    alpha_at_intersect = alpha_deg[idx]
    
    # Create figure
    fig = go.Figure()
    
    # Add main line
    fig.add_trace(go.Scatter(
        x=v_range,
        y=alpha_deg,
        mode='lines',
        name=f'HGS = {hgs} RPM',
        line=dict(color='teal', width=3),
        hovertemplate='Velocity: %{x:.2f} mm/s<br>Fibre Angle: %{y:.2f}°<extra></extra>'
    ))
    
    # Add target angle line
    fig.add_hline(
        y=target_angle,
        line_dash="dash",
        line_color="darkorange",
        name=f'Target: {target_angle}°',
        annotation_text=f'Target: {target_angle}°',
        annotation_position="right"
    )
    
    # Add intersection point
    fig.add_trace(go.Scatter(
        x=[v_intersect],
        y=[alpha_at_intersect],
        mode='markers',
        marker=dict(size=12, color='red'),
        name='Intersection',
        hovertemplate=f'Intersection at {v_intersect:.2f} mm/s<extra></extra>'
    ))
    
    # Update layout
    fig.update_layout(
        title=f'Fibre Angle (α) vs. Mandrel Velocity<br>({n} Gears, {dm}mm Mandrel, {hgs} RPM)',
        xaxis_title='Mandrel Velocity (v) [mm/s]',
        yaxis_title='Fibre Angle (α) [degrees]',
        hovermode='x unified',
        template='plotly_white',
        height=500,
        xaxis=dict(range=[0, 100]),
        yaxis=dict(range=[0, 90]),
        font=dict(size=12)
    )
    
    # Info text
    info_text = html.Div([
        html.P(f"Number of Horn Gears: {n}", className="mb-2"),
        html.P(f"Mandrel Diameter: {dm} mm", className="mb-2"),
        html.P(f"Horn Gear Speed: {hgs} RPM", className="mb-2"),
        html.P(f"Target Fibre Angle: {target_angle}°", className="mb-2"),
        html.Hr(),
        html.P(
            f"To achieve {target_angle}° at {hgs} RPM, use a mandrel velocity of approximately {v_intersect:.2f} mm/s",
            className="fw-bold"
        )
    ])
    
    return fig, info_text


if __name__ == '__main__':
    print("Starting interactive app at http://127.0.0.1:8050/")
    app.run(debug=True)
